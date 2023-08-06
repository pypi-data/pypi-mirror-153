import boto3

## Load infin_boto3, even if not used, to decorate boto3
from infinstor import infin_boto3
import tempfile
import mlflow
import os
import json
import pandas as pd
from infinstor import infinslice, infinsnap
from infinstor.infinfs import infinmount
from urllib.parse import urlparse
import multiprocessing
import glob
import copy

def list_one_dir(client, bucket, prefix_in, arr):
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix_in, Delimiter="/")
    for page in page_iterator:
        contents = page.get('Contents')
        if (contents != None):
            # print('   ' + str(contents))
            for one_content in contents:
                if 'Metadata' in one_content:
                    md = json.loads(one_content['Metadata'])
                else:
                    md = {}
                md['FileName'] = one_content['Key']
                md['FileSize'] = one_content['Size']
                md['FileLastModified'] = one_content['LastModified']
                if 'versionId' in one_content:
                    md['FileVersionId'] = one_content['versionId']
                arr.append(md)

        common_prefixes = page.get('CommonPrefixes')
        if (common_prefixes != None):
            for prefix in common_prefixes:
                this_prefix = str(prefix['Prefix'])
                # print('   ' + this_prefix)
                if this_prefix:
                    list_one_dir(client, bucket, this_prefix, arr)


def get_artifact_info_from_run(run_info, input_spec=None):
    artifact_uri = run_info.info.artifact_uri
    parse_result = urlparse(artifact_uri)
    if (parse_result.scheme != 's3'):
        raise ValueError('Error. Do not know how to deal with artifacts in scheme ' \
                         + parse_result.scheme)
    bucket = parse_result.netloc
    if input_spec and 'prefix' in input_spec:
        prefix = input_spec['prefix'].lstrip('/').rstrip('/')
    else:
        prefix = os.path.join(parse_result.path.lstrip('/'))
    return bucket, prefix


def load_input_spec(input_spec, request_prefix):
    if input_spec['type'] == 'infinsnap' or input_spec['type'] == 'infinslice':
        time_spec = input_spec.get('time_spec')
        bucket = input_spec['bucketname']
        prefix = input_spec['prefix']
    elif input_spec['type'] == 'mlflow-run-artifacts':
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(input_spec['run_id'])
        bucket, prefix = get_artifact_info_from_run(run, input_spec)
        #For mlflow artifacts i.e. intermediate input, request prefix is appended
        time_spec = None
    if request_prefix:
        prefix = os.path.join(prefix, request_prefix)
    return bucket, prefix, time_spec


def list_files_meta(bucket, request_prefix, input_name=None, start_time=None, end_time=None):
    ##Override input with runtime inputspec
    input_spec_list = infinmount.get_input_spec_json(input_name=input_name)
    data_frames = []
    all_keys = set()
    storage_spec_list = []
    for input_spec in input_spec_list:
        arr = []
        if input_spec:
            bucket, prefix, infinstor_time_spec = load_input_spec(input_spec, request_prefix)
        else:
            prefix = request_prefix
            if (start_time and end_time):
                infinstor_time_spec = infinslice(start_time, end_time)
            elif (end_time):
                infinstor_time_spec = infinsnap(end_time)
            else:
                infinstor_time_spec = None
        if not infinstor_time_spec:
            infinstor_time_spec = infinsnap()
        client = boto3.client('s3', infinstor_time_spec=infinstor_time_spec)
        if input_spec and input_spec['type'] == 'mlflow-run-artifacts':
            metadata_found = load_mlflow_artifacts_metadata(client, bucket, prefix, arr)
            if not metadata_found:
                list_one_dir(client, bucket, prefix, arr)
        else:
            list_one_dir(client, bucket, prefix, arr)
        df = pd.DataFrame(arr)
        if df.empty:
            print(f"No data found for input spec {input_spec}... Skipping")
            continue
        keygen_src = None
        if 'partition_keygen' in input_spec:
            keygen_src = input_spec['partition_keygen']
        key_list = apply_keygen(df, keygen_src)
        all_keys.update(key_list)
        storage_specs = {
            'bucket': bucket,
            'prefix': prefix.strip('/'),
            'infinstor_time_spec': infinstor_time_spec,
            'input_spec_type': input_spec['type']
        }
        storage_spec_list.append(storage_specs)
        data_frames.append(df)

    if not data_frames:
        print('Warning: no dataframes to process')
        return pd.DataFrame()

    df_to_keep = []
    storage_specs_to_keep = []
    all_keys = sorted(all_keys)
    for df, sspec in zip(data_frames, storage_spec_list):
        df = filter_df_for_partition(df, input_spec, all_keys)
        if not df.empty:
            df_to_keep.append(df)
            storage_specs_to_keep.append(sspec)

    row_count = 0
    for df, storage_spec in zip(df_to_keep, storage_specs_to_keep):
        storage_spec['row_start'] = row_count
        storage_spec['num_rows'] = df.shape[0]
        row_count = row_count + df.shape[0]


    if df_to_keep:
        combined_df = pd.concat(df_to_keep, ignore_index=True)
        combined_df.attrs['storage_specs'] = storage_specs_to_keep
        return combined_df
    else:
        return pd.DataFrame()


def filter_df_for_partition(df, input_spec, all_keys):
    if 'parallelization_schedule' in input_spec:
        psched = input_spec['parallelization_schedule']
        if psched[0] == 'default':
            filtered_df = default_partitioner_filter(df, all_keys, psched[1], psched[2])
            return filtered_df
    return df


def perform_mount_for_mount_spec(df, mount_spec, mount_path, download_ok=True):
    path_list = df['FileName'].tolist()
    # replace the cloud prefix by mounted path
    cloud_prefix = mount_spec['prefix']
    cloud_prefix_len = len(cloud_prefix) + 1
    local_file_list = []
    for fpath in path_list:
        local_path = os.path.join(mount_path, fpath[cloud_prefix_len:])
        local_file_list.append(local_path)

    if 'INFINSTOR_SERVICE' not in os.environ:
        ##Download files for local access
        if download_ok:
            perform_download(path_list, local_file_list, mount_spec)
        else:
            raise ('Cannot mount the cloud path in this environment')
    else:
        infinmount.perform_mount(mount_path, mount_spec)

    return local_file_list


def get_file_paths_local(df, download_ok=True):
    if 'storage_specs' in df.attrs:
        mount_specs = df.attrs['storage_specs']
    else:
        raise('File locations not available')

    mount_path = tempfile.mkdtemp()

    all_local_files = []
    for i, m_spec in enumerate(mount_specs):
        m_path = os.path.join(mount_path, "part-" + str(i))
        os.mkdir(m_path)
        m_spec['mountpoint'] = m_path
        rb = m_spec['row_start']
        re = rb + m_spec['num_rows']
        local_file_list = perform_mount_for_mount_spec(df[rb:re], m_spec, m_path)
        all_local_files.extend(local_file_list)
    return all_local_files


def get_paths_dir_by_dir(df):
    if 'storage_specs' in df.attrs:
        mount_specs = df.attrs['storage_specs']
    else:
        raise('File locations not available')

    mount_path = tempfile.mkdtemp()

    local_dir_list = []
    for i, m_spec in enumerate(mount_specs):
        m_path = os.path.join(mount_path, "part-" + str(i))
        os.mkdir(m_path)
        m_spec['mountpoint'] = m_path
        rb = m_spec['row_start']
        re = rb + m_spec['num_rows']
        local_file_list = perform_mount_for_mount_spec(df[rb:re], m_spec, m_path)
        for fpath in local_file_list:
            local_dir = os.path.dirname(fpath)
            if local_dir not in local_dir_list:
                local_dir_list.append(local_dir)
    return local_dir_list


def init_pool_task(time_spec):
    global s3_client_worker
    if time_spec:
        s3_client_worker = boto3.client('s3', infinstor_time_spec=time_spec)
    else:
        s3_client_worker = boto3.client('s3')

def download_from_s3(task):
    bucket_name, cloud_path, local_path = task
    if not os.path.exists(local_path):
        s3_client_worker.download_file(bucket_name, cloud_path, local_path)


def perform_download(cloud_path_list, local_file_list, mount_spec):
    bucket_name = mount_spec['bucket']
    time_spec = mount_spec.get('infinstor_time_spec')

    task_list = []
    for idx, fname in enumerate(local_file_list):
        cloud_path = cloud_path_list[idx]
        task_list.append((bucket_name, cloud_path, fname))

    mp_pool = multiprocessing.Pool(min(multiprocessing.cpu_count(), len(cloud_path_list)), init_pool_task, [time_spec])
    mp_pool.map(download_from_s3, task_list)


def log_metadata(local_path, artifact_path, *args, **kwargs):
    ##args are treated as keys
    ##kwargs are treated as metadata.
    if 'INFINSTOR_SERVICE' not in os.environ:
        return
    print('Emitting output#')
    print(local_path, artifact_path, kwargs)
    metadata = kwargs
    active_run = mlflow.active_run()
    bucket, prefix = get_artifact_info_from_run(active_run)
    all_files = glob.iglob(local_path, recursive=True)
    all_metadata = []
    for fpath in all_files:
        md = copy.deepcopy(metadata)
        remote_path = os.path.join(prefix, artifact_path, os.path.basename(fpath))
        md['FileName'] = remote_path
        all_metadata.append(md)

    meta_file_name = artifact_path.replace('/', '__') + "__" + os.path.basename(local_path) + ".json"
    metadata_tmp_local = os.path.join(tempfile.mkdtemp(), meta_file_name)
    os.makedirs(os.path.dirname(metadata_tmp_local), exist_ok=True)
    with open(metadata_tmp_local, "w") as fh:
        json.dump(all_metadata, fh)
    print("Log metadata: ", metadata_tmp_local, ".infinstor/metadata")
    mlflow.log_artifact(metadata_tmp_local, ".infinstor/metadata")


def infin_log_artifact(local_path, artifact_path, *args, **kwargs):
    ##args are treated as keys
    ##kwargs are treated as metadata.
    if 'INFINSTOR_SERVICE' not in os.environ:
        return
    log_metadata(local_path, artifact_path, *args, **kwargs)
    print("Log data output: ", local_path, artifact_path)
    mlflow.log_artifact(local_path, artifact_path)


def infin_log_artifacts(local_dir, artifact_path, *args, **kwargs):
    ##args are treated as keys
    ##kwargs are treated as metadata.
    if 'INFINSTOR_SERVICE' not in os.environ:
        return
    log_metadata(local_dir, artifact_path, *args, **kwargs)
    print("Log data output: ", local_dir, artifact_path)
    mlflow.log_artifacts(local_dir, artifact_path)


def load_mlflow_artifacts_metadata(client, bucket, prefix, arr):
    remote_folder = os.path.join(prefix, ".infinstor/metadata")
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=remote_folder, Delimiter="/")
    all_metadata = []
    for page in page_iterator:
        contents = page.get('Contents')
        if contents:
            for one_content in contents:
                key = one_content['Key']
                if key.endswith('.meta'):
                    data = client.get_object(Bucket=bucket, Key=key)
                    meta_object = data['Body'].read()
                    metadata = json.loads(meta_object.decode("utf-8"))
                    all_metadata = all_metadata + metadata
    arr.extend(all_metadata)
    return bool(all_metadata)


def default_partitioner_filter(df, all_keys, num_bins, index):
    if not all_keys:
        print("Warning: No filtering applied")
        return df
    key_subset = set()
    for i, key in enumerate(all_keys):
        if i % num_bins == index:
            key_subset.add(key)
    filtered_df = df[df.apply(lambda row: row['partitioning_key'] in key_subset, axis=1)]
    return filtered_df


def apply_keygen(df, keygen_src):
    if not keygen_src:
        if 'partitioning_key' in df.columns:
            keygen_func = lambda row : row['partitioning_key']
        else:
            ##By default we use object partitioning
            keygen_func = lambda row: row['FileName']
    elif keygen_src == 'directory':
        keygen_func = lambda row : os.path.basename(os.path.dirname(row['FileName']))
    elif keygen_src == 'object':
        keygen_func = lambda row: row['FileName']
    else:
        keygen_func = eval(keygen_src)
    keydf = pd.DataFrame([])
    keydf['partitioning_key'] = df.apply(lambda row: keygen_func(row), axis = 1)
    df['partitioning_key'] = keydf['partitioning_key']
    return sorted(keydf['partitioning_key'].unique())






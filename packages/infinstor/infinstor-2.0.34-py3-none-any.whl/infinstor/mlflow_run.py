import os
import sys
import argparse
from typing import List
from . import run_transform_inline
import json
from mlflow import start_run
import base64

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', help='infinstor|isstage?|isdemo?')
    parser.add_argument('--input_data_spec', help='input data spec')
    parser.add_argument('--xformname', help='name of transformation')
    args, unknown_args = parser.parse_known_args()
    print(str(unknown_args))
    kwa = dict()
    for ou in unknown_args:
        if (ou.startswith('--')):
            oup = ou[2:].split('=')
            if (len(oup) == 2):
                kwa[oup[0]] = oup[1]
    print(str(kwa))
    if args.input_data_spec.startswith('base64:'):
        input_data_spec = json.loads(base64.b64decode(args.input_data_spec[7:]).decode('utf-8'))
    else:
        input_data_spec = json.loads(args.input_data_spec)
    retval = None  # assign to avoid the error: 'variable used before assignment' in the 'return' statement below
    if (len(kwa.items()) > 0):
        with start_run() as run:
            retval = run_transform_inline(args.service, run.info.run_id,
                input_data_spec, args.xformname, **kwa)
    else:
        with start_run() as run:
            retval = run_transform_inline(args.service, run.info.run_id,
                input_data_spec, args.xformname)
    
    return retval

if __name__ == "__main__":
    main()

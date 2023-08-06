# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
import importlib
from pathlib import Path


def get_files(inputs):
    files = []
    for i in inputs:
        if i is None:
            continue
        for f in Path(i).glob('**/*'):
            if f.is_file():
                files.append(str(f))
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scoring_module_name')
    args, extra_args = parser.parse_known_args()

    input_fds = []
    for index, arg in enumerate(extra_args):
        if arg.startswith('--input_fds_') and index + 1 < len(extra_args) and Path(extra_args[index + 1]).exists():
            input_fds.append(extra_args[index + 1])

    scoring_module_path = Path(args.scoring_module_name)
    if scoring_module_path.exists():
        scoring_module_name = scoring_module_path.as_posix()[:-3].replace('/', '.')
        scoring_module = importlib.import_module(scoring_module_name)
    else:
        raise ValueError(f'{args.scoring_module_name} not exists in working directory')

    if hasattr(scoring_module, 'init'):
        scoring_module.init()

    scoring_module.run(get_files(input_fds))

    if hasattr(scoring_module, 'shutdown'):
        scoring_module.shutdown()

# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import json
from pathlib import Path, PureWindowsPath


def _normalize_identifier_name(name):
    import re
    normalized_name = name.lower()
    normalized_name = re.sub(r'[\W_]', ' ', normalized_name)  # No non-word characters
    normalized_name = re.sub(' +', ' ', normalized_name).strip()  # No double spaces, leading or trailing spaces
    if re.match(r'\d', normalized_name):
        normalized_name = 'n' + normalized_name  # No leading digits
    return normalized_name


def _sanitize_python_variable_name(name: str):
    return _normalize_identifier_name(name).replace(' ', '_')


def _sanitize_python_variable_name_with_value_check(name: str):
    sanitized_name = _sanitize_python_variable_name(name)
    if sanitized_name == '':
        raise ValueError(f'Given name {name} could not be normalized into python variable name.')
    return sanitized_name


def _get_or_sanitize_python_name(name: str, name_map: dict):
    return name_map[name] if name in name_map.keys() \
        else _sanitize_python_variable_name(name)


def is_float_convertible(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_int_convertible(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_bool_string(string):
    if not isinstance(string, str):
        return False
    return string == 'True' or string == 'False'


def _unique(elements, key):
    return list({key(element): element for element in elements}.values())


def _is_prod_workspace(workspace):
    if workspace is None:
        return True

    return workspace.location != "eastus2euap" and workspace.location != "centraluseuap" and \
        workspace.subscription_id != "4faaaf21-663f-4391-96fd-47197c630979" and \
        workspace.subscription_id != "74eccef0-4b8d-4f83-b5f9-fa100d155b22"


def _in_jupyter_nb():
    """Return true if the platform widget is running on is Jupyter notebook, otherwise return false."""
    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except (NameError, ModuleNotFoundError):
        return False  # Probably standard Python interpreter


def _is_json_string_convertible(string):
    try:
        json.loads(string)
    except ValueError:
        return False
    return True


def _get_short_path_name(path, create_dir=False):
    '''
        https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file#short-vs-long-names
        Maximum length for a path may defined by 260 characters in Windows.
        So need to trans path to shorten path to avoid filename too long.
        Example short/long path in windows:
            long path: C:\\pipeline-local_run\\67a8bfde-9014-45c0-acc7-1db02d422302\\A dummy pipeline
            short path: C:\\PIPELI~2\\67A8BF~1\\ADUMMY~1
        :param path: need to be shorten path
        :type path: str
        :param create_dir: If create_dir=True, when create dirs before get shorten name
        :type create_dir: bool
        :return: short path form. If path is a short path, will no change.
        :rtype: str
    '''
    if os.name == 'nt':
        try:
            # win32api is an additional module for windows in pywin32
            # https://docs.python.org/3/using/windows.html#additional-modules
            import win32api
            path_list = Path(path).absolute().parts
            short_path = win32api.GetShortPathName(os.path.join(path_list[0]))
            for item in path_list[1:]:
                if create_dir:
                    Path(os.path.join(short_path, item)).mkdir(parents=True, exist_ok=True)
                short_path = win32api.GetShortPathName(os.path.join(short_path, item))
            return short_path
        except Exception:
            # If path is not exist will raise error.
            return str(PureWindowsPath(Path(path).absolute()))
    else:
        return path


def _get_valid_directory_path(directory_path):
    suffix = 1
    valid_path = directory_path
    while os.path.exists(valid_path):
        valid_path = '{}({})'.format(directory_path, suffix)
        suffix += 1
    return valid_path


def _scrubbed_exception(exception_type, msg: str, args):
    """
    Return the exception with scrubbed error message. Use this to add scrubbed message to exceptions
    that we don't want the record the full message in because it may contains sensitive information.

    :param exception_type: The exception type to create.
    :param msg: The message format.
    :param args: The original args for message formatting.
    :return: The created exception.
    """
    scrubbed_data = '[Scrubbed]'
    e = exception_type(msg.format(args))
    e.scrubbed_message = msg.replace("{}", scrubbed_data)
    return e


def _is_github_url(yaml_file: str):
    import re
    return re.match(r'^(https?://)?github.com', yaml_file)

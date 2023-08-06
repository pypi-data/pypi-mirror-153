import io
import json
import os

import yaml
from loguru import logger


def get_file_path(url, entry_json):
    """ Gets of folders for the specified path. """
    file_name = 'test_' + ''.join(url.split("/")[-1].capitalize())
    api = is_file_exist(os.path.join(os.getcwd(), "api"))
    module = is_file_exist(
        os.path.join(
            api, {"module": v.get("tags")[0] for k, v in entry_json.items()}.get("module")))
    return os.path.join(module, file_name)


def is_file_exist(files):
    """
    Check whether the file exists
    """
    if not os.path.exists(files):
        os.mkdir(files)
    return files


def dump_yaml(case, yaml_file):
    """ dump HAR entries to yaml testCase
    """
    if os.path.exists(yaml_file):
        logger.debug("File exists, skip this parsing")
        return

    logger.info("dump testCase to YAML format.")
    with io.open(yaml_file, 'w', encoding="utf-8") as outfile:
        yaml.dump(case, outfile, allow_unicode=True, default_flow_style=False, indent=4)

        logger.info("Generate YAML testCase successfully: {}".format(yaml_file))


def dump_json(case, json_file):
    """ dump HAR entries to json testCase
    """
    logger.info("dump testCase to JSON format.")

    with io.open(json_file, 'w', encoding="utf-8") as outfile:
        my_json_str = json.dumps(case, ensure_ascii=False, indent=4)
        if isinstance(my_json_str, bytes):
            my_json_str = my_json_str.decode("utf-8")
        outfile.write(my_json_str)
    logger.info("Generate JSON testCase successfully: {}".format(json_file))


def get_target_value(key, _json, tmp_list=None):
    """
    Get the target value from the dictionary
    """
    if tmp_list is None:
        tmp_list = []

    if not isinstance(_json, dict) or not isinstance(tmp_list, list):
        return 'args[1] not an dict or args[-1] not an list.'

    if key in _json.keys():
        tmp_list.append(_json[key])

    for value in _json.values():
        if isinstance(value, dict):
            get_target_value(key, value, tmp_list)
        elif isinstance(value, (list, tuple)):
            _get_list_value(key, value, tmp_list)

    return tmp_list


def _get_list_value(key, value, tmp_list):
    """
    Iterate through the list to get the target value
    """
    for val_ in value:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)
        elif isinstance(val_, (list, tuple)):
            _get_list_value(key, val_, tmp_list)

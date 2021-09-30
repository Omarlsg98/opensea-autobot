import random
import time

import os
import os.path as path
import logging

from config import SECS_RANGE_FOR_CLICKS


def beautify_list(list_: list) -> str:
    str_ = ""
    total = len(list_)
    for index, item in enumerate(list_):
        if index < total - 2:
            str_ += f"{item}, "
        elif index < total - 1:
            str_ += f"{item} y "
        else:
            str_ += item
    return str_


def safe_str_to_int(string: str) -> int:
    characters_to_remove = " abcdefghijklmnñopqrstuvwxyz,"
    for character in characters_to_remove:
        string = string.replace(character, "")
    return int(string)


writes_memory = {}


def append_write_pandas_csv(file_path, dataframe, overwrite=False, index=False):
    global writes_memory
    if writes_memory.get(file_path):
        writes_memory[file_path] = writes_memory[file_path] + 1
    else:
        writes_memory[file_path] = 1
        if overwrite:
            delete_file(file_path)

    if path.isfile(file_path):
        mode = "a"
        header = False
    else:
        mode = "w"
        header = True
    dataframe.to_csv(file_path, index=index, mode=mode, header=header)


def create_csv_headers(file_path, headers):
    if not path.isfile(file_path):
        with open(file_path, 'w') as fd:
            fd.write(headers)


def append_to_csv(file_path, data, verbose):
    with open(file_path, 'a') as fd:
        fd.write(f"\n{data}")
        if verbose:
            logging.info(f"Data appended to {file_path}")


def delete_file(file_path):
    os.remove(file_path)
    logging.info(f"{file_path} removed successfully")


def sleep_random(range_secs_to_sleep: (float, float) = SECS_RANGE_FOR_CLICKS):
    time.sleep(random.uniform(*range_secs_to_sleep))


def get_execution_list_from_config(extract_dict: dict, key_to_extract):
    if key_to_extract != "":
        prefix = key_to_extract + "/"
        if extract_dict.get(key_to_extract):
            extract_dict = extract_dict[key_to_extract]
        else:
            return []
    else:
        prefix = key_to_extract

    extract_list = []
    for key, value in extract_dict.items():
        if type(value) is dict and value.get("enabled"):
            extract_list.append(prefix + key)
        elif type(value) is not dict and value:
            extract_list.append(prefix + key)
    return extract_list

# This is a sample Python script.
import configparser as configparser
import os
import glob
import time
from pathlib import Path

CONFIG_FILE_NAME = 'config.ini'
CONF_COMMON_KEY = 'Common'
CONF_COMMON_KEEP_FILES_KEY = 'keep_files'
CONF_COMMON_KEEP_FILES = 10
CONF_COMMON_KEEP_PATH_KEY = 'keep_path'
CONF_COMMON_KEEP_PATH = '.'
CONF_BACKUP_FILE_PREFIX_KEY = 'keep_file_prefix'
CONF_BACKUP_FILE_PREFIX = 'NOTHING-SET'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def load_config():
    global CONF_COMMON_KEEP_FILES, CONF_COMMON_KEEP_PATH, CONF_BACKUP_FILE_PREFIX

    if not os.path.exists(CONFIG_FILE_NAME):
        print("[ERR!] Config file <{}> does not exists.".format(CONFIG_FILE_NAME))
        return

    print("[INFO] Config file found. Loading values.")
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    confi_params_loaded = 0
    if CONF_COMMON_KEEP_FILES_KEY in config[CONF_COMMON_KEY]:
        CONF_COMMON_KEEP_FILES = config[CONF_COMMON_KEY][CONF_COMMON_KEEP_FILES_KEY]
        confi_params_loaded = confi_params_loaded + 1
    if CONF_COMMON_KEEP_PATH_KEY in config[CONF_COMMON_KEY]:
        CONF_COMMON_KEEP_PATH = config[CONF_COMMON_KEY][CONF_COMMON_KEEP_PATH_KEY]
        confi_params_loaded = confi_params_loaded + 1
    if CONF_BACKUP_FILE_PREFIX_KEY in config[CONF_COMMON_KEY]:
        CONF_BACKUP_FILE_PREFIX = config[CONF_COMMON_KEY][CONF_BACKUP_FILE_PREFIX_KEY]
        confi_params_loaded = confi_params_loaded + 1

    print("[ OK ] <{}> config params loaded from <{}>.".format(confi_params_loaded, CONFIG_FILE_NAME))


def print_directory(path):
    if not os.path.exists(path):
        print("[ERR!] Path <{}> does not exists.".format(path))
        return

    print("[INFO] Path <{}> exists.".format(path))
    print("[INFO] Search for files with prefix <{}>".format(CONF_BACKUP_FILE_PREFIX))
    l_files = os.listdir(path)
    for file in l_files:
        if file.startswith(CONF_BACKUP_FILE_PREFIX):
            print("Prefix yes: {}".format(file))
        else:
            print("Prefix  no: {}".format(file))


def get_count_of_possible_files(path):
    if not os.path.exists(path):
        print("[ERR!] Path <{}> does not exists.".format(path))
        return

    print("[INFO] Path <{}> exists.".format(path))
    print("[INFO] Search for files with prefix <{}>".format(CONF_BACKUP_FILE_PREFIX))
    found_files = 0
    l_files = os.listdir(path)
    for file in l_files:
        if file.startswith(CONF_BACKUP_FILE_PREFIX):
            found_files = found_files + 1

    print("[ OK ] Found <{}> possible files with prefix <{}>".format(found_files, CONF_BACKUP_FILE_PREFIX))
    return found_files


def handle_backup_files(path):
    print("[INFO] Starting backup handling")

    possible_files_count = get_count_of_possible_files(path)
    if possible_files_count > int(CONF_COMMON_KEEP_FILES):
        get_files_to_delete(path)
    else:
        print("[INFO] Found less backup files ({} < {}), nothing to do.".format(possible_files_count,
                                                                                int(CONF_COMMON_KEEP_FILES)))
    print("[ OK ] Backup handling successfully finished")


def get_files_to_delete(path):
    file_list = []
    if not os.path.exists(path):
        print("[ERR!] Path <{}> does not exists.".format(path))
        return file_list

    # l_files = os.listdir(path)
    # for file in l_files:
        # if file.startswith(CONF_BACKUP_FILE_PREFIX):
        #     file_path = Path("{}/{}".format(path, file)).absolute()
        #     # print(os.path.getctime(filePath))
    list_of_files = glob.glob("{}/{}*".format(path, CONF_BACKUP_FILE_PREFIX))
    for index in range(0, int(CONF_COMMON_KEEP_FILES)):
        latest_file = max(list_of_files, key=os.path.getctime)
        list_of_files.remove(latest_file)
        print(latest_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    load_config()
    handle_backup_files(CONF_COMMON_KEEP_PATH)

    print_hi('successfully finished')

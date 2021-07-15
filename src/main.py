# This is a sample Python script.
import configparser as configparser
import os
import time

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
    print(config.sections())
    if CONF_COMMON_KEEP_FILES_KEY in config[CONF_COMMON_KEY]:
        CONF_COMMON_KEEP_FILES = config[CONF_COMMON_KEY][CONF_COMMON_KEEP_FILES_KEY]
    if CONF_COMMON_KEEP_PATH_KEY in config[CONF_COMMON_KEY]:
        CONF_COMMON_KEEP_PATH = config[CONF_COMMON_KEY][CONF_COMMON_KEEP_PATH_KEY]
    if CONF_BACKUP_FILE_PREFIX_KEY in config[CONF_COMMON_KEY]:
        CONF_BACKUP_FILE_PREFIX = config[CONF_COMMON_KEY][CONF_BACKUP_FILE_PREFIX_KEY]


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    load_config()
    print_directory(CONF_COMMON_KEEP_PATH)
    possible_files_count = get_count_of_possible_files(CONF_COMMON_KEEP_PATH)
    if possible_files_count > int(CONF_COMMON_KEEP_FILES):
        print_directory(CONF_COMMON_KEEP_PATH)

    print_hi('successfully finished')

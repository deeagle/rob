# This is a sample Python script.
import configparser as configparser
import logging
import os
import glob
import sys
import getopt
import logging

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
        print_and_log_error("Config file <{}> does not exists.".format(CONFIG_FILE_NAME))
        return

    print_and_log_info("Config file found. Loading values.")
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

    print_and_log_ok("<{}> config params loaded from <{}>.".format(confi_params_loaded, CONFIG_FILE_NAME))


def print_directory(path):
    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exists.".format(path))
        return

    print_and_log_info("Path <{}> exists.".format(path))
    print_and_log_info("Search for files with prefix <{}>".format(CONF_BACKUP_FILE_PREFIX))
    l_files = os.listdir(path)
    for file in l_files:
        if file.startswith(CONF_BACKUP_FILE_PREFIX):
            print("Prefix yes: {}".format(file))
        else:
            print("Prefix  no: {}".format(file))


def get_count_of_possible_files(path):
    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exists.".format(path))
        return

    print_and_log_info("Path <{}> exists.".format(path))
    print_and_log_info("Search for files with prefix <{}>".format(CONF_BACKUP_FILE_PREFIX))
    found_files = 0
    l_files = os.listdir(path)
    for file in l_files:
        if file.startswith(CONF_BACKUP_FILE_PREFIX):
            found_files = found_files + 1

    print_and_log_ok("Found <{}> possible files with prefix <{}>".format(found_files, CONF_BACKUP_FILE_PREFIX))
    return found_files


def handle_backup_files(path, deletion_mode_active):
    print_and_log_info("Starting backup handling")

    possible_files_count = get_count_of_possible_files(path)
    if possible_files_count > int(CONF_COMMON_KEEP_FILES):
        files_to_hold = get_newest_files(path, int(CONF_COMMON_KEEP_FILES))
        files_to_remove = get_filenames_to_delete(path, files_to_hold)
        delete_files(files_to_remove, deletion_mode_active)
    else:
        print_and_log_info("Found less backup files ({} < {}), nothing to do.".format(possible_files_count,
                                                                                int(CONF_COMMON_KEEP_FILES)))
    print_and_log_ok("Backup handling successfully finished")


def get_newest_files(path, newest_files_count):
    newest_files = []
    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exists.".format(path))
        return newest_files

    list_of_files = glob.glob("{}/{}*".format(path, CONF_BACKUP_FILE_PREFIX))
    for index in range(0, newest_files_count):
        latest_file = max(list_of_files, key=os.path.getctime)
        list_of_files.remove(latest_file)
        newest_files.append(latest_file)
        logging.debug("File to hold: {}".format(latest_file))

    return newest_files


def get_filenames_to_delete(path, list_of_newest_files):
    files_to_remove = []

    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exists.".format(path))
        return files_to_remove

    if not list_of_newest_files:
        print_and_log_error("Newest files are empty.")
        return files_to_remove

    list_of_files = glob.glob("{}/{}*".format(path, CONF_BACKUP_FILE_PREFIX))
    for file in list_of_files:
        if file not in list_of_newest_files:
            files_to_remove.append(file)
            logging.debug("File to delete: {}".format(file))

    return files_to_remove


def delete_files(filenames_to_delete, deletion_mode_active):
    if not filenames_to_delete:
        print_and_log_error("Files to delete are empty.")
        return

    files_removed = 0
    for file in filenames_to_delete:
        if os.path.exists(file):
            if deletion_mode_active:
                os.remove(file)
                logging.debug("File <{}> removed.".format(file))
            else:
                print_and_log_info("File <{}> will be removed in deletion mode.".format(file))
            files_removed = files_removed + 1

    if deletion_mode_active:
        print_and_log_ok("<{}> files successfully removed.".format(files_removed))
    else:
        print_and_log_info("<{}> files will be removed in deletion mode.".format(files_removed))


def print_usage():
    print("run rob with -h for further details.")


def print_help():
    print("help")
    print("rob = remove old backups")
    print("-------------------------------------")
    print("-h:    prints this help")
    print("-d:    activates the deletion mode")

    exit(3)


def print_and_log_info(msg):
    logging.info(msg)
    print("[INFO] {}".format(msg))


def print_and_log_ok(msg):
    logging.info(msg)
    print("[ OK ] {}".format(msg))


def print_and_log_warning(msg):
    logging.warning(msg)
    print("[WARN] {}".format(msg))


def print_and_log_error(msg):
    logging.error(msg)
    print("[ERR!] {}".format(msg))
    exit(1)


def main(is_deletion_mode_active):
    logging.basicConfig(filename='rob.log',
                        filemode='a',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname).4s - %(message)s')

    print_and_log_ok("rob starts")
    if is_deletion_mode_active:
        print_and_log_info("deletion mode is active.")
    else:
        print_and_log_info("dry mode is active.")

    load_config()
    handle_backup_files(CONF_COMMON_KEEP_PATH, is_deletion_mode_active)


    print_and_log_ok('rob successfully finished')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    arguments = sys.argv[1:]
    deletion_mode_active = False

    try:
        opts, args = getopt.getopt(arguments, "hd")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        print(opt)
        if opt == '-h':
            print_help()
        elif opt == '-d':
            deletion_mode_active = True

    main(deletion_mode_active)

# rob
#
# rob (remove old backups) is a very simple implementation of a configurable backup management (file-level).
#
# :author: Martin Kock <code@deeagle.de>
# :project: https://github.com/deeagle/rob
import os
import glob
import sys
import getopt
import logging
import yaml

EXIT_CONFIG_ERROR = -1
EXIT_COMMON_ERROR = 1
EXIT_PRINT_HELP = 3

CONFIG_FILE_NAME = 'config.yml'
CONF_COMMON_KEY = 'Common'
CONF_COMMON_KEEP_FILES_KEY = 'files'
CONF_COMMON_KEEP_FILES = 10
CONF_COMMON_KEEP_PATH_KEY = 'path'
CONF_COMMON_KEEP_PATH = '.'
CONF_BACKUP_FILE_PREFIX_KEY = 'file_prefix'
CONF_BACKUP_FILE_PREFIX = 'NOTHING-SET'


def load_config():
    """Loads the preferences from config file."""
    global CONF_COMMON_KEEP_FILES, CONF_COMMON_KEEP_PATH, CONF_BACKUP_FILE_PREFIX

    if not os.path.exists(CONFIG_FILE_NAME):
        print_and_log_error("Config file <{}> does not exist.".format(CONFIG_FILE_NAME))
        exit(EXIT_CONFIG_ERROR)

    print_and_log_info("Config file found. Loading values.")
    with open(CONFIG_FILE_NAME, 'r') as config_file:
        config = yaml.safe_load(config_file)

    config_params_loaded = 0

    if len(config[CONF_COMMON_KEY]) < 1:
        print_and_log_error(
            "<{}> cannot find config params in file <{}>. Exit!".format(
                config_params_loaded,
                CONFIG_FILE_NAME
            )
        )
        exit(EXIT_CONFIG_ERROR)

    # read one 'keep' config per loop
    for config_index in range(0, len(config[CONF_COMMON_KEY])):
        if CONF_COMMON_KEEP_FILES_KEY in config[CONF_COMMON_KEY][config_index]:
            CONF_COMMON_KEEP_FILES = config[CONF_COMMON_KEY][config_index][CONF_COMMON_KEEP_FILES_KEY]
            config_params_loaded = config_params_loaded + 1
        if CONF_COMMON_KEEP_PATH_KEY in config[CONF_COMMON_KEY][config_index]:
            CONF_COMMON_KEEP_PATH = config[CONF_COMMON_KEY][config_index][CONF_COMMON_KEEP_PATH_KEY]
            config_params_loaded = config_params_loaded + 1
        if CONF_BACKUP_FILE_PREFIX_KEY in config[CONF_COMMON_KEY][config_index]:
            CONF_BACKUP_FILE_PREFIX = config[CONF_COMMON_KEY][config_index][CONF_BACKUP_FILE_PREFIX_KEY]
            config_params_loaded = config_params_loaded + 1

        if config_params_loaded == 0:
            print_and_log_error(
                "<{}> config 'keep' params loaded from <{}>. Exit!".format(
                    config_params_loaded,
                    CONFIG_FILE_NAME
                )
            )
            exit(EXIT_CONFIG_ERROR)

    print_and_log_ok("<{}> config params loaded from <{}>.".format(config_params_loaded, CONFIG_FILE_NAME))
    print_and_log_info(
        "config keep: [{} | {} | {}]".format(
            CONF_COMMON_KEEP_FILES,
            CONF_COMMON_KEEP_PATH,
            CONF_BACKUP_FILE_PREFIX
        )
    )


def print_directory(path: str):
    """Logs the directory with included file content (CONF_BACKUP_FILE_PREFIX).

    :param path: The path of the directory
    :return: None if an error occurs (e.g. path does not exist).
    """
    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exist.".format(path))
        return

    print_and_log_info("Path <{}> exists.".format(path))
    print_and_log_info("Search for files with prefix <{}>".format(CONF_BACKUP_FILE_PREFIX))
    l_files = os.listdir(path)
    for file in l_files:
        if file.startswith(CONF_BACKUP_FILE_PREFIX):
            print("Prefix yes: {}".format(file))
        else:
            print("Prefix  no: {}".format(file))


def get_count_of_possible_files(path: str):
    """Returns the count of possible backup files in path.

    :param path: The path to check for backup files.
    :return: The count of possible files to delete.
    """
    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exist.".format(path))
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


def handle_backup_files(path: str, is_deletion_mode_active: bool):
    """ Checks the backup size

    :param path:
    :param is_deletion_mode_active:
    """
    print_and_log_info("Starting backup handling")

    possible_files_count = get_count_of_possible_files(path)
    if possible_files_count > int(CONF_COMMON_KEEP_FILES):
        files_to_hold = get_newest_files(path, int(CONF_COMMON_KEEP_FILES))
        files_to_remove = get_filenames_to_delete(path, files_to_hold)
        delete_files(files_to_remove, is_deletion_mode_active)
    else:
        print_and_log_info("Found less backup files ({} < {}), nothing to do.".format(possible_files_count,
                                                                                      int(CONF_COMMON_KEEP_FILES)))
    print_and_log_ok("Backup handling successfully finished")


def get_newest_files(path: str, newest_files_count: int):
    """Return the newest files in the path with the CONF_BACKUP_FILE_PREFIX.

    :param path: The path to validate
    :param newest_files_count: The count of the newest files to catch
    :return: A list of the newest files (count dependent).
    """
    newest_files = []
    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exist.".format(path))
        return newest_files

    list_of_files = glob.glob("{}/{}*".format(path, CONF_BACKUP_FILE_PREFIX))
    for index in range(0, newest_files_count):
        latest_file = max(list_of_files, key=os.path.getctime)
        list_of_files.remove(latest_file)
        newest_files.append(latest_file)
        logging.debug("File to hold: {}".format(latest_file))

    return newest_files


def get_filenames_to_delete(path: str, list_of_newest_files: list):
    """Concatenation of path and filename

    :param path: The path as prefix for the files
    :param list_of_newest_files: The list of file to add behind the path
    :return: a list of files to remove
    """
    files_to_remove: list[str] = []

    if not os.path.exists(path):
        print_and_log_error("Path <{}> does not exist.".format(path))
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


def delete_files(filenames_to_delete: list, is_deletion_mode_active: bool):
    """Delete the given filenames.

    :param filenames_to_delete: The filenames to delete (absolute path)
    :param is_deletion_mode_active: switches between dry and real deletion mode
    """
    if not filenames_to_delete:
        print_and_log_error("Files to delete are empty.")
        return

    files_removed = 0
    for file in filenames_to_delete:
        if os.path.exists(file):
            if is_deletion_mode_active:
                os.remove(file)
                logging.debug("File <{}> removed.".format(file))
            else:
                print_and_log_info("File <{}> will be removed in deletion mode.".format(file))
            files_removed = files_removed + 1

    if is_deletion_mode_active:
        print_and_log_ok("<{}> files successfully removed.".format(files_removed))
    else:
        print_and_log_info("<{}> files will be removed in deletion mode.".format(files_removed))


def print_usage():
    """Prints the default cli usage."""
    print("run rob with -h for further details.")


def print_help():
    """Prints the cli help."""
    print("help")
    print("rob = remove old backups")
    print("-------------------------------------")
    print("-h:    prints this help")
    print("-d:    activates the deletion mode")

    exit(EXIT_PRINT_HELP)


def print_and_log_info(msg: str):
    """Logs an information message.

    :param msg: the message to print
    """
    logging.info(msg)
    print("[INFO] {}".format(msg))


def print_and_log_ok(msg: str):
    """Logs an okay message.

    :param msg: the message to print
    """
    logging.info(msg)
    print("[ OK ] {}".format(msg))


def print_and_log_warning(msg: str):
    """Logs a warning message.

    :param msg: the message to print
    """
    logging.warning(msg)
    print("[WARN] {}".format(msg))


def print_and_log_error(msg: str):
    """Logs an error message and exits.

    :param msg: the message to print
    """
    logging.error(msg)
    print("[ERR!] {}".format(msg))
    exit(EXIT_COMMON_ERROR)


def main(is_deletion_mode_active: bool):
    """The main function.

    :param is_deletion_mode_active: switch to handle dry run and full deletion mode
    """
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


if __name__ == '__main__':
    arguments = sys.argv[1:]
    deletion_mode_active = False

    try:
        opts, args = getopt.getopt(arguments, "hd")
    except getopt.GetoptError:
        print_usage()
        sys.exit(EXIT_PRINT_HELP)

    for opt, arg in opts:
        print(opt)
        if opt == '-h':
            print_help()
        elif opt == '-d':
            deletion_mode_active = True

    main(deletion_mode_active)

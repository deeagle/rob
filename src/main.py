# This is a sample Python script.
import configparser as configparser

CONF_COMMON_KEY = 'Common'
CONF_COMMON_KEEP_FILES_KEY = 'keep_files'
CONF_COMMON_KEEP_FILES = 10
CONF_COMMON_KEEP_PATH_KEY = 'keep_path'
CONF_COMMON_KEEP_PATH = '.'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def load_config():
    global CONF_COMMON_KEEP_FILES, CONF_COMMON_KEEP_PATH
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(config.sections())
    if CONF_COMMON_KEEP_FILES_KEY in config[CONF_COMMON_KEY]:
        CONF_COMMON_KEEP_FILES = config[CONF_COMMON_KEY][CONF_COMMON_KEEP_FILES_KEY]
    if CONF_COMMON_KEEP_PATH_KEY in config[CONF_COMMON_KEY]:
        CONF_COMMON_KEEP_PATH = config[CONF_COMMON_KEY][CONF_COMMON_KEEP_PATH_KEY]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    load_config()
    print(CONF_COMMON_KEEP_FILES)

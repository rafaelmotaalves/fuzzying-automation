from os import path, makedirs, listdir
from time import sleep
from sys import argv
from shutil import copy
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException

FUZZ = "fuzz"
UNDERSLASH = "_"
EMPTY_STRING = ""
HTML_EXTENSION = ".html"
FILE_PREFIX = "file://"

BROWSER_COMMAND = "epiphany"
PAGE_LOAD_TIMEOUT = 30

SUCCESS_FLAG = "success"
TIMEOUT_FLAG = "timeout"
CRASH_FLAG = "crash"
ERROR_FLAG = "error"

options = webdriver.WebKitGTKOptions()
options.binary_location = BROWSER_COMMAND
options.add_argument("--automation-mode")
options.set_capability("browserName", "Epiphany")
options.set_capability('version', '3.31.4')


def main():
    if len(argv) < 2:
        raise Exception("Must provide a valid html base directory")
    if len(argv) < 3:
        raise Exception("Must provide a valid results directory")

    html_dir = argv[1]
    results_dir = argv[2]

    if not path.exists(results_dir):
        makedirs(results_dir)

    fuzz_files_names = get_fuzz_files_names(html_dir)
    print(fuzz_files_names)
    for fuzz_file in fuzz_files_names:
        try:
            browser = webdriver.WebKitGTK(
                options=options, desired_capabilities={})
            browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

            print("Opening " + fuzz_file)
            browser.get(FILE_PREFIX + fuzz_file)

            print("Waiting for page changes")
            sleep(5)

            # getting the browser title to test access to the browser
            # if the browser has crashed this call should throw an exception
            browser_title = browser.title
            print(browser_title)
            print(fuzz_file + " has not crashed the browser")
            copyfile_to_result(fuzz_file, results_dir, SUCCESS_FLAG)
        except InvalidSessionIdException as e:
            print(fuzz_file + " crashed the browser")
            print(e)
            copyfile_to_result(fuzz_file, results_dir, CRASH_FLAG)
        except TimeoutException as e:
            print(fuzz_file + " timedout loading on the browser")
            print(e)
            copyfile_to_result(fuzz_file, results_dir, TIMEOUT_FLAG)
        except:
            print("A unexpected error ocurred using " + fuzz_file)
            copyfile_to_result(fuzz_file, results_dir, ERROR_FLAG)
        finally:
            try:
                browser.quit()
            except:
                pass


def copyfile_to_result(fuzz_file, results_dir, flag):
    dest_dir = path.join(results_dir, flag)
    if not path.exists(dest_dir):
        makedirs(dest_dir)
    formated_timestamp = datetime.now(tz=None).strftime("%m-%d-%Y-%H:%M:%S")

    copy(fuzz_file, path.join(dest_dir, FUZZ + str(get_file_number(fuzz_file)
                                                   ) + UNDERSLASH + formated_timestamp + HTML_EXTENSION))


def get_fuzz_files_names(base_dir):
    if not path.exists(base_dir):
        raise Exception("Passed html base directory doesn't exist")

    files = listdir(path.abspath(base_dir))  # list files on passed dir

    if len(files) == 0:
        raise Exception(
            "Passed base directory doesn't have any html directories")

    abs_files = map(lambda filename: path.abspath(
        path.join(base_dir, filename)), files)  # get files absolute path
    html_files = filter(lambda x: x.endswith(HTML_EXTENSION),
                        abs_files)  # get only html files
    html_file_list = list(html_files)  # convert "filter" to "list"
    html_file_list.sort(key=get_file_number)

    return html_file_list


def get_file_number(filename):
    return int(path.basename(filename).replace(FUZZ, EMPTY_STRING).replace(HTML_EXTENSION, EMPTY_STRING))


if __name__ == '__main__':
    main()
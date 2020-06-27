from os import path, makedirs, listdir
from time import sleep
from sys import argv

from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException

HTML_EXTENSION=".html"
FILE_PREFIX = "file://"

BROWSER_COMMAND="epiphany"
PAGE_LOAD_TIMEOUT=30


COMPLETE_FLAG="complete"
TIMEOUT_FLAG="timeout"

options = webdriver.WebKitGTKOptions()
options.binary_location = BROWSER_COMMAND
options.add_argument("--automation-mode")
options.set_capability("browserName", "Epiphany")
options.set_capability('version', '3.31.4')

def main():
    if len(argv) < 2:
        raise Exception("Must provide a valid html base directory")

    html_dir = argv[1]

    fuzz_files_names = get_fuzz_files_names(html_dir)

    for fuzz_file in fuzz_files_names:
        try:
            browser = webdriver.WebKitGTK(options=options, desired_capabilities={})
            browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

            print("Opening " + fuzz_file)
            browser.get(FILE_PREFIX + path.abspath(fuzz_file))

            print("Waiting for page changes")
            sleep(5)

            # getting the browser title to test access to the browser
            # if the browser has crashed this call should throw an exception
            browser_title = browser.title
            print(browser_title)
            print(fuzz_file + " has not crashed the browser")
        except InvalidSessionIdException as e :
            print(fuzz_file + " crashed the browser")
            print(e)
        except TimeoutException as e:
            print(fuzz_file + " timedout loading on the browser")
            print(e)
        except:
            print("A unexpected error ocurred using " + fuzz_file)
        finally:
            try:
                browser.quit()
            except:
                pass

def get_fuzz_files_names(base_dir):
    if not path.exists(base_dir):
        raise Exception("Passed html base directory doesn't exist")

    files = listdir(path.abspath(base_dir))

    if len(files) == 0:
        raise Exception("Passed base directory doesn't have any html directories")

    abs_files = map(lambda filename: path.abspath(path.join(base_dir, filename)), files)
    html_files = filter(lambda x: x.endswith(HTML_EXTENSION), abs_files)
    html_file_list = list(html_files)
    html_file_list.sort()

    return html_file_list    

if __name__ == '__main__':
    main()
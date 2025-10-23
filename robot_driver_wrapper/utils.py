import subprocess
import os
import zipfile
import os
import requests
import platform
from datetime import datetime, date
from difflib import SequenceMatcher
if platform.system() == "win32" or platform.system() == "Windows":
    import winreg


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def guess_date(string):
    for fmt in [

        "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y","%m/%-d/%Y",
        "%y/%m/%d", "%d/%m/%y", "%m/%d/%y",
        "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
        "%y-%m-%d", "%d-%m-%y", "%m-%d-%y",
        "%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %H:%M:%S",
        ]:
        try:
            return datetime.strptime(string, fmt).date()
        except ValueError:
            continue
    raise ValueError(string)


def format_dates(input_date):
    _length = len(input_date)
    if _length == 4:
        if int(input_date[-2:]) <= date.today().month:
            _year = date.today().year
        else:
            _year = date.today().year - 1

        py_date = datetime.strptime(f'{input_date}{_year}', '%d%m%Y').date()
    elif _length == 6:
        py_date = datetime.strptime(input_date, '%d%m%y').date()
    elif _length == 9:
        py_date = guess_date(input_date)
    else:
        py_date = guess_date(input_date)

    return py_date.strftime("%Y/%m/%d")


def get_edge_driver():
    [os.unlink(f) for f in os.listdir() if 'msedgedriver.exe' in f]
    [os.unlink(f) for f in os.listdir() if 'edgedriver_win64.zip' in f]
    [os.rmdir(f) for f in os.listdir() if 'edgedriver_win64' in f]

    keyPath2 = r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{56EB18F8-B008-4CBD-B6D2-8C97FE7E9062}"
    key2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                          keyPath2, 0, winreg.KEY_READ)
    edge_version = winreg.QueryValueEx(key2, "pv")[0]

    url = f'https://msedgedriver.microsoft.com/{edge_version}/edgedriver_win64.zip'
    print(url)
    print('Downloading started')

    data = subprocess.check_output(['curl', url])

    # Writing the file to the local file system
    with open('edgedriver_win64.zip', 'wb') as output_file:
        output_file.write(data)
    print('Downloading Completed')

    with zipfile.ZipFile("edgedriver_win64.zip", "r") as zip_ref:
        zip_ref.extract('msedgedriver.exe')

    [os.unlink(f) for f in os.listdir() if 'edgedriver_win64.zip' in f]


def get_chrome_driver():
    [os.unlink(f) for f in os.listdir() if 'chromedriver.exe' in f]
    [os.unlink(f) for f in os.listdir() if 'chromedriver_win32.zip' in f]
    [os.rmdir(f) for f in os.listdir() if 'chromedriver_win32' in f]

    keyPath2 = r"SOFTWARE\WOW6432Node\Google\Update\Clients\{8A69D345-D564-463c-AFF1-A69D9E530F96}"
    key2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                          keyPath2, 0, winreg.KEY_READ)
    chrome_version = winreg.QueryValueEx(key2, "pv")[0]

    url = f'https://chromedriver.storage.googleapis.com/{chrome_version}/chromedriver_win32.zip'
    print(url)
    downloaded = False

    while not downloaded:
        try:
            print(url)
            print('Downloading started')
            data = requests.get(url)

            if data.status_code == 200:
                # Writing the file to the local file system
                with open('chromedriver_win32.zip', 'wb') as chrome:
                    chrome.write(data.content)
                downloaded = True
                print('Downloading Completed')
            else:
                print('error')
                raise Exception("not found")
        except:
            current_fix_version = int(chrome_version.split('.')[-1])
            new_fix_version = current_fix_version - 1
            chrome_version = chrome_version.replace(
                str(current_fix_version), str(new_fix_version))
            url = f'https://chromedriver.storage.googleapis.com/{chrome_version}/chromedriver_win32.zip'

    with zipfile.ZipFile("chromedriver_win32.zip", "r") as zip_ref:
        zip_ref.extract('chromedriver.exe')

    [os.unlink(f) for f in os.listdir() if 'chromedriver_win32.zip' in f]
    
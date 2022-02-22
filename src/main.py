import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import alerts

frequency = 2
urls = []

print("Initializing")
data = []


def get_page(url):
    for attempt in range(2):
        try:
            res = requests.get(url)
            if res.status_code != 200:
                raise Exception(f"An error has occurred while requesting: {url}")
            content = BeautifulSoup(res.text, "html.parser")
        except Exception as e:
            print(f"{e}\nRetrying ({attempt + 1})")
            time.sleep(1)
        else:
            try:
                return content.find("title").string, content.find("body")
            except AttributeError:
                raise AttributeError("This url cannot be tracked")
    else:
        raise Exception("Retry timeout")


def check():
    status = False
    for i, url in enumerate(urls):
        page = get_page(url)
        try:
            if page[1] != data[i][1]:
                print(f"Page \"{data[i][0]}\" has been updated")
                try:
                    alerts.sms(f"Page \"{data[i][0]}\" has been updated")
                except Exception as e:
                    raise Exception(e)
                data[i] = page
                status = True
        except IndexError:
            data.append(page)
            print(f"Tracking: {page[0]}")
    return status


if not urls:
    raise Exception("URL list cannot be empty")
else:
    check()
    print(f"Initial snapshot: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    time.sleep(frequency * 3600)
    while True:
        if not check():
            print("No changes found")
        print(f"Last check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        time.sleep(frequency * 3600)

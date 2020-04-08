import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waitForElement(driver, by_what=By.XPATH, element_info='', delay=30, do_quit=True):
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_what, element_info)))
        print("Page is ready!")
        return elem
    except TimeoutException:
        print("Loading took too much time!")
        print("quiting while waiting for element:", element_info)
        if do_quit:
            driver.quit()
        return None


def sendNotification(app_name, message, additional_message='', event_name='log_from_app'):
    my_key = ''
    data = {
        "value1": app_name,
        "value2": message,
        "value3": additional_message
    }
    url = "https://maker.ifttt.com/trigger/" + event_name + "/with/key/" + my_key

    r = requests.post(url, data=data)

    return r


def send_report_and_close(report, driver, special=''):
    for i in range(10):
        r = sendNotification("Alpha Test", report, additional_message=special)
        if r.status_code == 200:
            break
        else:
            print("Hasn't sent retrying... " + str(i) + " of 10")
    if driver is not None:
        driver.close()
    exit()


def getTorrentLink(cell):
    for x in cell.find_all('a', href=True):
        if 'torrent/' in x['href']:
            return x['href']


options = Options()
# options.add_argument("--headless")  # necessary for RPi
try:
    # path_to_driver = '/usr/bin/chromedriver'
    path_to_driver = '/Users/Alexey/PycharmProjects/Scrapping/chromedriver'

    driver = webdriver.Chrome(path_to_driver, options=options)
except WebDriverException:
    report = 'WebDriver Not Found.'
    send_report_and_close(report, None, special='FATAL')

# TODO: replace with a table of shows
tv_show = "westworld s03e04"
tv_show = tv_show.replace(' ', '+')

# looking up on 1337x
driver.get('https://1337x.gd/search/' + tv_show + '/1/')

"""
    table-list-wrap
"""
waitForElement(driver, element_info="//div[contains(@class,'table-list-wrap')]")

# TODO: add checkups for

# Passing to beautifulsoup
raw_page = BeautifulSoup(driver.page_source, 'html.parser')
# driver.close()

a = raw_page.find_all('tr')[0]

row_marker = 0
column_marker = 0
col_names = []
for b in a.find_all('th'):
    col_names.append(b.get_text())
    column_marker += 1

col_names.append('url')  # assuming there's always some urls
# print(col_names)

urls = []
names = []
ses = []
les = []
times = []
sizes = []
uploaders = []

for row in raw_page.find_all('tr'):
    #     print('row: ', row)
    max_col = len(row.find_all('td'))
    i = 0
    for col in row.find_all('td'):
        if i == 0:
            urls.append(getTorrentLink(col))
            #             print('url: ', getTorrentLink(col))
            names.append(col.get_text())
        #             print('name: ', col.get_text())
        if i == 1:
            ses.append(col.get_text())
        #             print('se: ', col.get_text())
        if i == 2:
            les.append(col.get_text())
        #             print('le: ', col.get_text())
        if i == 3:
            times.append(col.get_text())
        #             print('time: ', col.get_text())
        if i == 4:
            sizes.append(col.get_text())
        #             print('size info: ', col.get_text())
        if i == 5:
            uploaders.append(col.get_text())
        #             print('uploader: ', col.get_text())
        i += 1

curTorrentTable = pd.DataFrame(columns=col_names)

curTorrentTable['name'] = names
curTorrentTable['se'] = ses
curTorrentTable['le'] = les
curTorrentTable['time'] = times
curTorrentTable['size'] = sizes
curTorrentTable['uploader'] = uploaders
curTorrentTable['url'] = urls

# casting types

test = curTorrentTable.copy()
test['size'] = test['size'].replace({r' GB[0-9]+': r''}, regex=True)
test['size'] = test['size'].apply(lambda x: x if ('MB' in x) else float(x) * 1024)
test['size'] = test['size'].replace({r' MB[0-9]+': r''}, regex=True)
test['size'] = test['size'].astype(float)

test['se'] = test['se'].astype(int)
test['le'] = test['le'].astype(int)
test['time'] = pd.to_datetime(test['time'])

best_torrent = test.loc[test.name.str.contains('1080p')]['url'].iloc[0]  # TODO: add better choosing technique

print('trying to add this torrent: ', best_torrent)

best_torrent_link = "https://1337x.gd" + best_torrent
driver.get(best_torrent_link)
waitForElement(driver, element_info="//div[contains(@class,'search-box')]")

final_page = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()  # IMPORTANT

# extracting magnet link, TODO: optimize this

magnet_link = str()
for a in final_page.find_all('a', href=True):
    if 'magnet' in a['href']:
        magnet_link = a['href']
        break

# adding to transmission

print('transmission-remote -a "' + magnet_link + '"')

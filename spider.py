# -*- coding: utf-8 -*-
import pickle
import json
from urllib.request import Request, urlopen
import bs4
from selenium.webdriver.support import expected_conditions as EC
import remove_space
import requests
from selenium import webdriver
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pymongo


def update_cookie(url, file_name, delayed):
    driver = webdriver.PhantomJS(executable_path=r'./resources/phantomjs')
    driver.get(url)
    # 这里加了延时，直到页面找到特定元素 或超时。
    WebDriverWait(driver, delayed).until(EC.presence_of_element_located((By.ID, 'steamdb-org')))
    pickle.dump(driver.get_cookies(), open(file_name, "wb"))


# 读取cookie,并访问网站
def load_to_requests(url, cookies_file, session=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    with open(cookies_file, 'rb') as f:
        cookies = pickle.load(f)
    if session is None:
        session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return requests.get(url, headers=headers).text


def get_price(url):
    html = load_to_requests(url, cookies_file=args.filename)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    all_data = soup.find("div", {"class": "table-responsive"}).find("tbody").find_all("tr")
    price_data = dict()
    for index in range(len(all_data)):
        if all_data[index].find_all("td")[0].text is not None:
            currency = remove_space.remove(all_data[index].find_all("td")[0].text)
            price_data['currency'] = currency

        if all_data[index].find_all("td")[1].text is not None:
            currency_price = all_data[index].find_all("td")[1].text
            price_data['currency_price'] = currency_price

        if all_data[index].find_all("td")[2].text is not None:
            converted_price = all_data[index].find_all("td")[2].text
            price_data['converted_price'] = converted_price

        if all_data[index].find_all("td")[4].text is not None:
            lowest_price = all_data[index].find_all("td")[4].text
            price_data['lowest_price'] = lowest_price

    return price_data




def put_appid_to_db(url, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    db = client["data_appid"]
    col = db["appid"]
    # 构建请求
    request = Request(url)
    html = urlopen(request)
    # 获取数据
    steam_id_data = html.read()
    # 转换成字典数据
    steam_id_json = json.loads(steam_id_data)
    if col.estimated_document_count() < len(steam_id_json['applist']['apps']):
        for index in range(len(steam_id_json['applist']['apps'])):
            data = steam_id_json['applist']['apps'][index]
            col.insert_one(data)
    else:
        print("Data is up to date, and the count is " + str(col.estimated_document_count()))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='update cookie')
    parser.add_argument('-u', '--url', type=str, default='http://steamdb.info/app/578080/?cc=cn')
    parser.add_argument('-f', '--filename', type=str, default='./data/cookies.pkl')
    parser.add_argument('-d', '--delayed', type=int, default=5)
    args = parser.parse_args()
    get_price("http://steamdb.info/app/578080/?cc=cn")
    # update_cookie(url=args.url, file_name=args.filename, delayed=args.delayed)
    # load_to_requests(url=args.url, cookies_file=args.filename)
    # put_appid_to_db('https://api.steampowered.com/ISteamApps/GetAppList/v0002/', 'mongodb://127.0.0.1:27017')

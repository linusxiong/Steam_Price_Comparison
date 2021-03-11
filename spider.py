# -*- coding: utf-8 -*-
import pickle
import bs4
from flask import jsonify
from selenium.webdriver.support import expected_conditions as EC
import models
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pymongo
import api


def update_cookie(url, file_name, delayed):
    driver = webdriver.PhantomJS(executable_path=r'./resources/phantomjs')
    driver.get(url)
    # 这里加了延时，直到页面找到特定元素 或超时。
    WebDriverWait(driver, delayed).until(EC.presence_of_element_located((By.ID, 'steamdb-org')))
    pickle.dump(driver.get_cookies(), open(file_name, "wb"))
    print("update success")


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
    # try:
        html = load_to_requests(url, './data/cookies.pkl')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        all_data = soup.find("div", {"class": "table-responsive"}).find("tbody").find_all("tr")
        data_list = list()
        for index in range(len(all_data)):
            price_data = dict()
            if soup.find("div", {"class": "span8"}).find("tbody").find("tr").find_all("td")[1].text is not None:
                appid = soup.find("div", {"class": "span8"}).find("tbody").find("tr").find_all("td")[1].text
                price_data['appid'] = appid
            else:
                price_data['appid'] = "No appid data"

            if soup.find("h1", {"itemprop": "name"}).text is not None:
                tittle = soup.find("h1", {"itemprop": "name"}).text
                price_data['game_name'] = tittle
            else:
                price_data['game_name'] = "No game_name data"

            if all_data[index].find_all("td")[0].text is not None:
                currency = models.remove(all_data[index].find_all("td")[0].text)
                price_data['currency'] = currency
            else:
                price_data['currency'] = "No currency data"

            if all_data[index].find_all("td")[1].text is not None:
                currency_price = all_data[index].find_all("td")[1].text
                price_data['currency_price'] = currency_price
            else:
                price_data['currency_price'] = "No currency_price data"

            if all_data[index].find_all("td")[2].text is not None:
                converted_price = all_data[index].find_all("td")[2].text
                price_data['converted_price'] = converted_price
            else:
                price_data['converted_price'] = "No converted_price data"

            if all_data[index].find_all("td")[4].text is not None and len(all_data[index].find_all("td")) != 5:
                lowest_price = all_data[index].find_all("td")[4].text
                price_data['lowest_price'] = lowest_price
            else:
                price_data['lowest_price'] = "No lowest_price data"

            if all_data[index].find_all("td", {"class": "muted"})[0].text is not None and len(all_data[index].find_all("td")) != 5:
                discount_minor = all_data[index].find_all("td", {"class": "muted"})[0].text
                price_data['discount_minor'] = discount_minor
            elif len(all_data[index].find_all("td")) == 5:
                lowest_price = all_data[index].find_all("td")[4].text
                price_data['discount_minor'] = lowest_price
            else:
                price_data['discount_minor'] = "No discount_minor data"

            data_list.append(price_data)
        return data_list
    # except:
    #     # jsonify({"status": "error", "detail": "无此GameID"})
    #     print("未查询到ID")


def put_gameinfo_to_db(url, mongo_url):
    # try:
        price_data = get_price(url)
        client = pymongo.MongoClient(mongo_url)
        db = client["game_data"]
        col = db[price_data[0]['appid']]
        for index in range(len(price_data)):
            col.insert_one(price_data[index])
            # print(price_data[index])
    # except:
    #     # jsonify({"status": "error", "detail": "数据库异常"})
    #     print("数据库异常")

# if __name__ == '__main__':
    # print(put_gameinfo_to_db('http://steamdb.info/app/578080111/?cc=cn', 'mongodb://127.0.0.1:27017'))
    # print(get_price("http://steamdb.info/app/578080/?cc=cn"))
    # update_cookie(url=args.url, file_name=args.filename, delayed=args.delayed)
    # load_to_requests(url=args.url, cookies_file=args.filename)
    # print(get_price('http://steamdb.info/app/1468810/?cc=cn'))
    # print(get_price('http://steamdb.info/app/1546540/?cc=cn'))
    # put_appid_to_db('https://api.steampowered.com/ISteamApps/GetAppList/v0002/', 'mongodb://127.0.0.1:27017')

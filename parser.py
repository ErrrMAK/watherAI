# Нужно настроить проверку ip на 200
# Еще нужно доделать сохранение в csv

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
from selenium.webdriver.chrome.options import Options
import os
# from watherAI.ip_rotate import save_to_csv


def csv_reader(massive):
    with open(massive, 'r') as file:
        reader = csv.reader(file)
        list_ip = []
        for row in reader:
            list_ip.append(''.join(list(row)))
    return list_ip


def get_sourse_html():
    # Запускаем перебор
    # ip_list = ['34.139.55.89:8585', '34.145.186.193:8585', '34.174.62.103:8585']
    # months = ["01", "02", "03"]
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    # years = ['2000']
    years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
             '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    data = []
    id_ip = 0
    for i, year in enumerate(years):
        for j, month in enumerate(months):
            # Открываем в браузере ссылку
            # link = 'http://www.meteomanz.com/sy1?ty=hp&l=1&cou=6216&ind=13274&d1=01&m1=02&y1=2022&h1=00Z&d2=31&m2=02&y2=2022&h2=23Z'
            link = 'http://www.meteomanz.com/sy1?ty=hp&l=1&cou=6216&ind=13274&d1=01&m1=' + month + '&y1=' + year + '&h1=00Z&d2=31&m2=' + month + '&y2=' + year + '&h2=23Z'
            options = webdriver.ChromeOptions()
            # options.add_argument(f"--proxy-server={ip_address}")
            print(year, month)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url=link)
                time.sleep(7)
                # Сохраняем страницу в файл
                file_html = os.path.join("html", "wather" + month + "-" + year + ".html")
                with open(file_html, mode="w", encoding="utf-8") as file:
                    file.write(driver.page_source)
            except Exception as _ex:
                print(_ex)
            finally:
                driver.quit()
            # Проверяем что страница подгрузилась корректно
            items_urls = get_items_urls(file_html)
            if items_urls is not None:
                data += items_urls
            print(data)
    return data


def get_items_urls(url):
    #
    with open(url, 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    table = soup.find('table', {'class': 'data'})
    data = []
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            data.append(cols)
        return data[1:]
    else:
        print('Table not found')

def save_to_csv(data, directory):
    #Сорханяем список в файл
    with open(directory, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

ip_file = 'working_ip.csv'
directory = 'weather_data.csv'

data = get_sourse_html()
csv_data = save_to_csv(data, directory)


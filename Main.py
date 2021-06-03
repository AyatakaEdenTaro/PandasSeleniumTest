import time
import pandas as pd
import datetime
from selenium import webdriver as wb
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs4
import re

class UseSelenium:
    def access_url(self,driver,url,csv_list):
        driver.get(url)
        time.sleep(5)
        elem_buton1 = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div/div[1]/div/span[1]/span/ul/li[2]/div/label/input")
        elem_buton2 = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div/div[1]/div/span[1]/span/ul/li[3]/div/label/input")
        elem_buton3 = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div/div[2]/div[17]/span")
        driver.implicitly_wait(10)
        elem_buton1.click()
        elem_buton2.click()
        elem_buton3.click()
        html = driver.page_source.encode('utf-8')
        soup = bs4(html,"html.parser")
        heading1 = driver.find_element_by_tag_name('h1')
        model = heading1.text
        model_name = model.replace("の店舗在庫","")
        price = soup.findAll("div",{"class":"red"})
        for i in price:
            price_deta =i.text

        stock = soup.findAll("span",{"class":"green"})
        for i in stock:
            stock_deta =i.text

        price_number = re.sub(r"\D", "", price_deta)

        csv_row = []
        csv_row.append(model_name)
        csv_row.append(price_number)
        csv_row.append(stock_deta)

        csv_list.append(csv_row)

class UsePandas:
    def export_csv(self,csv_row):
        today = datetime.date.today()
        df = pd.DataFrame(
            csv_row,
            columns=['商品名','在庫', '価格'])
        df.to_csv("./{deal}.csv".format(deal = today),index = None,mode='a')

list_product = ['https://www.yodobashi.com/ec/product/stock/100000001005798744/',
'https://www.yodobashi.com/ec/product/stock/100000001005815492/',
'https://www.yodobashi.com/ec/product/stock/100000001005653038/',
'https://www.yodobashi.com/ec/product/stock/100000001005431783/',
'https://www.yodobashi.com/ec/product/stock/100000001005431782/',
'https://www.yodobashi.com/ec/product/stock/100000001005431781/',
'https://www.yodobashi.com/ec/product/stock/100000001005644115/',
'https://www.yodobashi.com/ec/product/stock/100000001005644114/',
'https://www.yodobashi.com/ec/product/stock/100000001005644113/']

# クラスの定義
use_selenium = UseSelenium()
use_pandas = UsePandas()

# 出力用CSVリスト
csv_list = []

# ドライバーの設定
#options = Options()
#options.add_argument('--headless')
driver = wb.Firefox(executable_path="./geckodriver-v0.29.1-win64/geckodriver.exe")

# urlにアクセス
for url in list_product:
    use_selenium.access_url(driver,url,csv_list)

# ドライバーの終了
driver.quit()

# CSVファイルに出力
use_pandas.export_csv(csv_list)
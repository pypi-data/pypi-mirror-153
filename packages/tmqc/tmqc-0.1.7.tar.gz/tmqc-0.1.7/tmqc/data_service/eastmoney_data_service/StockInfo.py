# -*- coding: utf-8 -*-
# @Time    : 2018/11/15 14:41
# @Author  : hc
# @Site    : 
# @File    : StockInfo.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup

STOCK_URL= "http://quote.eastmoney.com/stocklist.html" #股票代码查询一览表

class StockInfo():
    def __init__(self):
        self.url =STOCK_URL
    def get_data(self):
        response = requests.get(self.url,)


        self.format(response.content)

    def format(self, rep_data):
        soup = BeautifulSoup(rep_data, "lxml")
        quote_body = soup.select('quote_body')[0]
        print(quote_body)




if __name__ == '__main__':
    stock = StockInfo()
    stock.get_data()
# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import requests
import datetime
import demjson
from functools import partial
from tradeTools import Decorator
import pandas as pd
import numpy as np


STOCK_CODE_PATH = 'stock_codes.conf'
# IDX_STOCKS={
# "HS300":"000300",
# "SZ50":"000016",
# "ZZ500":"000905"
# }

def code_add_prefix(code):
    """给没有前缀的股票代码增加前缀"""
    if isinstance(code, int):
        if code < 999999:
            code = '%06d' % (code)
        else:
            code = '%s' % (code)
               
    if code.startswith('SH.') or  code.startswith('SZ.'):
        return code
    return '%s.%s' % (get_stock_exchange(code), code)

def get_stock_exchange(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90','110'] 为 SH
    ['00', '13', '18', '15','16', '18', '20', '30', '39', '115'] 为 SZ
    ['5', '6', '9'] 开头的为 SH， 其余为 SZ
    :param stock_code:股票ID, 若以 'SZ', 'SH'开头直接返回对应类型，否则使用内置规则判断
    :return 'SH' or'SZ'"""
    if isinstance(stock_code, int) and stock_code < 999999:
        stock_code = '%06d' % (stock_code)
        
    # if stock_code.startswith(('sh', 'sz')) or stock_code.startswith(('SH', 'SZ')):
    #     return stock_code[:2]
    
    if len(stock_code) == 8: # 期权
        if stock_code.startswith('10'):
            return 'SH'
        if stock_code.startswith('90'):
            return 'SZ'
    stock_code = stock_code[-6:]
    if stock_code.startswith(('50', '51', '60', '90', '110', '113', '132', '204')):
        return 'SH'
    if stock_code.startswith(('00', '13', '18', '15', '16', '18', '20', '30', '39','115', '1318')):
        return 'SZ'
    if stock_code.startswith(('5','6', '9', '7')):
        return 'SH'
    return 'SZ'

def get_stock_type(code):
    """
    判断代码是属于那种类型，目前仅支持 ['fund', 'stock']
    :return str 返回code类型, fund 基金 stock 股票
    """
    if code.startswith(('00', '30', '60','688')):
        return 'stock'
    return 'fund'

def get_stock_codes(real_time=False, stock_type=None, with_exchange=False):
    """获取所有股票 ID 到 all_stock_code 目录下
    real_time:是否实时
    stock_type:(fund 基金 stock 股票)
    with_exchange:是否要加上对应的证券市场编码
    """
    if real_time:
        all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
        grep_stock_format = '~(\w+)`([^`]+)`'
        grep_stock_codes = re.compile(grep_stock_format)
        response = requests.get(all_stock_codes_url)
        # 这里对id去重
        stock_codes = list(set(grep_stock_codes.findall(response.text)))
        with open(stock_code_path(STOCK_CODE_PATH), 'w') as f:
            f.write(json.dumps(dict(stock=stock_codes), ensure_ascii=False))
    else:
        with open(stock_code_path(STOCK_CODE_PATH)) as f:
            stock_codes = json.load(f)['stock']

    if stock_type:
        stock_codes = [
            (stock[0],stock[1]) for stock in stock_codes if stock_type == get_stock_type(stock[0])
        ]

    if with_exchange:
        stock_codes = [(code_add_prefix(code[0]), code[1])
                       for code in stock_codes]

    return stock_codes

def get_codes_from_web():
    import requests
    all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
    grep_stock_format = '~(\w+)`([^`]+)`'
    grep_stock_codes = re.compile(grep_stock_format)
    stock_info = []
    try:
        response = requests.get(all_stock_codes_url)
        found_info = grep_stock_codes.findall(response.text)
        stock_info = []
        last = 0
        for e in found_info:
            if e[0] == last:continue
            if not (e[0].startswith('60') or
                    e[0].startswith('30') or
                    e[0].startswith('00') or
                    e[0].startswith('51') or
                    e[0].startswith('15')): continue
            stock_info.append({'code': code_add_prefix(e[0]), 'name': e[1]})
            last = e[0]
    except:
        pass
    return stock_info

def get_stock_codes_exclude_ST():
    all_stock_codes = get_stock_codes(real_time=True, stock_type="stock", with_exchange=False)  # 股票开板或者封板状态
    all_stock_codes = {int(s[0]): s[1] for s in all_stock_codes if
                            s[1].lower().find('st') == -1  # 过滤ST
                            and s[1].lower().find('pt') == -1
                            and s[1].lower().find('退') == -1
                            }  # 过滤ST
    return all_stock_codes

def stock_code_path(STOCK_CODE_PATH):
    if getattr(sys, 'frozen', False):
        pathname = STOCK_CODE_PATH
    else:
        pathname = os.path.join(os.path.dirname(__file__), STOCK_CODE_PATH)
    return pathname

# 方便兼容打包exe
def get_path_dirname():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        # 取当前脚本的上级目录
        application_path = os.path.dirname(os.path.dirname(__file__))
    return application_path

# 回测 读取股票成交记录。提取买入股票清单
def get_buy_list_conf():
    path = ["conf","buy_list.xlsx"]
    path = os.sep.join(path)
    work_dir = get_path_dirname()
    full_path = work_dir + os.sep + path
    buy_list = {}
    import xlrd
    # 1、打开文件
    with xlrd.open_workbook(full_path) as f:
        sheet = f.sheet_by_index(0)
        row_length = sheet.nrows  # 获取行长度
        for i in range(1,row_length): # 过滤第一行标题
            data = sheet.row_values(i)
            _date =  int(data[0])
            code = int(data[2])
            dir = data[4]
            if dir != "证券买入":
                continue
            if _date not in buy_list:
                buy_list[_date] = []
            buy_list[_date].append(code)

    return buy_list

def calc_time_diff(beg, end=None):
    b = datetime.datetime.strptime(str(beg), '%Y%m%d%H%M%S%f')
    if end:
        e = datetime.datetime.strptime(str(end), '%Y%m%d%H%M%S%f')
    else:
        e = datetime.datetime.now()
    seconds_diff = (e - b).total_seconds()
    return seconds_diff

def format_datetime(datetime:str):
    length = len(str(datetime))
    if length == 17:
        return "%s-%s-%s %s:%s:%s.%s" % (
             datetime[:4], datetime[4:6], datetime[6:8], datetime[8:10], datetime[10:12], datetime[12:14], datetime[14:]
        )
    elif length == 9:
        return "%s:%s:%s.%s"% (datetime[0:2],datetime[2:4],datetime[4:6],datetime[6:])
    else:
        return

def debug_data_print(data):
    _datetime = str(data['date']) + "%09d" % data['time']
    diff = calc_time_diff(_datetime)
    print('行情时间[%s]本机时间[%s]股票id[%s]与本机时间间隔[%s]'
          % (format_datetime(_datetime),
             datetime.datetime.now(),
             data['code'],
             diff))


def debug_tran_print(data):
    trade_time = str(data['time'])
    _len = len(trade_time)
    if _len !=17:
        _date = datetime.datetime.now().strftime("%Y%m%d")
        trade_time =_date+ "%09d"%data['time']
    diff = calc_time_diff(trade_time)
    print('成交时间[%s]本机时间[%s]股票id[%06d]与本机时间间隔[%s]'
          % (format_datetime("%09s"%data['time']),
             datetime.datetime.now(),
             int(data['code']),
             diff))

    # 　上市公司季报披露时间：
    # 　　1季报：每年4月1日——4月30日。
    # 　　2季报（中报）：每年7月1日——8月30日。
    # 　　3季报： 每年10月1日——10月31日
    # 　　4季报 （年报）：每年1月1日——4月30日。
    #todo: 年报和一季度报最迟披露时间一致，默认返回年报
def getReportDate(dateTime:int,isUseYear = True):
    # isUseYear:True 返回年报日期 Fasle 返回一季度日期
    mmdd = dateTime % 10000
    year = dateTime // 10000
    dateRange = [1031, 830, 430, ]  # 公布日期

    reportDate = [930, 630, 1231]  if isUseYear else [930, 630, 331,]
    for idx, _dateRange in enumerate(dateRange):
        if mmdd > _dateRange:
            if idx == 2:
                year = year - 1 if isUseYear else year
            return year * 10 ** 4 + reportDate[idx]
    return (year - 1) * 10 ** 4 + reportDate[0]

def getTTmReportDates(reportDate):
    """返回一年滚动需要查询的报告期
        上年同季度日期，上年的年报日期，当季报告期

        如果reportDate是年报日期。则直接返回reportDate
    """
    quarterDate = reportDate % 10 ** 4
    if quarterDate == 1231:
        return [reportDate]
    lastYear = reportDate // 10 ** 4 - 1
    quarterDates = list(set([reportDate % 10 ** 4, 1231]))
    reportDates = [lastYear * 10 ** 4 + q for q in quarterDates]
    reportDates.append(reportDate)
    return reportDates

@Decorator.loadData()
def getSymbolsInfo(isRealTime = False,**kwargs):
    """[生成股票代码，名称，和行业]

    Args:
        isRealTime (bool, optional): [如果为True，会增量添加数据]. Defaults to False.

    Returns:
        [type]: [description]
    """
    fileName = kwargs["fileName"]
    # todo：get_stock_codes 获取全市场股票ID.退市的股票有可能获取不到
    stock_codes = get_stock_codes(real_time=isRealTime, stock_type="stock", with_exchange=True)
    cathchedSymbols = []
    
    if  os.path.exists(fileName):
        df = pd.read_excel(fileName, sheet_name="数据源", index_col=0,engine="openpyxl")
        cathchedSymbols = df["symbol"].tolist()

    symbols = [symbol for symbol,name in stock_codes]
    catchSymbols = list(set(symbols)-set(cathchedSymbols)) # 需要增加的股票
    url = "http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax"
    params = {
        "code":"",
    }
    data = []
    cnt = len(catchSymbols)
    i = 0
    for symbol,name in stock_codes:
        if symbol not in catchSymbols:
            continue
        i+=1
        print(f"{symbol}{name}\t{i}/{cnt}")
    # for symbol,name in [("SZ.300104","乐视")]:
        params["code"] = symbol.replace(".","")
        r = requests.get(url, params=params)
        textData = r.text
        dataJson = demjson.decode(textData)
        if "fxxg" not in dataJson: # 未上市
            continue
        if "ssrq" not in dataJson["fxxg"]: # 未上市
            continue
        listingDate = pd.to_datetime(dataJson["fxxg"]["ssrq"]) if dataJson["fxxg"]["ssrq"].replace("--","") else np.nan
        series = pd.Series({"symbol":symbol,"name":name,"listingDate":listingDate})
        data.append(series)
    if cathchedSymbols:
        df = df.append(pd.DataFrame(data))
    else:
        df = pd.DataFrame(data)
    return df

@Decorator.loadData(path="data")
def getKzzCodes(isRealTime = False,**kwargs)-> pd.DataFrame:
    """获取可转债基础信息
    isRealTime: True 实时抓取 东财网数据  http://data.eastmoney.com/kzz/default.html
    Returns:
        pd.DataFrame: _description_
    """
    import akshare as ak
    
    df = ak.bond_zh_cov()
    df["债券代码"] = df["债券代码"].apply(lambda x:f"SH.{x}" if str(x).startswith("11") else f"SZ.{x}")
    df["正股代码"] = df["正股代码"].apply(lambda x:code_add_prefix(x))
    df = df.set_index("债券代码", verify_integrity=True)
    return df

if __name__ == '__main__':
    df = getKzzCodes(isRealTime = True)
    print(df.dtypes)
    print(df.head())
    # stock_codes = get_stock_codes(real_time=True,stock_type="stock",with_exchange=True)
    # print(stock_codes)

    # # stocks = ["0"+stock_code[0] if get_stock_exchange(stock_code[0])=="sh" else "1"+stock_code[0] for stock_code in stock_codes ]
    # print(stock_codes)
    # print(getReportDate(20120330))
    # print(getReportDate(20120530))
    # print(getReportDate(20120831))
    # print(getReportDate(20121130))
    # print(pow(2.5,1/11))
    # print(getSymbolsInfo(isRealTime=True))
    # print(getSymbolsInfo())
# http://f10.eastmoney.com/CompanySurvey/Index?type=web&code=SZ300104
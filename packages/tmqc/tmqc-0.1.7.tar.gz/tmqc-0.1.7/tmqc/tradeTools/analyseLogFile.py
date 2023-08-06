# -*- coding: utf-8 -*-
# 对策略的回测结果分析
import pandas as pd
import numpy as np
import json
import os
import re
import sys
import requests
import datetime
from  tmqc.common import basefunc
from tmqc.frame import data_center
from tradeTools import DataMgr
from tradeTools import Decorator


CON_NET_VALUE_FILENAME = "stock_day_net_value.log" # 要读取的日志文件名
STRATEGY_PATH_CONF = [os.path.dirname(os.path.dirname(__file__)),"FundFlow"]
STRATEGY_PATH_CONF.append("20150713INDEX_SYMBOL[SH.000905]USE_PRICEclose是否首次突破才买False是否全平[True]是否平均持仓[True]考虑涨跌停True可持仓数量20")
# STRATEGY_PATH_CONF = [os.path.dirname(os.path.dirname(__file__)),"reversal","log_500市值加权"]
# pathCnf = [STRATEGY_PATH, f"{CON_NET_VALUE_FILENAME}.log"]
path = os.sep.join(STRATEGY_PATH_CONF)
full_path = path + os.sep + CON_NET_VALUE_FILENAME
# print(full_path)



class Mgr(DataMgr.Mgr):
    @Decorator.loadData()
    def addIndex(self,frequency = 1):
        df = self.load()
        begTime = df.iloc[0].name # 策略开始时间
        dfs = [df]
        for indexSymbol in ["SH.000300","SH.000905","SH.000001"]:
            idx = self.genIDXData(indexSymbol=indexSymbol, frequency=frequency)
            idx = idx[idx.index >= str(begTime)]
            dfs.append(idx[[indexSymbol]])
        total = pd.concat(dfs, axis=1, join='outer', )
        return total
    
    # df 每日收益率
    @Decorator.loadData()
    def qryAnalyse(self,df,strategy,frequency):
        begTime = df.iloc[0].name # 策略开始时间
        dfs = [df]
        for indexSymbol in ["SH.000300","SH.000905","SH.000001"]:
            idx = self.genIDXData(indexSymbol=indexSymbol, frequency=frequency)
            idx = idx[idx.index >= str(begTime)]
            dfs.append(idx[[indexSymbol]])
        total = pd.concat(dfs, axis=1, join='outer', )

        d = {}
        for name, s in total.items():
            tradeDays = s.size
            # todo:股票k线数据丢失或停牌，会导致收益率均值为0.加权为空，影响占用天数的统计
            keepTradeDays = tradeDays - s.isnull().sum() # 占用天数
            std = s[~s.isnull()].std()
            yearStd = std * pow(252, 0.5)  # 年化标准差

            avg = s[~s.isnull()].mean()
            std = s[s < avg].std()  # 每日收益率标准差
            SDRyearStd = 2* std * pow(252, 0.5)  # #补偿只有基准以下的收益率计算入标准差，需要再将标准差乘以2
            d[name] = [tradeDays,keepTradeDays,yearStd,SDRyearStd]
        ret = pd.DataFrame(d,index=["总天数","实际占用天数","年化标准差","SDR年化标准差"]).T
        total.fillna(0, inplace=True)  # 停牌的日期。收益率为设为0
        totalCumprod = (1 + total).cumprod()
        ret["累计净值"] = totalCumprod.iloc[-1,:].T

        ret["复合年收益率"] = pow(ret["累计净值"],252/ret["总天数"])-1
        ret["夏普率"] = (ret["复合年收益率"]-0.02)/ret["年化标准差"]
        ret["SDR夏普率"] = (ret["复合年收益率"]-0.02)/ret["SDR年化标准差"]

        ret["年收益率_根据实际占用天数"] =pow(ret["累计净值"],252/ret["实际占用天数"])-1
        ret["夏普率_根据实际占用天数"] = (ret["年收益率_根据实际占用天数"]-0.02)/ret["年化标准差"]
        ret["SDR夏普率_根据实际占用天数"] = (ret["年收益率_根据实际占用天数"] - 0.02) / ret["SDR年化标准差"]

        maximumDrawdown = 1-totalCumprod/np.maximum.accumulate(totalCumprod)
        ret["最大回撤"] = maximumDrawdown.max()
        ret["最大回撤日期"] = maximumDrawdown.idxmax()
        return ret
    
    @Decorator.loadData()
    def qryRateByYear(self,df,frequency,indexSymbol,strategyName):
        idx = self.genIDXData(indexSymbol=indexSymbol, frequency=frequency)
        begTime = df.iloc[0].name # 策略开始时间
        endTime = df.iloc[-1].name # 策略结束时间
        idx = idx[(idx.index >= begTime)&(idx.index <= endTime)]
        total = pd.concat([df,idx[[indexSymbol]]], axis=1, join='outer', )
        s = []
        for i ,y  in total.resample("Y"):
            _y = (1 + y).cumprod()
            _s = _y.iloc[-1]-1
            _s.name = i.year
            s.append(_s)
        r = pd.DataFrame(s)
        return r
    
    @Decorator.loadData()
    def qryDayNetValue(self,logName):
        STRATEGY_PATH_CONF = [os.path.dirname(os.path.dirname(__file__)),"FundFlow",logName]
        # LOG_FILE_NAME = [year for year in range(2010,2012)]
        CON_NET_VALUE_FILENAME = "stock_day_net_value {year}.log"  # 要读取的日志文件名
        dfs = []
        for year in range(2010, 2022):
            paths = []
            paths.extend(STRATEGY_PATH_CONF)
            paths.append(str(year))
            paths.append(CON_NET_VALUE_FILENAME.format(year = year))

            path = os.sep.join(paths)
            print(path)
            df = pd.read_csv(path, engine='python', encoding='gb2312', sep='\t',header=None)
            print(df)
            dfs.append(df)
        total  = pd.concat(dfs, axis=0, join='outer', )
        total.columns = ["日期","净值","回撤","上证指数","上证回撤","沪深300","沪深300回撤","上证50","上证50回撤","资产","利润","保证金","手续费","滑点损失"]

        total["每日收益率"] = total["净值"]/total["净值"].shift() -1
        return total
    #     print(max(1-totalCumprod["SH.000300"]/np.maximum.accumulate(totalCumprod["SH.000300"])))
    #     print(idmax(1-totalCumprod["SH.000300"]/np.maximum.accumulate(totalCumprod["SH.000300"])))
    # # def __init__(self):
    #     self.oldDc = data_center.use()
        # self.df = self.load()

    def load(self):
        df = pd.read_csv(full_path,engine='python', encoding='gb2312', sep='\t')
        df['date'] = pd.to_datetime(df['日期'], format='%Y%m%d')
        df.set_index('date', inplace=True)
        df.drop_duplicates( keep='first',inplace=True)
        return df
    #
    # def concat(self):
    #     indexSymbol = "SH.000905"
    #     df = pd.concat([self.df,self.genIDXData()],axis = 1,join="inner")
    #     dateIdx = df[df['净值']!= 1].iloc[0].name # 首次开仓日期
    #     df = df[df.index>=dateIdx].copy()
    #     df["中证500"] = (1 + df[f"{indexSymbol}收益率"]).cumprod()
    #     name = path+os.sep+f"{STRATEGY_PATH_CONF[-1]}.xlsx"
    #     df.to_excel(name, sheet_name="数据源")
# def genYearReport():
#
#     df = df.resample('Y').last()
#     # Index(['日期', '净值', '回撤', '上证指数', '上证回撤', '沪深300', '沪深300回撤', '上证50', '上证50回撤',
#     #        '资产', '利润', '保证金', '手续费', '滑点损失'],
#     #       dtype='object')
#     df.to_excel("年度净值报告 .xlsx", sheet_name="数据源")

if __name__ == '__main__':
    mgr = Mgr()
    CON_FREQUENCY = 1
    CON_INDEX_SYMBOL = "SH.000300"
    # idxDf = mgr.genIDXData(symbol=CON_INDEX_SYMBOL, fileExtension=CON_FREQUENCY)
    # df = mgr.qryDayNetValue(logName="20100424INDEX_SYMBOL[SH.000905]USE_PRICEopen是否首次突破才买False是否全平[True]是否平均持仓[False]考虑涨跌停True可持仓数量99999")
    # mgr.concat()
    print(mgr.qryRateByYear())

# -*- coding: utf-8 -*-
import json
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
from common import basefunc
from common.define import SUBSTITUTE_FLAG
from common import log
from tradeTools import helpers
from re import sub

SETTING = basefunc.get_strategy_setting()
FILENAME= "按照清单净值计算_%s"
class ETF_Info:
    def __init__(self,datetime):
        # self.dc = data_center.use()
        self.etf_infos = self.load(datetime=datetime)
        self.etf_list = self.gen_list()

    # def set_last_datetime(self): # 设置上一个交易日
    #     if self.datetime not in self.dc.trade_days:
    #         last_datetime = self.dc.trade_days[-1]
    #         if last_datetime>=self.datetime:
    #             raise Exception('上一个交易日[{last_datetime}]大于当前交易日[{datetime}]'
    #                             .format(last_datetime= last_datetime,datetime = self.datetime))
    #         return last_datetime
    #     return self.dc.trade_days[self.dc.trade_days.index(self.datetime)-1]

    # 根据成分股的数量从高到低排序。然后分组
    def gen_list(self):
        etf_list = []
        for id2 in self.etf_infos.keys():
            constituent_stocks = self.get_constituent_stock_info(id2)
            cnt = len(constituent_stocks)
            etf_list.append((cnt,id2))
        etf_list.sort(reverse=True)
        res =[[] for i in range(SETTING.GROUP_NUM)]

        for _idx,_ in enumerate(etf_list):
            id2 = _[1]
            idx =_idx%SETTING.GROUP_NUM if _idx//SETTING.GROUP_NUM%2 == 0 else -(_idx %SETTING.GROUP_NUM) - 1
            # idx = _idx % SETTING.GROUP_NUM
            res[idx].append(id2)
        return res

    def load(self,datetime:int):
        self.datetime = datetime
        # self.last_datetime = self.set_last_datetime()

        etf_infos = {}
        path = os.sep.join([basefunc.get_path_dirname(), "conf", "etf",str(datetime // 100)])
        if not os.path.exists(path):
            txt = "不存在该路径{}".format(path)
            print(txt)
            return etf_infos
        full_paths = [os.sep.join([path, "etf_%s_%s.conf" % (market_name,datetime)]) for market_name in ["sh","sz"]]

        for full_path in full_paths:
            if not os.path.exists(full_path):
                print("未找到etf配置路径 ",full_path)
                continue
            with open(full_path) as f:
                obj = json.load(f)
                for fundid2,details in obj.items():
                    constituent_stock_info = {int(stock_id):v for stock_id,v in details["constituent_stock_info"].items()}
                    details["constituent_stock_info"] = constituent_stock_info
                    etf_infos.update({helpers.code_add_prefix(fundid2):details})
            print("读取etf配置路径 ",full_path)
        return etf_infos

    def get_creationRedemptionUnit(self,fundid2)->int:
        """申赎单位(份)"""
        return int(self.etf_infos[fundid2]["creationRedemptionUnit"])

    def get_estimatedCashComponent(self,fundid2)->float:
        """预估现金"""
        # estimatedCashComponent = float(sub(r'[^-?\d.]', '', ))
        return self.etf_infos[fundid2]["estimatedCashComponent"]

    def get_constituent_stock_info(self,fundid2)->dict:
        """成分股"""
        d = {helpers.code_add_prefix(code):info for code,info in self.etf_infos[fundid2]["constituent_stock_info"].items()}
        return d

    def get_idx(self,fundid2)->int:
        """跟踪指数"""
        return int(self.etf_infos[fundid2]["index_id"])
    def getRedemptionUnitAssetValue(self,fundid2)->float:
        """上一个交易日的单位资产净值"""
        return float(self.etf_infos[fundid2]["fRedemptionUnitAssetValue"])

    def get_market_type(self,fundid2)->int: # 十位：（1:沪市 2:深市） 个位（2;跨市）
        """市场类型标志"""
        return int(self.etf_infos[fundid2]["market_type"])

    # def calc_estimatedCashComponent(self,fundid2,fRedemptionUnitAssetValue): # 计算预估现金
    #     """
    #     T日预估现金部分
    #     ＝T-1日最小申购、赎回单位的基金资产净值
    #     －（申购、赎回清单中必须用现金替代的固定替代金额
    #     ＋申购、赎回清单中可以用现金替代成份证券的数量与T日预计开盘价相乘之和
    #     +申购、赎回清单中禁止用现金替代成份证券的数量与T日预计开盘价相乘之和）
    #     """
    #     # 成分股价值
    #     log.WriteLog(FILENAME%self.datetime,"code\t股数\t%s日收盘价\t价值"%self.last_datetime)
    #     sum = 0
    #     for code, v in self.get_constituent_stock_info(fundid2).items():
    #         if v["substituteFlag"] == SUBSTITUTE_FLAG.MUST.value:
    #             sum += v["cashAmount"]
    #             log.WriteLog(FILENAME % self.datetime, f"{code}\t\t\t{v['cashAmount']}")
    #             continue
    #         stock = helpers.code_add_prefix(code)
    #         close, datetime = self.dc.get_nearest_price(stock, self.last_datetime)
    #         if datetime != self.last_datetime:
    #             print("%s 有停牌" % stock)
    #         if self.dc.query_dividend_by_reg_date(stock,datetime):
    #             print("%s 股权登记" % stock)
    #         quantity = v["quantity"]
    #         sum+=close*quantity
    #         log.WriteLog(FILENAME % self.datetime, f"{code}\t{quantity}\t{close}\t{close*quantity}")
    #
    #     estimatedCashComponent = fRedemptionUnitAssetValue - sum
    #     web_estimatedCashComponent = self.get_estimatedCashComponent(fundid2)
    #     log.WriteLog(FILENAME % self.datetime, f"根据股数计算的净值\t{fRedemptionUnitAssetValue}\t-清单净值\t{sum}\t=预估现金{estimatedCashComponent}公告的预估现金{web_estimatedCashComponent}")
    #     return estimatedCashComponent,web_estimatedCashComponent

if __name__ == '__main__':
    etf = ETF_Info(20210621)
    fundid2 ="SZ.159801"
    # print(etf.etf_infos[fundid2])
    # a = etf.calc_estimatedCashComponent(fundid2)
    for i in etf.etf_list:
        print(i)
    # # etf.calc_estimatedCashComponent(fundid2)
    # # print(type(etf.get_estimatedCashComponent(fundid2)))
    # for k,v in etf.get_constituent_stock_info(fundid2).items():
    #     print(k,v)
    # print(etf.get_estimatedCashComponent(fundid2))
    # print(etf.get_estimatedCashComponent(fundid2))
    # print(etf.etf_infos.keys())
    # print(etf.constituent_stock_info)
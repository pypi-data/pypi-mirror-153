# -*- coding: utf-8 -*-
# @Time    : 2017/11/3 15:38
# @Author  : hc
# @Site    :
# @File    : _TradeX.py
# @Software: PyCharm
import ctypes
import pandas as pd
import common.pyetc as pyetc
import datetime
import os
class _TradeX():
    def __init__(self,account_id):
        self.max_num = 60 # 查询历史数据的周期
        self.conf_path = r'..\..\conf\actStock.py'
        self.dll_path = r'.\dll\trade_%s.dll'
        self.account_conf = pyetc.load(self.conf_path).ACCOUNT_INFO[account_id]
        self.dll = self.load_dll()

        self.ClientID = -1
        self.OpenTdx()
        self.ErrInfo = ctypes.create_string_buffer('/0' * 256)

    def load_dll(self):
        dll_filename = self.dll_path%self.account_conf["AccountNo"]
        if os.path.exists(dll_filename):
            return ctypes.windll.LoadLibrary(dll_filename)
        if self.gen_dll():
            return ctypes.windll.LoadLibrary(dll_filename)
        return None
    def gen_dll(self):
        res = self.gen_keyword()
        f = open(self.dll_path%"CCHOGIBI", 'rb')
        file_data = f.read()
        f.close()
        # print filedata[0x1148A8:0x1148B7]
        file_data2 = file_data[:0x1148A9]
        for i in res:
            file_data2+=i
        for cnt in range(15-len(res)):
            file_data2+=chr(00)
        file_data2+=file_data[0x1148B8:]
        f2 = open(self.dll_path%self.account_conf["AccountNo"], 'wb')
        f2.write(file_data2)
        f2.close()
        print("破解文件已完成%s"%(self.dll_path%self.account_conf["AccountNo"]))
        return True
    def gen_keyword(self):
        account_id = self.account_conf["AccountNo"]
        res_account = ""  # 账号的奇数账号
        print("准备生成破解文件。账号：%s 奇数位账号：%s"%(account_id,res_account))
        for i in range(len(account_id)):
            if i % 2 == 0:
                res_account += account_id[i]
        a3 = ctypes.c_uint16()
        a3.value = 0x55E
        result = ""
        for i in res_account:
            a = ord(i)
            b = a3.value >> 0x8
            c = a ^ b
            a3.value = 0x207F * (a3.value + c) - 0x523D
            next_flat = True
            for j in range(65, 91):
                if next_flat:
                    for k in range(90, 64, -1):
                        tmp = 1755 + c - k
                        # print("i:[%s] j[%d] k[%d] a[%s] b[%d] c[%d] a3[%s] tmp[%s]" % (i, j, k, a, b, c, a3, tmp))
                        if (tmp % 26 == 0 and tmp / 26 == j):
                            result += chr(j) + chr(k)
                            next_flat = False
                            break
                else:
                    break
        return result
    def OpenTdx(self):
        return self.dll.OpenTdx()
    def CloseTdx(self):
        return self.dll.CloseTdx()

    def __del__(self):
        # pass
        self.Logoff()
        self.CloseTdx()
    def Logoff(self):
        # Result = ctypes.create_string_buffer('/0' * 1024)
        if self.ClientID!=-1:
            self.dll.Logoff(self.ClientID)
    def Logon(self):
        self.ClientID = self.dll.Logon(self.account_conf["IP"], self.account_conf["Port"], self.account_conf["Version"], self.account_conf["YybID"], self.account_conf["AccountNo"], self.account_conf["TradeAccount"], self.account_conf["JyPassword"], self.account_conf["TxPassword"], self.ErrInfo)
        if self.ClientID == -1:
            print(self.ErrInfo.value.decode("gbk"))
        return self.ClientID

    def _QueryData(self,nCategory):
        Result = ctypes.create_string_buffer('/0' * 1024)
        self.dll.QueryData(self.ClientID, nCategory, Result, self.ErrInfo)  # 查询资金
        if self.ErrInfo.value:
            print(self.ErrInfo.value.decode("gbk"))
            return None
        return Result.value.decode("gbk")

    # nCategory:查询信息的种类，
    # 0:资金
    # 1:股份
    # 2:当日委托
    # 3:当日成交
    # 4:可撤单
    # 5:股东代码
    # ====以下未调试成功
    # 6:融资余额
    # 7:融券余额
    # 8:可融证券
    # 9
    # 10
    # 11
    # 12:可申购新股查询
    # 13:新股申购额度查询
    # 14:配号查询
    # 15:中签查询
    def QueryData(self,nCategory=0):
        res = self._QueryData(nCategory)
        if res:
            res = [_r.split("\t") for _r in  res.split("\n")]
            df = pd.DataFrame(res[1:],columns=res[0])
            return df

    def _QueryHistoryData(self,nCategory, sStartDate, sEndDate):
        sStartDate = str(sStartDate)
        sEndDate = str(sEndDate)
        Result = ctypes.create_string_buffer('/0' * (1024*10240))
        self.dll.QueryHistoryData(self.ClientID,nCategory,sStartDate,sEndDate,Result,self.ErrInfo)
        if self.ErrInfo.value:
            print(self.ErrInfo.value.decode("gbk"))
            return None
        return Result.value.decode("gbk")

    def gen_date_list(self,sStartDate,sEndDate):
        date_list = []
        startDate = datetime.datetime.strptime(sStartDate, '%Y%m%d')
        endDate = datetime.datetime.strptime(sEndDate, '%Y%m%d')
        delta = endDate - startDate
        range_num = delta.days // self.max_num + 1
        _startDate = 0
        for i in range(range_num):
            dt = datetime.timedelta(days=self.max_num)
            _startDate = startDate if not _startDate else _startDate + dt
            _endDate = endDate if i == range_num - 1 else _startDate + dt - datetime.timedelta(days=1)
            date_list.append((_startDate.strftime('%Y%m%d'), _endDate.strftime('%Y%m%d')))
        return date_list
    # nCategory:查询信息的种类，
    # 0:历史委托
    # 1:历史成交
    # 2:交割单
    def QueryHistoryData(self,nCategory,sStartDate,sEndDate):
        # """
        df= pd.DataFrame()
        date_list = self.gen_date_list(sStartDate,sEndDate)
        for _date in date_list:
            res = self._QueryHistoryData(nCategory, _date[0], _date[1])
            if res:
                res = [_r.split("\t") for _r in res.split("\n")]
                # if df.empty:
                # df = pd.DataFrame(res[1:], columns=res[0])

                _df = pd.DataFrame(res[1:], columns=res[0])
                # print("==_df==",_date,_df)
                df = df.append(_df,ignore_index=True)

        return df
        # """

if __name__ == "__main__":
    a = _TradeX("305600050220")
    a.Logon()
    for i in range(0,6):
        r = a.QueryData(i)
        print(r)

    # r = a.QueryHistoryData(1,"20170111","20171111")

    # print(a.ClientID)
    # print(r)




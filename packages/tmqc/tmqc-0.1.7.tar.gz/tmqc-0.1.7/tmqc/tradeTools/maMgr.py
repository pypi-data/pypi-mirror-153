# -*- coding: utf-8 -*-
from frame import data_center
from common import basefunc
import os
import pandas as pd


IDX_FILENAME = [basefunc.get_path_dirname(), "data", "ma", "{symbol}.xlsx"]

# isUp = 0 # 短线上穿长线信号 0表示短在长下
class MaMgr:
    def __init__(self,symbol= "SH.000300"):
        self.df = self.getIdxData(symbol)

    def getIsOpen(self,datetime): # 当日短线是否在长线上方
        isOpen = self.df.loc[datetime,"isOpen"]
        return isOpen

    def isDnCross(self,datetime): # 是否是死叉
        isOpen = self.getIsOpen(datetime)
        if isOpen: # 如果当日是短在上
            return False
        idx = self.df.index.tolist().index(datetime)
        if idx == 0:
            return False
        preDatetime = self.df.index.tolist()[idx-1]
        if self.getIsOpen(preDatetime): # 如果昨日短在上
            return True

    def getIdxData(self,symbol):
        fileName = os.sep.join(IDX_FILENAME)
        fileName = fileName.format(symbol = symbol)
        if not os.path.exists(fileName):
            self.datacenter = data_center.use()
            maShort = 100
            maLong = 200  # 均线指标
            beg_date = 20081231
            beg_date_idx = self.datacenter.trade_days.index(beg_date)
            beg_ma_day = self.datacenter.trade_days[beg_date_idx - maLong + 1]
            conn = self.datacenter.database.conn
            sql = "select time as date,code as '代码',close as '收盘价' from index_day_data where code ='%s' and time >=%s" % \
                  (symbol, beg_ma_day)
            df = pd.read_sql(sql, conn)

            for maDay in [maShort,maLong]:
                maColName = "ma" + str(maDay)
                df[maColName] = df["收盘价"].rolling(maDay).mean()

            def _calc(hang):  # 计算收盘价是否在当日50日均线下方
                # global isUp  # 是否上穿
                # close = hang["收盘价"]
                _maShort = hang["ma" + str(maShort)]
                _maLong = hang["ma" + str(maLong)]

                if _maShort>_maLong:
                    return 1
                return 0

            df["isOpen"] = df.apply(_calc, axis=1)
            df = df.set_index(["date"])
            df = df.dropna(axis=0)  # 删除带空值得行

            df.to_excel(fileName, sheet_name="指数数据")
            print("生成指数数据清单完成")

        else:
            df = pd.read_excel(fileName, sheet_name="指数数据", index_col=0)
            print("加载指数数据清单完成")

        return df

if __name__ == '__main__':
    obj = MaMgr("SH.000001")
    df = obj.getIsOpen(20190404)
    print(df)
    df = obj.getIsOpen(20200723)
    print(df)
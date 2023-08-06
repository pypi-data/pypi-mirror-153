from dataclasses import dataclass

import ts_Def as Def
import _stock_load as lib


class StockLoad:
#public:
    # 构造
    def __init__(self):
        self.c = lib.StockLoad()
        self.li = lib.Info()
        self.li2 = lib.Info2()
        self.lis2 = []

#public:
    # 设置加载起始路径
    def SetPath(self, path:str):
        self.c.SetPath(path)

    # 开始加载 yyyymmdd
    def BeginLoad(self, begin:int, end:int):
        self.c.BeginLoad(begin, end)

    # 获取一个信息
    def Get(self, si:Def.Info) -> bool:
        
        bGet = self.c.Get(self.li)
        if bGet:
            si.date = self.li.date
            si.time = self.li.time
            si.type = self.li.type
            si.mk   = self.li.mk
            si.code = self.li.code
            si.open = self.li.open
            si.high = self.li.high
            si.low  = self.li.low
            si.close= self.li.close
            si.volume = self.li.volume

        return bGet

    # 获取一个信息
    def Get2(self, si:Def.Info) -> bool:
        
        bGet = self.c.Get2(self.li2)
        if bGet:
            si.date = self.li2.date
            si.time = self.li2.time
            si.type = self.li2.type
            si.mk   = self.li2.mk
            si.code = self.li2.code
            si.open = self.li2.open
            si.high = self.li2.high
            si.low  = self.li2.low
            si.close= self.li2.close
            si.volume = self.li2.volume

        return bGet        

    # 获取一日信息
    def GetDay(self, sis) -> bool:
        sis.clear()
        bGet = self.c.GetDay(self.lis2)
        if bGet:
            sis.extend(self.lis2)
            self.lis2.clear()

        return bGet

    # 获取一日信息
    def GetDay2(self) -> bool:
        self.c.GetDay(self.lis2)
        return self.lis2

    # 是否获取完毕
    def IsOver(self) -> bool:
        return self.c.IsOver();    
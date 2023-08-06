# -*- coding: utf-8 -*-
import sys
from concurrent import futures
import grpc
from google.protobuf.json_format import MessageToJson
from functools import wraps
sys.path.append("./")
import indexData_pb2,indexData_pb2_grpc
import time
# from common import
import json

import pandas as pd
import os
# 装饰函数 记录请求和返回的参数
def a_decorator_passing_arguments(function_to_decorate):
    @wraps(function_to_decorate)
    def a_wrapper_accepting_arguments(*arg,**kwargs):
        sFuncName = function_to_decorate.__name__
        pbReq = arg[1]        # 获取pd对象  arg[0]: 对应self，arg[1] 对于服务端方法的request参数
        jsonReq = MessageToJson(pbReq)
        sReq = f"[{sFuncName}]\t[Request]{str(jsonReq)}"
        print(sReq)
        pbRsp =  function_to_decorate(*arg,**kwargs)
        jsonRsp = MessageToJson(pbRsp)
        sRsp = f"[{sFuncName}]\t[Response]{str(jsonRsp)}"
        print(sRsp)
        return pbRsp
    return a_wrapper_accepting_arguments

# 接口方法返回对象
class IndexDataServicer(indexData_pb2_grpc.indexDataServicer):
    @a_decorator_passing_arguments
    def sayHello(self, request, context):
        return indexData_pb2.JSONResponse(sRsp='Hello, %s!' % request.sReq)

    @a_decorator_passing_arguments
    def getSymbols(self, request, context):
        req = request.sReq
        req = json.loads(req)
        dateTime = req["dateTime"]
        indexID = req["indexID"]
        idxData = indexData()
        symbols = idxData.getSymbols(dateTime = dateTime,indexID = indexID)
        rsp = indexData_pb2.Symbols()
        for symbol in symbols:
            # 由于是基本数据类型，这儿就不需要实例化了，直接追加数据即可
            rsp.symbol.append(symbol)
        return rsp


class indexData:
    def __init__(self):
        self.indexDF = pd.DataFrame()

    def load(self,indexID = "000300"):
        fileName = os.sep.join([r"data", "index", f"{indexID}指数成分股数据.xlsx"])  #
        df = pd.read_excel(fileName, sheet_name="Sheet", index_col=0)
        df.sort_index(ascending=True, inplace=True)
        df['date'] = pd.to_datetime(df.index, format='%Y-%m-%d')
        df.set_index('date', inplace=True)
        self.indexDF = df

    def getSymbols(self,dateTime,indexID = "000300"):
        if self.indexDF.empty:
            self.load(indexID = indexID)
        df = self.indexDF.iloc[self.indexDF.index <= str(dateTime)]
        symbols =[]
        for index, row in df.iterrows():
            symbol = row["代码"][-2:] + "."+ row["代码"][:6]
            addOrDel = row[r"纳入/剔除"]
            if addOrDel == "纳入":
                symbols.append(symbol)
            elif addOrDel == "剔除":
                symbols.remove(symbol)
            else:
                print(f"纳入/剔除 列的值错误 #{addOrDel}#" )
        return symbols

def server():
    PORT = 50052  # 端口号
    _ONE_DAY_IN_SECONDS = 100
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    try:
        indexData_pb2_grpc.add_indexDataServicer_to_server(IndexDataServicer(), server)

        server.add_insecure_port('[::]:{}'.format(PORT))
        print("add_insecure_port {}".format(PORT))
        server.start()
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    # log.set_log_mode("a")
    # log.set_log_rotating(True)
    # log.set_log_time_prifix(True)


    import threading
    t = threading.Thread(target=server, name='newThread')
    t.start()


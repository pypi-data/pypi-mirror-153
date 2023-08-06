# -*- coding: utf-8 -*-
# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time
import logging
import json
import grpc

import tradex_pb2
import tradex_pb2_grpc

from stock_tools.TradeX import _TradeX as TradeX


_ONE_DAY_IN_SECONDS = 1
# ACCOUNT = "35212133"
# PW = "159159"
ACCOUNT = "8660001779"
PW = "188188"
TOKEN = "WQiOiJLNzFVOERCUE5FIiw"

# 用于验证客户端的请求是否合法
def isAuth(token):

    if token == TOKEN:
        return True

class TradeXServicer(tradex_pb2_grpc.TradeXServicer):

    def SayHello(self, request, context):
        rqt_param = json.loads(request.rqt_string)
        if not isAuth(rqt_param["token"]):
            return json.dumps({"status": -1, "err_text": "非法访问"})
        return tradex_pb2.HelloReply(message='Hello, %s!' % rqt_param["name"])


    def GetPos(self, request, context):
        rqt_param = json.loads(request.rqt_string)
        if not isAuth(rqt_param["token"]):
            return json.dumps({"status": -1, "err_text": "非法访问"})
        tdx = TradeX._TradeX(ACCOUNT)
        tdx.open_Tdx()
        client_Id, e = tdx.logon(PW)
        json_response = tradex_pb2.JSONResponse()
        if e :
            json_response.rsp_string = json.dumps({"status":-1,"err_text":e})
            return json_response
        pos =  tdx.get_stock_positions()
        json_response.rsp_string=json.dumps({"status":0,"res":pos})
        return json_response

    def GetOrders(self, request, context):
        rqt_param = json.loads(request.rqt_string)
        if not isAuth(rqt_param["token"]):
            return json.dumps({"status": -1, "err_text": "非法访问"})
        tdx = TradeX._TradeX(ACCOUNT)
        tdx.open_Tdx()
        client_Id, e = tdx.logon(PW)
        json_response = tradex_pb2.JSONResponse()
        if e :
            json_response.rsp_string = json.dumps({"status":-1,"err_text":e})
            return json_response
        orders = tdx.get_Orders()
        json_response.rsp_string=json.dumps({"status":0,"res":orders})
        return json_response

    def SendOrder(self, request, context):
        rqt_param = json.loads(request.rqt_string)
        if not isAuth(rqt_param["token"]):
            return json.dumps({"status": -1, "err_text": "非法访问"})
        tdx = TradeX._TradeX(ACCOUNT)
        tdx.open_Tdx()
        client_Id, e = tdx.logon(PW)
        json_response = tradex_pb2.JSONResponse()
        if e :
            json_response.rsp_string = json.dumps({"status":-1,"err_text":e})
            return json_response

        order_param  = rqt_param["order_param"]
        print(type(order_param))
        r, e = tdx.SendOrder(order_param["nOrderType"], order_param["nCategory"], order_param["stock_code"], order_param["issue_price"], order_param["apply_cnt"])
        if e:
            json_response.rsp_string = json.dumps({"status": -1, "err_text": e})
            return json_response
        json_response.rsp_string=json.dumps({"status":0,"res":r})
        return json_response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tradex_pb2_grpc.add_TradeXServicer_to_server(TradeXServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()

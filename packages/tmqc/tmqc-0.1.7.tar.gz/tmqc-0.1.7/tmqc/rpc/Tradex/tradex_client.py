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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

from rpc.Tradex import  tradex_pb2
from rpc.Tradex import  tradex_pb2_grpc
import json
TOKEN = "WQiOiJLNzFVOERCUE5FIiw"
HOST = "106.75.213.173:50051"

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(HOST) as channel:
        stub = tradex_pb2_grpc.TradeXStub(channel)
        rqt_string = json.dumps({"token": TOKEN,
                                 "name": 'hanc',})
        # SayHello
        print("test rpcfunc SayHello")
        response = stub.SayHello(tradex_pb2.JSONRequest(rqt_string=rqt_string))
        print(response.rsp_string)

        print("test rpcfunc GetPos")
        rqt_string = json.dumps({"token": TOKEN,
                                 })
        response = stub.GetPos(tradex_pb2.JSONRequest(rqt_string=rqt_string))
        print(response.rsp_string)

    print("test rpcfunc GetOrders")
    orders = get_orders()
    print(orders)


    nCategory= 0 # 0买入, 1卖出
    nOrderType = 0 # 0限价委托； 上海限价委托 / 深圳限价委托
    stock_code="000001"
    issue_price=float(10.27)
    apply_cnt =1000000

    print("test SendOrder GetOrders")
    res = send_order(nCategory, nOrderType, stock_code, issue_price, apply_cnt)
    print(res)



def get_orders():
    with grpc.insecure_channel(HOST) as channel:
        stub = tradex_pb2_grpc.TradeXStub(channel)
        rqt_string = json.dumps({"token": TOKEN,
                                 "name": 'hanc',})
        orders = stub.GetOrders(tradex_pb2.JSONRequest(rqt_string=rqt_string))
        d = json.loads(orders.rsp_string)
        if d["status"] == -1:
            print(d["err_text"])
            return
        return d["res"]

 # nCategory= 0 # 0买入, 1卖出
 #nOrderType = 0 # 0限价委托； 上海限价委托 / 深圳限价委托
 #stock_code="000001"
 #issue_price=float(10)
 #apply_cnt =100

def send_order( nCategory, nOrderType, stock_code, issue_price, apply_cnt):
    with grpc.insecure_channel(HOST) as channel:
        stub = tradex_pb2_grpc.TradeXStub(channel)
        rqt_string = json.dumps({"token": TOKEN,
                                 "order_param": {"stock_code": stock_code,
                                                 "nCategory": nCategory,
                                                 "nOrderType": nOrderType,
                                                 "issue_price": issue_price,
                                                 "apply_cnt": apply_cnt,
                                                 }}

                                )
        res = stub.SendOrder(tradex_pb2.JSONRequest(rqt_string=rqt_string))

        d = json.loads(res.rsp_string)
        if d["status"] == -1:
            print(d["err_text"])
            return d["err_text"]
        return d["res"]


if __name__ == '__main__':
    logging.basicConfig()
    run()
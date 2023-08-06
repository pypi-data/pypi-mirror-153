# -*- coding: utf-8 -*-
import grpc
import sys
sys.path.append("./")
import indexData_pb2,indexData_pb2_grpc
from google.protobuf.json_format import MessageToJson
import json
import better_exceptions

better_exceptions.hook()

HOST = "localhost"
PORT = 50051
# HOST = "120.78.165.177:50051"
def run():
    with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
        stub = indexData_pb2_grpc.indexDataStub(channel)
        sReq = json.dumps({
                                 "name": 'hanc',})
        print("=====测试欢迎函数==========")
        response = stub.sayHello(indexData_pb2.JSONRequest(sReq=sReq))
        print(response)
        print("=====测试getSymbols==========")
        sReq = json.dumps({
            "indexID": '000300', "dateTime":"20180501"})
        response = stub.getSymbols(indexData_pb2.JSONRequest(sReq=sReq))
        jsonRsp = MessageToJson(response)
        jsonRsp = json.loads(jsonRsp)
        return jsonRsp["symbol"]

if __name__ == '__main__':
    # logging.basicConfig()
    run()
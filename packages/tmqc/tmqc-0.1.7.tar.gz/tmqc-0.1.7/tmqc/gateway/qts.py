# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 11:26
# @Author  : hc
# @Site    :
# @File    : qts.py
# @Software: PyCharm
#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import sys
import time
import struct
import datetime
import threading

from twisted.internet import defer, reactor
from stompest.config import StompConfig
from stompest.async import Stomp
from stompest.async.listener import SubscriptionListener
from common import log


def log_w(str_text):
    stime = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S.%f")
    day = datetime.datetime.now().strftime("%Y%m%d")
    str_text = stime + "\t" + str_text
    print(str_text)
    log.WriteLog(day + "_qts_Trace", str_text)


def log_e(str_text):
    stime = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S.%f")
    day = datetime.datetime.now().strftime("%Y%m%d")
    str_text = stime + "\t" + str_text
    print(str_text)
    log.WriteLog(day + "_qts_err", str_text)


user = os.getenv('ACTIVEMQ_USER') or 'admin'
password = os.getenv('ACTIVEMQ_PASSWORD') or 'password'
host_backup = os.getenv('ACTIVEMQ_HOST') or '39.108.169.211'
host1 = os.getenv('ACTIVEMQ_HOST') or '39.108.169.211'
port = int(os.getenv('ACTIVEMQ_PORT') or 61613)
destination = {
    "quotation": r'/topic/Quotation1',  # 行情地址
    "tran_sh": r'/topic/sh1',            # 上海逐笔成交
    "tran_sz": r'/topic/sz1',            # 深圳逐笔成交
    "orders": r'/topic/orders1',         # 逐笔委托，只有深圳
}


PACK_TYPE_BYTE = 2
PACK_TYPE_SHORT = 3
PACK_TYPE_INT = 4
PACK_TYPE_LONG = 5
PACK_TYPE_FLOAT = 6
PACK_TYPE_DOUBLE = 7
PACK_TYPE_STRING = 8
PACK_TYPE_BYTES = 9


class stream_reader(object):
    def __init__(self, data):
        self.index = 0
        self.data = data

    def isEnd(self):
        return self.index >= len(self.data)

    def read(self, type, length=0):
        value = None
        if type == PACK_TYPE_BYTE:
            value, = struct.unpack("<B", self.data[self.index:self.index + 1])
            self.index += 1
        elif type == PACK_TYPE_SHORT:
            value, = struct.unpack("<H", self.data[self.index:self.index + 2])
            self.index += 2
        elif type == PACK_TYPE_LONG:
            value, = struct.unpack("<q", self.data[self.index:self.index + 8])
            self.index += 8
        elif type == PACK_TYPE_INT:
            value, = struct.unpack("<I", self.data[self.index:self.index + 4])
            self.index += 4
        elif type == PACK_TYPE_FLOAT:
            value, = struct.unpack("<f", self.data[self.index:self.index + 4])
            self.index += 4
        elif type == PACK_TYPE_DOUBLE:
            value, = struct.unpack("<d", self.data[self.index:self.index + 8])
            self.index += 8
        elif type == PACK_TYPE_STRING:
            value, = struct.unpack("<%ds" %
                                   length, self.data[self.index:self.index + length])
            self.index += length
        elif type == PACK_TYPE_BYTES:
            length, = struct.unpack("<H", self.data[self.index:self.index + 2])
            self.index += 2
            value, = struct.unpack("<%ds" %
                                   length, self.data[self.index:self.index + length])
        return value

def read_quo10(s):
    data = {}
    data["code"] = '%06d' % s.read(PACK_TYPE_INT)
    data["date"] = s.read(PACK_TYPE_INT)
    data["JTlocaltime"] = s.read(PACK_TYPE_INT)
    data["local_time"] = s.read(PACK_TYPE_INT)
    data["time"] = s.read(PACK_TYPE_INT)
    data["last_price"] = round(s.read(PACK_TYPE_FLOAT), 2)
    data["open_price"] = round(s.read(PACK_TYPE_FLOAT), 2)
    data["high_price"] = round(s.read(PACK_TYPE_FLOAT), 2)
    data["low_price"] = round(s.read(PACK_TYPE_FLOAT), 2)
    data["pre_close_price"] = round(s.read(PACK_TYPE_FLOAT), 2)
    for i in range(1, 11):
        data["buy_price%02d" % i] = round(s.read(PACK_TYPE_FLOAT), 2)
    for i in range(1, 11):
        data["buy_volume%02d" % i] = s.read(PACK_TYPE_INT)
    for i in range(1, 11):
        data["sell_price%02d" % i] = round(s.read(PACK_TYPE_FLOAT), 2)
    for i in range(1, 11):
        data["sell_volume%02d" % i] = s.read(PACK_TYPE_INT)
    data["up_limit"] = s.read(PACK_TYPE_FLOAT)
    data["down_limit"] = s.read(PACK_TYPE_FLOAT)
    flag = s.read(PACK_TYPE_STRING, 8)  # SecurityPhaseTag
    status = s.read(PACK_TYPE_STRING, 8)  # TradeStatus只适用上交所
    data['flag'] = 0  # todo 按需要解析
    data['status'] = 0
    return data


class Listener(object):
    def __init__(self, strategy=None, active_subscribe=None):
        self.strategy = strategy
        self.client = None
        self.count = 0                              # 接受数据条数计数 用于显示
        self.active_subscribe = active_subscribe    # 需要订阅的接口
        self.subscribe_conf = {                     # 回调函数
            "quotation": self.handleFrame,          # 行情地址
            "tran_sh": self.handleFrame_tran_sh,    # 上海逐笔成交
            "tran_sz": self.handleFrame_tran_sz,            # 深圳逐笔成交
            "orders": self.handleFrame_order,         # 逐笔委托，只有深圳
        }

    def load_subscribe(self):
        for idx, _topic in enumerate(self.active_subscribe):
            print(idx, _topic)
            self.client.subscribe(
                destination[_topic],
                listener=SubscriptionListener(
                    self.subscribe_conf[_topic]),
                headers={
                    'ack': 'auto',
                    'id': "han"+str(idx),


                })
            log_text = "  订阅  %s " % destination[_topic]
            print(log_text)
            log_w(log_text)
        # self.client.subscribe('/topic/Quotation', listener=SubscriptionListener(self.handleFrame),
        #                  headers={'ack': 'auto', 'id': 'required-for-STOMP-1.1'})

    @defer.inlineCallbacks
    def handleFrame1(self, client, frame):
        # print(self.count)
        self.count += 1
        if self.count % 10 == 0:
            print(self.count, frame.body)
        if self.count == 100000:
            self.stop(client)
    @defer.inlineCallbacks
    def run(self):
        try:
            self.strategy.startup()  # 策略当天初始化
            """
            config = StompConfig(
                'failover:(tcp://%s:%d,tcp://%s:%d)?randomize=false,startupMaxReconnectAttempts=-1,startupMaxReconnectAttempts=-1,priorityBackup=true' %
                (host1, port,host_backup, port), login=user, passcode=password, version='1.1')
            self.client = Stomp(config)
            # yield self.client.connect(headers = {"client-id":"hancheng"})
            yield self.client.connect(host='mybroker')
            """
            config = StompConfig(
                'failover:(tcp://%s:%d,tcp://%s:%d)?randomize=false,startupMaxReconnectAttempts=-1,startupMaxReconnectAttempts=-1,priorityBackup=true' %
                (host1, port, host1, port), login=user, passcode=password, version='1.1')
            self.client = Stomp(config)
            a = yield self.client.connect(host='mybroker',headers = {"client-id":"hancheng_mac_qts_quo"})
            print(a)
            self.count = 0
            start = time.time()
            print(start)

            self.load_subscribe()
        except Exception as e:
            log_e("[FUNC_name]%s\t" % sys._getframe().f_code.co_name + str(e))


    
    @defer.inlineCallbacks
    def handleFrame(self, client, frame):
        self.count += 1
        s = stream_reader(frame.body)
        while not s.isEnd():
            # data = {}
            # data["symbol"] = s.read(PACK_TYPE_INT)  # 证券代码
            # data["date"] = s.read(PACK_TYPE_INT)  # date:交易日期
            # data["JTlocaltime"] = s.read(PACK_TYPE_INT)  # 津泰采集时间
            # data["localTime"] = s.read(PACK_TYPE_INT)  # locatTime:接收时间
            # data["time"] = s.read(PACK_TYPE_INT)   # time:真实数据生成时间
            # data["last_price"] = s.read(PACK_TYPE_DOUBLE)
            # data["open_price"] = s.read(PACK_TYPE_DOUBLE)
            # data["high_price"] = s.read(PACK_TYPE_DOUBLE)
            # data["low_price"] = s.read(PACK_TYPE_DOUBLE)
            # data["pre_close_price"] = s.read(PACK_TYPE_DOUBLE)
            # data["buy_price1"] = s.read(PACK_TYPE_DOUBLE)
            # data["buy_volume1"] = s.read(PACK_TYPE_LONG)
            # data["sell_price1"] = s.read(PACK_TYPE_DOUBLE)
            # data["sell_volume1"] = s.read(PACK_TYPE_LONG)
            # data["uplimit"] = s.read(PACK_TYPE_DOUBLE)
            # data["downlimit"] = s.read(PACK_TYPE_DOUBLE)
            # data["flag"] = s.read(PACK_TYPE_STRING, 8)  # SecurityPhaseTag
            # data["status"] = s.read(PACK_TYPE_STRING, 8)  # TradeStatus只适用上交所

            data = read_quo10(s)
            if self.strategy:
                self.strategy.on_tick(data)

    @defer.inlineCallbacks
    def handleFrame_order(self, client, frame):
        self.count += 1
        s = stream_reader(frame.body)
        while not s.isEnd():
            data = {}
            data["set_id"] = s.read(PACK_TYPE_INT)
            data["rec_id"] = s.read(PACK_TYPE_LONG)
            data["code"] = s.read(PACK_TYPE_INT)
            data["order_time"] = s.read(PACK_TYPE_LONG)
            data["order_price"] = s.read(PACK_TYPE_DOUBLE)
            data["order_volume"] = s.read(PACK_TYPE_DOUBLE)
            data["order_code"] = s.read(PACK_TYPE_BYTE)
            data["reverse1"] = s.read(PACK_TYPE_BYTE)
            data["order_type"] = s.read(PACK_TYPE_BYTE)
            data["reverse2"] = s.read(PACK_TYPE_BYTE)
            if self.strategy:
                self.strategy.on_order(data)

    @defer.inlineCallbacks
    def handleFrame_tran_sz(self, client, frame):
        s = stream_reader(frame.body)
        while not s.isEnd():
            data = {}
            data["set_id"] = s.read(PACK_TYPE_INT)         #     频道代码
            data["rec_id"] = s.read(PACK_TYPE_LONG)        #     消息记录号 从 1 开始计数，同一频道连续。
            data["buy_order_id"] = s.read(PACK_TYPE_LONG) #     买方委托索引：从 1 开始计数,0 表示无对应委托。
            data["sel_order_id"] = s.read(PACK_TYPE_LONG) #     卖方委托索引：从 1 开始计数,0 表示无对应委托。
            data["code"] = s.read(PACK_TYPE_INT)
            data["trade_time"] = s.read(PACK_TYPE_LONG)
            data["trade_price"] = s.read(PACK_TYPE_DOUBLE)
            data["trade_volume"] = s.read(PACK_TYPE_DOUBLE)
            data["trade_type"] = s.read(PACK_TYPE_BYTE)   #     ASCII码 成交类别：4=撤销，主动或自动撤单执行报告；F=成交，成交执行报告。
            data["res"] = s.read(PACK_TYPE_BYTE)
            if self.strategy:
                self.strategy.on_tran_sz(data)

    @defer.inlineCallbacks
    def handleFrame_tran_sh(self, client, frame):
        s = stream_reader(frame.body)
        while not s.isEnd():
            data = {}
            data["trade_channel"] = s.read(PACK_TYPE_INT)  # 成交通道
            data["rec_id"] = s.read(PACK_TYPE_INT)         #    业务索引
            data["buy_order_id"] = s.read(PACK_TYPE_LONG)    #    买方订单号
            data["sel_order_id"] = s.read(PACK_TYPE_LONG)      #  卖方订单号
            data["code"] = s.read(PACK_TYPE_INT)
            data["trade_time"] = s.read(PACK_TYPE_INT)
            data["trade_price"] = s.read(PACK_TYPE_DOUBLE)
            data["trade_volume"] = s.read(PACK_TYPE_INT)
            data["buysell_flag"] = s.read(PACK_TYPE_BYTE) #  ASCII码 B–外盘,主动买；S –内盘,主动卖；N – 未知。
            data["res"] = s.read(PACK_TYPE_BYTE)
            if self.strategy:
                self.strategy.on_tran_sh(data)

    @defer.inlineCallbacks
    def stop(self):
        print('Disconnecting. Waiting for RECEIPT frame ...',)
        yield self.client.disconnect(receipt='bye')
        print('ok')
        print('Received %s frames' % (self.count))

# 计算时间的秒数差距
def calc_diff_time(beg,end=None):
    b = datetime.datetime.strptime(str(beg), "%Y%m%d%H%M%S%f")
    if end:
        e = datetime.datetime.strptime(str(end), "%Y%m%d%H%M%S%f")
    else:
        e = datetime.datetime.now()
    seconds_diff = (e - b).total_seconds()
    return seconds_diff

class tst_t:
    def __init__(self):
        self.name = "测试策略"
        self.cnt = 0
        self.total = 10  # 达到累计数时打印一条

    def startup(self):
        pass
    def on_tick(self, tick):

        self.cnt += 1
        # print(self.cnt,tick)
        if (self.cnt % self.total == 0):
            _time = tick["time"]
            _date = int(datetime.datetime.now().strftime('%Y%m%d'))
            _datetime = str(_date) + str(_time)
            diff = calc_diff_time(_datetime)
            print("行情时间[%s]qts接收时间[%s]本机时间[%s]股票id[%s]与本机时间间隔[%s]"
                  % (_datetime,
                     tick["local_time"],
                     datetime.datetime.now(),
                     tick["code"]
                     , diff))

    def on_order(self, tick):
        self.cnt += 1
        if (self.cnt % self.total == 0):
            print("on_order", tick)

    def on_tran_sz(self, tick):
        self.cnt += 1
        if (self.cnt % self.total == 0):
            print("on_tran_sz", tick)

    def on_tran_sh(self, tick):
        self.cnt += 1
        if (self.cnt % self.total == 0):
            print("on_tran_sh", tick)


if __name__ == '__main__':
    DAY_START = datetime.time(9, 10)  # 日盘启动和停止时间
    DAY_END = datetime.time(23, 30)
    # DAY_START1 = datetime.time(10,7)  # 日盘启动和停止时间
    # DAY_END1 = datetime.time(15, 30)
    # quotation
    # tran_sh
    # tran_sz
    # orders
    # import Strategy_Limit_UP
    sub_list = ("quotation","tran_sh","tran_sz","orders")
    # listener = Listener(Strategy_Limit_UP.Strategy_Limit_UP(), sub_list)
    try:
        # sub_list = ("quotation",)

        #from gateway import listener
        #ltn = listener.Listener()
        ltn = Listener(tst_t(), sub_list)
        ltn.run()
    except Exception as e:
        print(e)
    pass
    """
    def action(listener):
        p = False  # 定时器线程。用来控制关闭
        while True:
            print("111")
            recording = False
            # weekday = datetime.datetime.now().weekday()
            currentTime = datetime.datetime.now().time()
            # 判断当前处于的时间段
            if currentTime >= DAY_START and currentTime <= DAY_END:
                recording = True

            print("是否为交易时间[%s]" % recording)
            # 记录时间则需要启动子进程
            print('[%s] 定时器线程 name is:%s\r' %
                  (currentTime, threading.currentThread().getName()))
            # print(listener.client.session)
            if recording and not p:
                ltn.run()
                p = True
            if not recording and p:
                ltn.stop()
                p = False
            time.sleep(20)
    p = threading.Thread(target=action, args=(ltn,))
    p.start()
    """
    reactor.run()




import os
import struct
import lzma

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
            value, = struct.unpack("<B", self.data[self.index:self.index+1])
            self.index += 1
        elif type == PACK_TYPE_SHORT:
            value, = struct.unpack("<H", self.data[self.index:self.index+2])
            self.index += 2
        elif type == PACK_TYPE_LONG:
            value, = struct.unpack("<q", self.data[self.index:self.index+8])
            self.index += 8
        elif type == PACK_TYPE_INT:
            value, = struct.unpack("<I", self.data[self.index:self.index+4])
            self.index += 4
        elif type == PACK_TYPE_FLOAT:
            value, = struct.unpack("<f", self.data[self.index:self.index+4])
            self.index += 4
        elif type == PACK_TYPE_DOUBLE:
            value, = struct.unpack("<d", self.data[self.index:self.index+8])
            self.index += 8
        elif type == PACK_TYPE_STRING:
            value, = struct.unpack("<%ds" % length, self.data[self.index:self.index+length])
            self.index += length
        elif type == PACK_TYPE_BYTES:
            length, = struct.unpack("<H", self.data[self.index:self.index+2])
            self.index += 2
            value, = struct.unpack("<%ds" % length, self.data[self.index:self.index+length])

        return value

def read_shtran_file(c):
    s = stream_reader(c)
    while not s.isEnd():
        data = {}
        data["tradeChannel"] = s.read(PACK_TYPE_INT)
        data["rec_id"] =  s.read(PACK_TYPE_INT)
        data["buy_rec_id"] = s.read(PACK_TYPE_LONG)
        data["sel_rec_id"] = s.read(PACK_TYPE_LONG)
        data["code"] = s.read(PACK_TYPE_INT)
        data["trade_time"] = s.read(PACK_TYPE_INT)
        data["trade_price"] = s.read(PACK_TYPE_DOUBLE)
        data["trade_volume"] = s.read(PACK_TYPE_INT)
        data["buySellFlag"] = s.read(PACK_TYPE_BYTE)
        data["res"] = s.read(PACK_TYPE_BYTE)
        yield data

def read_tran_file(c):
    s = stream_reader(c)
    head = s.read(PACK_TYPE_STRING,4)
    v1 = s.read(PACK_TYPE_BYTE)
    v2 = s.read(PACK_TYPE_BYTE)
    while not s.isEnd():
        data = {}
        data["code"] = s.read(PACK_TYPE_INT)
        data["set_id"] =  s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_INT)
        data["JT_time"] = s.read(PACK_TYPE_INT)
        data["rec_id"] =  s.read(PACK_TYPE_LONG)
        data["buy_order_id"] = s.read(PACK_TYPE_LONG)
        data["sel_order_id"] = s.read(PACK_TYPE_LONG)
        data["trade_price"] = s.read(PACK_TYPE_DOUBLE)
        data["trade_volume"] = s.read(PACK_TYPE_DOUBLE)
        data["trade_type"] = s.read(PACK_TYPE_BYTE)
        data["res1"] = s.read(PACK_TYPE_BYTE)
        data["res2"] = s.read(PACK_TYPE_BYTE)
        data["res3"] = s.read(PACK_TYPE_BYTE)
        yield data


def read_order_file(c):
    s = stream_reader(c)
    head = s.read(PACK_TYPE_STRING,4)
    v1 = s.read(PACK_TYPE_BYTE)
    v2 = s.read(PACK_TYPE_BYTE)
    while not s.isEnd():
        data = {}
        data["code"] = s.read(PACK_TYPE_INT)
        data["set_id"] =  s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_INT)
        data["JT_time"] = s.read(PACK_TYPE_INT)
        data["rec_id"] =  s.read(PACK_TYPE_LONG)
        data["order_price"] = s.read(PACK_TYPE_DOUBLE)
        data["order_volume"] = s.read(PACK_TYPE_DOUBLE)
        data["order_code"] = s.read(PACK_TYPE_BYTE)
        data["reverse1"] = s.read(PACK_TYPE_BYTE)
        data["order_type"] = s.read(PACK_TYPE_BYTE)
        data["reverse2"] = s.read(PACK_TYPE_BYTE)

        yield data
def read_index_file(c):
    s = stream_reader(c)
    head = s.read(PACK_TYPE_STRING,4)
    v1 = s.read(PACK_TYPE_BYTE)
    v2 = s.read(PACK_TYPE_BYTE)

    while not s.isEnd():
        data = {}
        data["code"] = s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_INT)
        data["JT_time"] = s.read(PACK_TYPE_INT)
        data["res"] =  s.read(PACK_TYPE_INT)
        data["last_price"] = round(s.read(PACK_TYPE_DOUBLE),2)
        data["open_price"] = round(s.read(PACK_TYPE_DOUBLE),2)
        data["high_price"] = round(s.read(PACK_TYPE_DOUBLE),2)
        data["low_price"] = round(s.read(PACK_TYPE_DOUBLE),2)
        data["pre_close_price"] = round(s.read(PACK_TYPE_DOUBLE),2)
        data["trade_volume"] = s.read(PACK_TYPE_DOUBLE)

        yield data


def read_hquo_file(c):
    s = stream_reader(c)
    head = s.read(PACK_TYPE_STRING,4)
    v1 = s.read(PACK_TYPE_BYTE)
    v2 = s.read(PACK_TYPE_BYTE)

    while not s.isEnd():
        data = {}
        data["code"] = s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_LONG)
        data["last_price"] =  s.read(PACK_TYPE_DOUBLE)
        data["order_book"] =  s.read(PACK_TYPE_DOUBLE)
        data["trade_volume"] = s.read(PACK_TYPE_DOUBLE)
        data["withdraw_volume"] = s.read(PACK_TYPE_DOUBLE)

        yield data

def read_shorder_file(c):
    s = stream_reader(c)
    while not s.isEnd():
        data = {}
        data["rec_id"] =  s.read(PACK_TYPE_LONG)
        data["code"] = s.read(PACK_TYPE_INT)
        data["order_time"] = s.read(PACK_TYPE_INT)
        data["order_price"] = s.read(PACK_TYPE_DOUBLE)
        data["order_volume"] = s.read(PACK_TYPE_INT)
        data["order_code"] = s.read(PACK_TYPE_BYTE)
        data["reverse1"] = s.read(PACK_TYPE_BYTE)

        yield data

def read_quo_1_5(s):
    while not s.isEnd():
        data = {}
        data["symbol"] =  s.read(PACK_TYPE_INT)
        data["date"] =  s.read(PACK_TYPE_INT)
        data["jt_time"] = s.read(PACK_TYPE_INT)
        data["local_time"] = s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_INT)
        data["last_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["open_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["high_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["low_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["pre_close_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        for i in range(1, 11):
            data["buy_price%02d"%i] = round(s.read(PACK_TYPE_FLOAT),2)
        for i in range(1, 11):
            data["buy_volume%02d"%i] = s.read(PACK_TYPE_INT)
        for i in range(1, 11):
            data["sell_price%02d"%i] = round(s.read(PACK_TYPE_FLOAT),2)
        for i in range(1, 11):
            data["sell_volume%02d"%i] = s.read(PACK_TYPE_INT)
        data["uplimit"] = s.read(PACK_TYPE_FLOAT)
        data["downlimit"] = s.read(PACK_TYPE_FLOAT)
        data["total_amount"] = s.read(PACK_TYPE_DOUBLE)
        data["sp"] = s.read(PACK_TYPE_STRING, 8)
        data["ts"] = s.read(PACK_TYPE_STRING, 8)
        yield data

def read_quo_1_4(s):
    while not s.isEnd():
        data = {}
        data["symbol"] =  s.read(PACK_TYPE_INT)
        data["date"] =  s.read(PACK_TYPE_INT)
        data["jt_time"] = s.read(PACK_TYPE_INT)
        data["local_time"] = s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_INT)
        data["last_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["open_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["high_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["low_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        data["pre_close_price"] = round(s.read(PACK_TYPE_FLOAT),2)
        for i in range(1, 11):
            data["buy_price%02d"%i] = round(s.read(PACK_TYPE_FLOAT),2)
        for i in range(1, 11):
            data["buy_volume%02d"%i] = s.read(PACK_TYPE_INT)
        for i in range(1, 11):
            data["sell_price%02d"%i] = round(s.read(PACK_TYPE_FLOAT),2)
        for i in range(1, 11):
            data["sell_volume%02d"%i] = s.read(PACK_TYPE_INT)
        data["uplimit"] = s.read(PACK_TYPE_FLOAT)
        data["downlimit"] = s.read(PACK_TYPE_FLOAT)
        data["sp"] = s.read(PACK_TYPE_STRING, 8)
        data["ts"] = s.read(PACK_TYPE_STRING, 8)
        yield data

def read_quo_1_1(s):
    while not s.isEnd():
        data = {}
        data["symbol"] =  s.read(PACK_TYPE_INT)
        data["date"] =  s.read(PACK_TYPE_INT)
        data["jt_time"] = s.read(PACK_TYPE_INT)
        data["local_time"] = s.read(PACK_TYPE_INT)
        data["time"] = s.read(PACK_TYPE_INT)
        data["last_price"] = s.read(PACK_TYPE_DOUBLE)
        data["open_price"] = s.read(PACK_TYPE_DOUBLE)
        data["high_price"] = s.read(PACK_TYPE_DOUBLE)
        data["low_price"] = s.read(PACK_TYPE_DOUBLE)
        data["pre_close_price"] = s.read(PACK_TYPE_DOUBLE)
        data["buy_price01"] = s.read(PACK_TYPE_DOUBLE)
        data["buy_volume01"] = s.read(PACK_TYPE_LONG)
        data["sell_price01"] = s.read(PACK_TYPE_DOUBLE)
        data["sell_volume01"] = s.read(PACK_TYPE_LONG)
        data["uplimit"] = s.read(PACK_TYPE_DOUBLE)
        data["downlimit"] = s.read(PACK_TYPE_DOUBLE)
        data["sp"] = s.read(PACK_TYPE_STRING, 8)
        data["ts"] = s.read(PACK_TYPE_STRING, 8)
        yield data

def read_quo_file(c):
    s = stream_reader(c)
    head = s.read(PACK_TYPE_STRING,4)
    v1 = s.read(PACK_TYPE_BYTE)
    v2 = s.read(PACK_TYPE_BYTE)

    if v1 == 1 and v2 == 1:
        return read_quo_1_1(s)
    elif v1 == 1 and v2 == 4:
        return read_quo_1_4(s)
    elif v1 == 1 and v2 == 5:
        return read_quo_1_5(s)


def parse_file(path, is_compress):
    p = path[:path.rfind(".")]
    ext = path[path.rfind(".")+1:]
    if ext == "csv": return

    zf = open(path, "rb")
    c = zf.read()
    if is_compress:
        c = lzma.decompress(c)
    zf.close()

    of = "%s_%s.log" % (p, ext)
    if ext == "tran":
        title = ["股票编码", "成交时间", "记录号", "频道代码","", "成交价格",
                 "成交数量","","", "市场", "买方id", "卖方id","成交类型(52：撤单，70：成交)",
                 ]
        with open(of, "wt") as f:
            line = (",").join(title)
            f.write(line + "\n")
            for d in read_tran_file(c):
                linee = []
                linee.append("%06d" % d["code"])
                linee.append(d["time"])
                linee.append(d["JT_time"])
                linee.append(d["rec_id"])
                linee.append(d["set_id"])
                linee.append(0)# tradeChannel
                linee.append(d["trade_price"])
                linee.append(d["trade_volume"])
                linee.append(0)# tradeAmount
                linee.append(0)# UNIX
                linee.append("SZ")
                linee.append(d["buy_order_id"])
                linee.append(d["sel_order_id"])
                linee.append(d["trade_type"])
                linee = [str(s) for s in linee]
                line = (",").join(linee)
                f.write(line+"\n")
    elif ext== "order":
        title =["股票编码","委托时间","记录号","频道代码","委托价格",
                "委托数量","市场","买卖方向(1:买2:卖)","订单类别(1:市价2:限价)",
                ]
        with open(of, "wt") as f:
            line = (",").join(title)
            f.write(line + "\n")
            for d in read_order_file(c):
                linee = []
                linee.append("%06d" % d["code"])
                linee.append(d["time"])
                linee.append(d["JT_time"])
                linee.append(d["rec_id"])
                linee.append(d["set_id"])
                linee.append(d["order_price"])
                linee.append(d["order_volume"])
                linee.append("SZ")
                linee.append(d["order_code"])
                linee.append(d["order_type"])
                linee = [str(s) for s in linee]
                line = (",").join(linee)
                f.write(line+"\n")
    elif ext == "shorder":

        with open(of, "wt") as f:
            for d in read_shorder_file(c):
                linee = []
                linee.append("%06d" % d["code"])
                linee.append(d["rec_id"])
                linee.append(d["order_time"])
                linee.append(d["order_price"])
                linee.append(d["order_volume"])
                linee.append(d["order_code"])
                linee = [str(s) for s in linee]
                line = (",").join(linee)
                f.write(line+"\n")
    elif ext == "shtran":
        title =["股票编码","日期","成交","本地时间","交易所生成时间",
                "最新价","开盘价","最高价","最低价","上一个交易日收盘价",
                "买一价","买一量","卖一价","卖一量","涨停价",
                "跌停价","成交量","SecurityPhaseTag","TradeStatus",
                ]
        with open(of, "wt") as f:
            line = (",").join(title)
            f.write(line + "\n")
            for d in read_shtran_file(c):
                linee = []
                linee.append("%06d" % d["code"])
                linee.append(d["tradeChannel"])
                linee.append(d["rec_id"])
                linee.append(d["buy_rec_id"])
                linee.append(d["sel_rec_id"])
                linee.append(d["trade_time"])
                linee.append(d["trade_price"])
                linee.append(d["trade_volume"])
                linee.append(d["buySellFlag"])
                linee = [str(s) for s in linee]
                line = (",").join(linee)
                f.write(line+"\n")
    elif ext == "quo":
        title =["股票编码","日期","津泰时间","本地时间","交易所生成时间",
                "最新价","开盘价","最高价","最低价","上一个交易日收盘价",
                "买一价","买一量","买二价","买二量","卖一价","卖一量","卖二价","卖二量","涨停价",
                "跌停价","成交量","SecurityPhaseTag","TradeStatus",
                ]
        with open(of, "wt") as f:
            line = (",").join(title)
            f.write(line + "\n")
            for d in read_quo_file(c):
                linee = []
                linee.append("%06d" % d["symbol"])
                linee.append(d["date"])
                linee.append(d["jt_time"])
                linee.append(d["local_time"])
                linee.append(d["time"])
                linee.append(d["last_price"])
                linee.append(d["open_price"])
                linee.append(d["high_price"])
                linee.append(d["low_price"])
                linee.append(d["pre_close_price"])
                linee.append(d["buy_price01"])
                linee.append(d["buy_volume01"])
                linee.append(d["buy_price02"])
                linee.append(d["buy_volume02"])
                linee.append(d["sell_price01"])
                linee.append(d["sell_volume01"])
                linee.append(d["sell_price02"])
                linee.append(d["sell_volume02"])
                linee.append(d["uplimit"])
                linee.append(d["downlimit"])
                if "total_amount" in d:
                    linee.append(d["total_amount"])
                linee.append(d["sp"])
                linee.append(d["ts"])

                linee = [str(s) for s in linee]
                line = (",").join(linee)
                f.write(line+"\n")
    elif ext == "idx":
        title =["股票编码","交易时间","津泰时间",
                "最新价","开盘价","最高价","最低价","上一个交易日收盘价",
                "成交量"
                ]
        with open(of, "wt") as f:
            line = (",").join(title)
            f.write(line + "\n")
            for d in read_index_file(c):
                linee = []
                linee.append("%06d" % d["code"])
                linee.append(d["JT_time"])
                linee.append(d["time"])
                linee.append(d["last_price"])
                linee.append(d["open_price"])
                linee.append(d["high_price"])
                linee.append(d["low_price"])
                linee.append(d["pre_close_price"])
                linee.append(d["trade_volume"])

                linee = [str(s) for s in linee]
                line = (",").join(linee)
                f.write(line + "\n")
    elif ext == "hquo":
        title =["股票编码","生成时间",
                "最新价","成交量","封单量",
                "撤单量"
                ]
        with open(of, "wt") as f:
            line = ("\t").join(title)
            f.write(line + "\n")
            for d in read_hquo_file(c):
                linee = []
                linee.append("%06d" % d["code"])
                linee.append(d["time"])
                linee.append(d["last_price"])
                linee.append(d["trade_volume"])
                linee.append(d["order_book"])
                linee.append(d["withdraw_volume"])
                linee = [str(s) for s in linee]
                line = ("\t").join(linee)
                f.write(line+"\n")


if __name__ == '__main__':
    rootdir = r'F:\hqtest\data1'
    is_compress = False

    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            parse_file(path, is_compress)


    # parse_file(r"000002.quo", False)

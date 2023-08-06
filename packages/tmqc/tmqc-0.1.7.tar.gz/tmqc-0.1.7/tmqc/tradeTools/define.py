# -*- coding: utf-8 -*-
# 交易周期
from enum import Enum
class SUBSTITUTE_FLAG(Enum): # 现金替代标志
    ALLOW = 0           # 允许
    MUST = 1           # 必须
    FORBID = 2           # 禁止

class STK_STATUS(Enum):  # 股票状态
    NORMAL = 0           # 正常
    LIM_UP = 1           # 涨停
    LIM_DOWN = 2         # 跌停
    SUSPEND = 3          # 停牌



class PERIOD(Enum):
    s1 = "second1"
    m1 = "minite1"
    d1 = "day1"

class TRADE_TYPE(Enum):
    open  = 0
    close = 1

class CALL_OR_PUT(Enum):
    nil = 'NaN'
    call= 'call'
    put = 'put'

class DIR(Enum):
    buy     = 0
    sell    = 1
    both    = 2
    null    = 3

class MARKET(Enum):
    stock   = "stock"
    future  = "future"
    option  = "option"

class MODE(Enum):
    public      = "public"
    backtesting = "backtesting"

class ORDER_TYPE(Enum):
    LIMIT  = 0 # 限价委托
    MARKET = 1 # 市价委托

class ORDER_STATUS(Enum):
    """报单状态"""
    PENDING     = 0 # 待成交
    TRADED      = 1 # 已经全部成交
    TRADED_PART = 2 # 部分成交
    CANCEL_REQ  = 3 # 待撤单
    CANCELED    = 4 # 已撤单
    REJECTED    = 5 # 被拒绝
    FAILURE     = 6 # 已失败（网络问题等技术问题导致的失败）

class DATA_TYPE(Enum):
    """数据类型"""
    hq      = "hq"      # 行情
    hhq     = "hhq"     # 高速行情
    order   = "order"   # 报单
    tran    = "tran"    # 成交
    index   = "index"   # 指数
    info    = "info"    # 股票信息
    div     = "div"     # 股票分红送配
    k_min   = "k_min"    # K线
    k_day   = "k_day"    # K线

# 返回值状态类型
class RET_TYPE(Enum):
    """数据类型"""
    NORMAL       = 0   # 正常
    ERR_NORMAL   = 1   # 一般错误
    ERR_SERIOUS  = 2   # 严重错误
    ERR_IGNORE   = 3   # 忽略错误 - 做心跳.

MAX_POSITION_NUMBER = 9999999999
USE_REFERENDUM_PRICE = False
MAX_STOCK_CODE = 1700000

# USE_DATACENTER 控制datacenter 读取数据的模式
USE_DATACENTER = "mysql"
# USE_DATACENTER = "redis"

LOG_ERROR = "error"
LOG_DATA = "data_error"
LOG_SQL = "sql"
LOG_TRADE = "trade"
LOG_TRANSECTION = "transection"
LOG_TRADE_ERROR = 'trade_error'
LOG_ORDER = "order"
LOG_GATEWAY = "gateway"
LOG_RECORD = "trade_record"
LOG_POLICY = "trade_policy"
LOG_POSITION = "position"
LOG_POSITION_CHANGE = "position_change"
LOG_DAY_NET_VALUE = "day_net_value"
LOG_MONTH_NET_VALUE = "month_net_value"
LOG_YEAR_NET_VALUE = "year_net_value"
LOG_SUMMARY_REPORT = "summary_report"
LOG_EACH_STOCK_PROFIT = "each_stock_profit"
LOG_CLOSE_PROFIT = "close_profit"

LOG_DIVIEND_DIVIEND = "diviend_diviend"
LOG_DIVIEND_TRANSFER = "diviend_transfer"
LOG_DIVIEND_QTY_COST = "diviend_qty_cost"
LOG_DIVIEND_BUY = "diviend_buy"
LOG_DIVIEND_BUY_FAILED = "diviend_buy_failed"
LOG_DATACENTER = "dataCenter"
LOG_MQRECEIVER = "mqReceiver"

g_log_switch = {
    LOG_ERROR : True,
    LOG_DATA : False,
    LOG_TRADE : True,
    LOG_RECORD : True,
    LOG_POSITION_CHANGE : True,
    LOG_EACH_STOCK_PROFIT : True,
    LOG_DIVIEND_DIVIEND : True,
    LOG_DIVIEND_TRANSFER : True,
    LOG_DIVIEND_QTY_COST : False,
    LOG_DIVIEND_BUY : True,
    LOG_DIVIEND_BUY_FAILED : False,
}


g_report_switch = {
    LOG_RECORD : False,
    LOG_MONTH_NET_VALUE : True,
    LOG_YEAR_NET_VALUE : True,
    LOG_SUMMARY_REPORT: True,
    LOG_DAY_NET_VALUE: True,
}

def is_log_switch_on(log_name):
    return g_report_switch.get(log_name, False)

def enum(**enums):
    return type('Enum', (), enums)

EVENT_TICK          = 'eTick.'          # TICK行情事件，可后接具体的vtSymbol
EVENT_TRADE         = 'eTrade.'         # 成交回报事件
EVENT_ORDER         = 'eOrder.'         # 报单回报事件
EVENT_ORDER_STATUS  = 'eOrderStatus'    # 报单状态
EVENT_POSITION      = 'ePosition.'      # 持仓回报事件
EVENT_TRANSACTION   = 'eTransaction'    # 成交回报事件
EVENT_ACCOUNT       = 'eAccount.'       # 账户回报事件
EVENT_CONTRACT      = 'eContract.'      # 合约基础信息回报事件
EVENT_ERROR         = 'eError.'         # 错误回报事件
EVENT_COMMAND       = 'eCommand'        # 交易
EVENT_TIMER         = 'eTimer'          # 时间心跳事件
EVENT_DATA          = 'eData.'          # 数据接收事件

if __name__ == '__main__':
    a = enum(**g_report_switch)
    print (dir(a))
    print(STK_STATUS(1))
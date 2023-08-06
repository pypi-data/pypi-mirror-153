from typing import List
from dataclasses import dataclass
from common.define import ( TRADE_TYPE,
                            ORDER_TYPE,
                            ORDER_STATUS,
                            MARKET,
                            DIR)

@dataclass
class BaseData:
    """
    Any data object needs a gateway_name as source or
    destination and should inherit base data.
    """
    gateway_name: MARKET

@dataclass
class stBarData(BaseData):
    """
    Candlestick bar data of a certain trading period.
    """
    code: str
    date: int
    time: int
    volume: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

@dataclass
class stSendOrder(BaseData):
    """报单"""
    code: str
    order_type: ORDER_TYPE
    trade_type: TRADE_TYPE
    dir: DIR
    price: float
    number: int
    date: int
    time: int
    name: str
    local_no: str
    order_no: str = ''


@dataclass
class stCancelOrder(BaseData):
    """撤单"""
    order_no: str
    market: int
    status: ORDER_STATUS


@dataclass
class stPositionsRequest(BaseData):
    """持仓请求"""
    pass

@dataclass
class stTransRequest(BaseData):
    """成交请求"""
    pass

@dataclass
class stOrdersRequest(BaseData):
    """报单请求"""
    pass


@dataclass
class stOrderStatus(BaseData):
    """报单状态"""
    order_no: str       # 委托编号
    status: ORDER_STATUS


@dataclass
class stPos:
    """持仓信息"""
    code: str
    price: float
    number: int
    dir: DIR
    margin: float           # 市值
    unlimited_sell: int =0  # 可卖数量(昨仓数量
    name: str = ''          # 合约名字
    day_counter: int =0     # 持仓时间
    datetime_last: int =0   # 加仓/减仓时间
    datetime_open: int =0   # 开仓时间

@dataclass
class stPositions(BaseData):
    """持仓集合"""
    datas: List[stPos]

@dataclass
class stOrder:
    """报单信息"""
    code: str
    name: str
    dir: DIR
    trade_type: TRADE_TYPE
    date:int
    order_time: int     # 委托时间
    price: float        # 委托价格
    price_traded: float # 成交价格
    number: int         # 委托数量
    number_traded: int  # 成交数量
    number_cancel: int  # 撤单数量
    order_no: str       # 委托编号
    local_no: str       # 本地编号
    status: ORDER_STATUS# 委托状态

@dataclass
class stOrders(BaseData):
    """报单集合"""
    datas: List[stOrder]


@dataclass
class stTran:
    """成交记录"""
    market:MARKET
    code:str
    date:int
    tran_time:int
    dir:DIR
    trade_type: TRADE_TYPE
    price:float
    commission:float
    number_traded:int
    order_no:str           # 委托编号
    tran_no:str            # 成交编号
    turnover:float         # 发生金额
    op_name:str = ''       # 业务名称
    name:str = ''
    trade_code:str = ''     # 交易代码


@dataclass
class stTrans(BaseData):
    """成交集合"""
    datas: List[stTran]


@dataclass
class stProfit:
    """利润记录"""
    code:str
    date:int
    time: int
    dir: DIR
    price: float
    number: int
    tran_no: str   # 成交编号
    profit: float
    commission: float
    name:str = ''

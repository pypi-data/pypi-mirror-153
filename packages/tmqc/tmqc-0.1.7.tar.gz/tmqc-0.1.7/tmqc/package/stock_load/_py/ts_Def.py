# python 结构体定义
from enum import Enum
from dataclasses import dataclass

import _stock_load as lib

# 购或沽
class Type(Enum):
    # 股票
    Stock           = lib.Type.Stock
    # 指数
    Index           = lib.Type.Index
    # 基金
    Fund            = lib.Type.Fund
    # 期货
    Future          = lib.Type.Future
    # 期权
    Option          = lib.Type.Option
    # 债券
    Bond            = lib.Type.Bond
    # 可转换债券
    BondConvertible = lib.Type.BondConvertible

# 交易所
class Market(Enum):
    ShangHai        = lib.Market.ShangHai
    ShenZhen        = lib.Market.ShenZhen


# 股票信息
class Info:
    # 日期 yyyymmdd
    date:int
    # 时间 hhmmss
    time:int
    # 类型
    type:Type
    # 市场
    mk:Market
    # 合约代码(一般是数字, 也可能是字符, 如期货.)
    code:str
    # 开
    open:float
    # 高
    high:float
    # 低
    low:float
    # 收
    close:float
    # 数量
    volume:int 

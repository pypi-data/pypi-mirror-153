'''
    这里测试了从历史行情仓库获取历史数据的接口.

    测试:
        1. 进入python3.6 环境
            F:/ProgramFiles/Anaconda3/Scripts/activate
            conda activate F:\ProgramFiles\Anaconda3
        
        2. 测试命令
            python test_py_hq_client.py

'''
import time
from py_hq_client import *

print("begin work")

# 测试获取某日的分钟线行情信息
info = hq_client_fetch(BAR_TYPE.Minute, 
                       CodeInfo(MARKET_TYPE.ShangHai, HQ_TYPE.Stock, 510050), 
                       TimePos(20201201, 93000000), 
                       TimePos(20210115, 150000000))

# 测试订阅标的的实时行情信息
hq_client_subscribe(CodeInfo(MARKET_TYPE.ShangHai, HQ_TYPE.Stock, 510050))

# 获取当日标的的情况
ltime = time.localtime()
yyyymmdd = int(time.strftime('%Y%m%d', ltime))
optInfos = hq_client_get_day_opt_info(yyyymmdd)

if optInfos and len(optInfos):
    for optInfo in optInfos:
        # 订阅当日期权信息
        hq_client_subscribe(CodeInfo(MARKET_TYPE.ShangHai, HQ_TYPE.Option, optInfo.code))


while True:
    if not hq_client_is_connect():
        # 连接已经断开
        break
    
    hq = hq_client_try_take()
    if not hq:
        # 未获取到行情
        # 模拟推送一个行情
        # hq_client_push(BAR_TYPE.Tick, HQInfo(mk= MARKET_TYPE.ShangHai, 
        #     hq= HQ_TYPE.Stock, 
        #     code = 510050,
        #     date = 20200102, 
        #     time = 15,
        #     open = 1.0,
        #     high = 2.0,
        #     low = 3.0,
        #     close = 4.0,
        #     volume = 5.0))
        time.sleep(0.1)
        continue

    print(str(hq.cinfo.code) + ' ' + str(hq.close))


print("all ok end work")
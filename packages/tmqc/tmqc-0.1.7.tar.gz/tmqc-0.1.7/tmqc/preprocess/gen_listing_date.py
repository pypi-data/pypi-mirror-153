import re
from common import log
from common import basefunc
from frame import DataContainer as DC
from frame import DataType
from frame.MarketContainer import StockContainer
# from collections import Counter

def get_listing_date(database,code):
    sql = "SELECT time FROM tdx_day_data WHERE code = '%s' ORDER BY TIME DESC LIMIT 1" % code
    database.Query(sql)
    data = database.FetchOne()
    if not data: return None, None
    
    delisting_date = data[0]
    sql = "SELECT time FROM tdx_day_data WHERE code = '%s' ORDER BY TIME ASC LIMIT 1" % code
    database.Query(sql)
    data = database.FetchOne()
    listing_date = data[0]
    
    return listing_date, delisting_date

def acquire_listing_data(database, codes):
    listing_dates =[]
    progress = 0
    
    length = len(codes)
    for code in codes:
        progress += 1
        listing_date, delisting_date = get_listing_date(database, code)
        if not listing_date:
            log.WriteLog("get_listing_err","get stock[%s] listing date fail from tdx_day_data"%code)
            continue
        listing_dates.append((code, listing_date, delisting_date))
        print("std_listing_date: progress  %d/%d"%(progress, length))
    return listing_dates

def write_file(datas):
    baseRoot = basefunc.get_path_dirname()
    log.WriteLog("sys", "baseRoot:"+baseRoot)
    filename = f'{baseRoot}/rec/listing_date.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for code,listing_date,delisting_date in datas:
            f.write(f'{code}\t{listing_date}\t{delisting_date}\n')

def read_file():
    baseRoot = basefunc.get_path_dirname()
    filename = f'{baseRoot}/rec/listing_date.txt'
    
    info = {}
    with open(filename,'rt', encoding='utf8') as f:
        c = f.read()
        if len(c) == 0:
            print("请先运行 preprocess/gen_listing_date.py 生成上市/退市日期数据！")
            return
        ls = c.split('\n')
        for l in ls[1:]:
            try:
                e = re.split(r'\s+', l)
                if len(e) == 3:
                    info[e[0]] = ({'listing_date': e[1], 'deliting_date': e[2]})
            except:
                pass
    return info
            
def gen():
    # 加载股票信息表
    database = basefunc.create_database()
    
    info = DC.DictArray(keys= DataType.keys_stock_info, types = DataType.dtype)
    c = StockContainer({})    
    c.load_info_from_file(info, database, 0, 0)

    codes = info.codes()
    datas = acquire_listing_data(database, codes)
    
    # # 过滤掉抓取数据的最后一天，这一天不是退市日
    # dates = [d[1] for d in datas]
    # last_date = Counter(dates).most_common(1)[0][0]
    # datas = [(code, date) for code, date in datas if date != last_date]
    
    write_file(datas)
    
        
if __name__ == '__main__':
    # gen()
    
    info = read_file()
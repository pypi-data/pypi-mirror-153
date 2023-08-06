
from frame import DataContainer as DC
from frame import DataType
from frame.DataCenterBkt import DbReader
from frame.MarketContainer import StockContainer
from common import basefunc

def price_restoration(begin_time, end_time):
    restoration_table_name = 'day_data_restoration'
    database = basefunc.create_database()
    # 先检查复权表是否存在，不存在则建表
    database.Query('select * from information_schema.tables where table_name =\'%s\'' % restoration_table_name)
    rec = database.FetchOne()
    if not rec:
        database.Execute("""CREATE TABLE IF NOT EXISTS `%s` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `code` varchar(150) NOT NULL,
                        `time` int(11) NOT NULL,
                        `close` float DEFAULT NULL,
                        PRIMARY KEY (`id`),
                        UNIQUE KEY `id_time` (`code`,`time`),
                        KEY `time` (`time`)
                        ) ENGINE=MyISAM AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;""" % restoration_table_name)
        database.Commit()
    else: 
        database.Execute('truncate table %s' % restoration_table_name)
                
    # 加载分红配股表
    c = StockContainer({})    
    div = DC.DictArray(keys = DataType.keys_div, types = DataType.dtype)
    c.load_div_from_file(div, begin_time, end_time)
    
    # 加载股票信息表
    info = DC.DictArray(keys= DataType.keys_stock_info, types = DataType.dtype)
    c.load_info_from_file(info, begin_time, end_time)

    codes = info.codes()
    for code in codes:
        if div[code] is None:
            # 没有分红送股，不需要复权
            database.Execute('INSERT INTO %s SELECT 0,`code`,`time`,`close` FROM %s WHERE `code`="%s"' % 
                             (restoration_table_name, 'tdx_day_data', code))
        else:
            file = DbReader(DataType.keys_K1, begin_time, end_time, 'tdx_day_data', [code], batch_number = 10000)
            data = []
            actor = 1
            while not file.is_end():
                while file.data and file.data['date'] <= end_time:                    
                    code = file.data['code']

                    D = div[code]
                    if D is None: continue
                    D = D[D['reg_date'] == file.data['date']] # 这里使用登记日，登记日当天结束后分红配股除权
                    if D and D.size > 0: 
                        # 先进行复权运算
                        close = file.data['close']
                        file.data['close'] = float(round(file.data['close'] * actor, 3))
                        
                        # 累计计算当日除权因子
                        dividend_rec = D.iloc[0]
                        qty          = dividend_rec["qty"] #配股数
                        price        = dividend_rec["price"] #配股价
                        dividend     = dividend_rec["dividend"] # 红利
                        transfer     = dividend_rec["transfer"] #配股+送股数
                        # ratio = dividend_rec["ratio"]
                        """
                        除息价＝股权登记日收盘价-每股所派现金
                        送股除权计算办法为：送股除权价＝股权登记日收盘价÷(1＋送股比例)
                        配股除权价计算方法为：配股除权价＝(股权登记日收盘价＋配股价×配股比例)÷(1＋配股比例)
                        有分红、派息、配股的除权价计算方法为：除权价＝(收盘价＋配股比例×配股价-每股所派现金)÷(1＋送股比例＋配股比例)
                        """
                        res_close = (close + qty/10.0 * price - dividend/10.0)/(1+transfer/10.0 + qty/10.0)
                        actor *= close / res_close
                    else:
                        file.data['close'] = float(round(file.data['close'] * actor, 3))
                    data.append([file.data['code'], file.data['date'], file.data['close']])
                    file.step()
                    
            database.Executemany('INSERT INTO '+ restoration_table_name +' VALUES(0,%s,%s,%s)', data)
        print(code, "OK")
        
        
if __name__ == '__main__':
    price_restoration(19800101, 20991231)
    
    
# -*- coding: utf-8 -*-
# @Time    : 2017/1/24 16:55
# @Author  : hc
# @Site    :
# @File    : TestTrade.py
# @Software: PyCharm
# DLL是32位的,编译环境需要python 2.7以上的32位版本
# /// <param name="IP">券商交易服务器IP</param>
# /// <param name="Port">券商交易服务器端口</param>
# /// <param name="Version">设置通达信客户端的版本号</param>
# /// <param name="YybID">营业部代码，请到网址 http://www.chaoguwaigua.com/downloads/qszl.htm 查询</param>
# /// <param name="AccountNo">完整的登录账号，券商一般使用资金帐户或客户号</param>
# /// <param name="TradeAccount">交易账号，一般与登录帐号相同. 请登录券商通达信软件，查询股东列表，股东列表内的资金帐号就是交易帐号</param>
# /// <param name="JyPassword">交易密码</param>
# /// <param name="TxPassword">通讯密码</param>
# import TradeX
# import _TradeX
# client_id, err = TradeX.Logon("119.145.12.67", 443, "6", 11, "06118253378", "06118253378", "188188", "")
# client_id, err = TradeX.Logon("mock.tdx.com.cn", 7708, "6.40", 9000, "net828@163.com", "f001001001005792", "123123", "")
# if client_id < 0 :
#   print "fail"
#   err= err.decode('gb2312')
#   err =err.encode('utf-8')
#   print err
# else :
#   print "ok\n"
# ret, res, err = TradeX.TdxHq_Connect("14.17.75.71", 7709)
# print res.decode('gb2312').encode('utf-8')
# print err.decode('gb2312').encode('utf-8')
# #
# ret, res, err = TradeX.TdxHq_GetMinuteTimeData(0, "000001")
# print ret
# print res.decode('gb2312').encode('utf-8')
# print err.decode('gb2312').encode('utf-8')
# # print dir(TradeX)
# # print dir(_TradeX)
import ctypes
dll = ctypes.windll.LoadLibrary( 'trade20171030.dll' )
# dll =ctypes.cdll('trade20171030.dll')
IP="119.145.12.67"          #券商交易服务器IP
Port=443                    #券商交易服务器端口
Version="2.37"                 #设置通达信客户端的版本号
YybID=0                     #营业部代码
AccountNo="0618253378"     #完整的登录账号，券商一般使用资金帐户或客户号
TradeAccount="0618253378"  #交易账号
JyPassword="188188"          #交易密码
TxPassword=""           #通讯密码
ErrInfo=ctypes.create_string_buffer('/0' * 256)
# CBIQARGDEQ
#此API执行返回后，如果出错，保存了错误信息说明。一般要分配256字节的空间。没出错时为空字符串。
# ClientID =  dll.Logon("mock.tdx.com.cn", 7708, "6.40", 9000, "net828@163.com", "f001001001005792", "123123", "", ErrInfo)
# print dll.Logon(IP, Port,Version, YybID, AccountNo,TradeAccount, JyPassword, TxPassword, ErrInfo)
dll.OpenTdx()
# ErrInfo = ctypes.create_string_buffer('/0' * 256)
ClientID = dll.Logon(IP, Port,Version, YybID, AccountNo,TradeAccount, JyPassword, TxPassword, ErrInfo)
print(ClientID)
# print ErrInfo
print(ErrInfo.value.decode("gbk"))
# print(ClientID)
Result=ctypes.create_string_buffer('/0' * 1024)
dll.QueryData(ClientID, 4, Result, ErrInfo)# 查询资金
# ClientID.GetQuote()
# print (Result.value.decode("gbk"))
dll.QueryHistoryData(ClientID, 1, "20171025","20171030",Result,ErrInfo)# 查询各种历史数据
print(Result.value.decode("gbk"))
# <param name="ClientID">客户端ID</param>
# <param name="Category">表示委托的种类，0买入 1卖出  2融资买入  3融券卖出   4买券还券   5卖券还款  6现券还券</param>
# <param name="PriceType">表示报价方式 0上海限价委托 深圳限价委托 1(市价委托)深圳对方最优价格
#  2(市价委托)深圳本方最优价格  3(市价委托)深圳即时成交剩余撤销  4(市价委托)上海五档即成剩撤 深圳五档即成剩撤 5(市价委托)深圳全额成交或撤销 6(市价委托)上海五档即成转限价
# <param name="Gddm">股东代码, 交易上海股票填上海的股东代码；交易深圳的股票填入深圳的股东代码</param>
# <param name="Zqdm">证券代码</param>
# <param name="Price">委托价格</param>
# <param name="Quantity">委托数量</param
price  =ctypes.c_float()
price.value = 10.03
# dll.SendOrder(ClientID, 0, 0, "0121059858", "002864", price, 8500,Result,ErrInfo)
# import sys
# reload(sys)
# sys.getdefaultencoding('utf8')
# print (Result.value,ErrInfo.value.decode("gbk"))
# print(Result.value.decode("gbk").encode("utf8"))
# print(ErrInfo.value.decode("gbk").encode("utf8"))
# # print("\xe5\xa7\x94\xe6\x89\x98\xe4\xbb\xb7\xe6\xa0\xbc\xe9\x9d\x9e\xe6\xb3\x95".decode("gbk"))
# print("\xce\xaf\xcd\xd0\xb1\xe0\xba\xc5\t\xb7\xb5\xbb\xd8\xd0\xc5\xcf\xa2\t\xbc\xec\xb2\xe9\xb7\xe7\xcf\xd5\xb1\xea\xd6\xbe\t\xb1\xa3\xc1\xf4\xd0\xc5\xcf\xa2\n14\t\t\t".decode("gbk"))
# # 委托价格非法
# print "\xce\xaf\xcd\xd0\xbc\xdb\xb8\xf1\xb7\xc7\xb7\xa8".decode("gbk").encode("utf8")
# # 不存在的客户号或者客户号和股东代码不匹配!
# print "\xb2\xbb\xb4\xe6\xd4\xda\xb5\xc4\xbf\xcd\xbb\xa7\xba\xc5\xbb\xf2\xd5\xdf\xbf\xcd\xbb\xa7\xba\xc5\xba\xcd\xb9\xc9\xb6\xab\xb4\xfa\xc2\xeb\xb2\xbb\xc6\xa5\xc5\xe4!".decode("gbk")
print(dll.CloseTdx())

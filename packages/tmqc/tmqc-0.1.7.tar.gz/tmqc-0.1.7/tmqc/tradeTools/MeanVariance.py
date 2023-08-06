# -*- coding: utf-8 -*-
# 简单实现
# https://zhuanlan.zhihu.com/p/60499205
# 原理
# https://mp.weixin.qq.com/s?__biz=MzIxMDM0Mjg1Mw==&mid=2247483730&idx=1&sn=d32547775c275fad11ad0b724535e25f&chksm=976747f8a010ceeed594e1ca98fdbeb580132cd2531753b108adf8e1f73ad4e95c3d5e737e8f&scene=178&cur_album_id=1524209730238382081#rd
# 贝叶斯优化
# https://zhuanlan.zhihu.com/p/38282835
# https://zhuanlan.zhihu.com/p/363540266
from os import stat
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from tradeTools import Decorator
from tradeTools import helpers
from tradeTools import indexData
from tradeTools import DataMgr
import scipy.optimize as sco
import matplotlib.pyplot as plt
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.efficient_frontier import EfficientFrontier


class MeanVariance():
    def __init__(self) -> None:
        pass
    
    def getSymbolsData(self,symbols,endDate):
        self.mgr = DataMgr.Mgr()
        rates = []
        for symbol  in symbols:
            rateDf = self.mgr.getSymbolRateData(symbol=symbol,frequency=1)
            star = endDate.replace(endDate.year - 2)
            df = rateDf[(star<=rateDf.index)&(rateDf.index<=endDate)]
            rate = df["rate"]
            rate.name = symbol
            rates.append(rate)
        df = pd.DataFrame(rates)
        df = df.T
        return df
    
    def optWeights(self,df:DataFrame,coef:int = 252,type:str="avg",isSale=False,expectedRet =np.array([]))->DataFrame:
        """[利用马科维茨模型获取最优权重]

        Args:
            df (DataFrame): [收益率序列 ，每一列代表一只股票，每一行代表一天的收益率]
            coef (int, optional): [转换为年化的系数。如果收益率序列式日频，默认值为252]. Defaults to 252.
            type (str, optional): [求解。平均权重/最小方差/最优夏普 "minVar","avg","minSharp"]. Defaults to "avg".
            isSale (bool, optional): [是否允许做空]
            expectedRet (list, optional): [期望的收益率]. Defaults to []. 如果为空。这期望收益率是历史收益率的均值
        Returns:
            DataFrame: [description]
        """
        if expectedRet.size != 0:
            rtn = expectedRet
        else:
            rtn = df.mean()
        def stats(weights):
            weights = np.array(weights)
            port_returns = np.sum(rtn*weights)*coef # 年化收益率
            port_variance = np.sqrt(np.dot(weights.T, np.dot(df.cov()*coef,weights))) # 年化标准差
            return np.array([port_returns, port_variance, port_returns/port_variance])

        #给定初始权重
        cnt = df.shape[1]
        x0 = cnt*[1./cnt] # 初始权重。平均分配
        if type!="avg":
            if type =="minVar":
                def minFunc(weights):
                    return stats(weights)[1]**2
            else : # type =="minSharpe"
                def minFunc(weights):
                    return -stats(weights)[2] #最小化夏普指数的负值
           
            if isSale:
                bnds = ()
            else:
                 #权重（某股票持仓比例）限制在0和1之间。
                bnds = tuple((0,0.2) for x in range(cnt))
            #权重（股票持仓比例）的总和为1。
            cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1})
            #优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。我们简单的使用平均分布。
            opts = sco.minimize(minFunc,
                                x0, 
                                method = 'SLSQP', 
                                bounds = bnds, 
                                constraints = cons)
            w = opts["x"]
            w = w.round(3)
        else:
            w = x0
        symbolWeights = pd.DataFrame({"code":df.columns,
        "weight":w}
        )
        symbolWeights.set_index('code', inplace=True)
        print("权重",w)
        print("预期收益率，标准差，夏普率：",stats(w))        
        return  symbolWeights
def genSymbolsReturn(symbols):
    dfs = []
    m = DataMgr.Mgr() 
    for symbol  in symbols:
        # TODO是否要用log计算对数收益率
        rate = m.genSymbolRateData(symbol=symbol,frequency=1)
        rate = rate[("20160528"<=rate.index)&(rate.index<="20201226")]
        rate = rate["mRate"]
        rate.name = symbol
        dfs.append(pd.DataFrame(rate))
    symbolsReturn = pd.concat(dfs,axis=1) 
    # symbolsReturn = symbolsReturn.dropna()
    return symbolsReturn    

# 获取最后一日市值权重比例
def genMarketValueWeight(symbols):
    dfs = []
    m = DataMgr.Mgr() 
    for symbol  in symbols:
        # TODO是否要用log计算对数收益率
        rate = m.genSymbolRateData(symbol=symbol,frequency=1)
        rate = rate[("20180528"<=rate.index)&(rate.index<="20200326")]
        marketValue = rate["MarketV"]
        marketValue.name = symbol
        dfs.append(pd.DataFrame(marketValue))
    marketValue = pd.concat(dfs,axis=1) 
    marketValue["TOTAL"] = marketValue.sum(axis=1) 
    marketValue = (marketValue.T / marketValue.TOTAL).T # 求权重
    marketValue = marketValue.iloc[-1]
    marketValue = marketValue.drop("TOTAL")
    return marketValue   

class BlackLitterman:
    # 计算风险厌恶系数lambda、先验预期收益率implied_ret
    def get_implied_excess_equilibrium_return(self, stock_cc_ret, w_mkt):
        '''
        :param stock_cc_ret: 指定T部分的10只股票收益率数据（维度：T * 10）
        :param w_mkt: 当前的市场权重（维度：1*10）
        :return: 风险厌恶系数lambd、先验预期收益率：implied_ret
        '''

        # weekly risk-free cc return = ln(1+3.24%)/(365/7) = 0.0006132
        # rf = (1+3.24/100)/(365) # 无风险日收益率
        rf = 0 # 无风险日收益率
        # 根据股票收益率计算得到协方差矩阵：mkt_cov
        mkt_cov = np.array(stock_cc_ret.cov())

        # lambd: implied risk-aversion coefficient（风险厌恶系数）
        # 即计算夏普率
        lambd = ((np.dot(w_mkt, stock_cc_ret.mean())) - rf) / np.dot(np.dot(w_mkt, mkt_cov), w_mkt.T)
        # 计算先验预期收益率：implied_ret
        implied_ret = lambd * np.dot(mkt_cov, w_mkt)
        return implied_ret, lambd
    
    # 设定观点矩阵 P、相对收益率向量 Q（共4种Views可选）
    # 目前 只有view_type =3 可用
    def get_views_P_Q_matrix(self,stock_cc_ret):
        N = stock_cc_ret.shape[1]
        
        T_near = 30
        P = np.identity(N)
        stock_cc_ret_near = stock_cc_ret.iloc[-T_near:]
        stock_cc_ret_near = stock_cc_ret_near.fillna(0)  # 停牌股。当日的收益率为0
        print("stock_cc_ret_near.mean()")
        print(stock_cc_ret_near.mean())
        Q = np.array(stock_cc_ret_near.mean())
        return P,Q    
    """
        if(view_type == 0 or view_type == 1):
            # view_type = 0: 投资者无观点，使用当前市值权重（即均衡状态下的权重）作为作为投资组合的权重
            # view_type = 1: 为投资者分配任意观点，这里随机分配了3个观点
            '''
            # 观点1. 伯克希尔哈撒韦比埃克森美孚的预期收益高0.01%；
            # 观点2. 微软比摩根大通的预期收益高0.025%；
            # 观点3. 10%摩根+90%VISA的投资组合比10%沃尔玛+90%美国银行的投资组合预期收益高0.01%
            # '''
            # P = np.zeros([3, N])
            # P[0, 8] = 1
            # P[0, 9] = -1
            # P[1, 1] = 1
            # P[1, 3] = -1
            # P[2, 3] = 0.1
            # P[2, 4] = 0.9
            # P[2, 6] = -0.1
            # P[2, 7] = -0.9
            # Q = np.array([0.0001, 0.00025, 0.0001])
        elif(view_type == 2):
          
            P = np.zeros([1, N])
            P[0, 2] = 1
            P[0, 3] = -1
            Q = [0.017]
        elif(view_type == 3):
            # view_type = 3: 选用最近VIEW_T期的历史平均收益率作为预期收益率
            # T_near: 使用近期T_near期数据的历史平均收益率作为预期收益率
            T_near = 30
            P = np.identity(N)
            stock_cc_ret_near = stock_cc_ret.iloc[-T_near:]
            Q = np.array(stock_cc_ret_near.mean())
        else:
            print("There is no such kind of view type!")
        return P, Q
    """
  # Step8. 计算Omega矩阵
    def get_views_omega(self, mkt_cov, P):
        tau = 0.3   # 后验期望收益率协方差矩阵的放缩尺度，取值在0~1之间
        # K: 投资者观点的数量
        K = len(P)
        # 生成K维度的对角矩阵（对角线上全为1）
        omega = np.identity(K)
        for i in range(K):
            # 逐行选取P（Views矩阵，维度：K*N，此处N=10）
            P_i = P[i]
            omg_i = np.dot(np.dot(P_i, mkt_cov), P_i.T) * tau
            # 将得到的结果赋值到矩阵对角线元素
            omega[i][i] = omg_i
        return omega
    
    # Step9. 计算后验期望收益率mu_p
    def calc_posterior_combined_return(self, mkt_cov, implied_ret, P, Q, omega):
        # tau为缩放尺度
        tau = 0.3   # 后验期望收益率协方差矩阵的放缩尺度，取值在0~1之间
        # 后验期望收益率mu_p的计算公式
        _tau = np.linalg.inv(tau * mkt_cov)
        _omega = np.linalg.inv(omega)
        k = np.linalg.inv(_tau + np.dot(np.dot(P.T, _omega), P))
        posterior_ret = np.dot(k, np.dot(np.linalg.inv(tau * mkt_cov), implied_ret) +
                            np.dot(np.dot(P.T, np.linalg.inv(omega)), Q))
        return posterior_ret   
    
        # Step10. 计算由BL模型得到的新权重weight_bl
    def get_weight_bl(self, posterior_ret, mkt_cov, lambd):
        weight_bl = np.dot(np.linalg.inv(lambd * mkt_cov), posterior_ret)
        return weight_bl
    
    def getPosteriorCombinedReturn(self,df:DataFrame,marketValueWeight:Series):
        mkt_cov = np.array(df.cov())                              # 将T区间部分的股票收益率计算成协方差矩阵

        implied_ret, lambd = self.get_implied_excess_equilibrium_return(stock_cc_ret=df,w_mkt=marketValueWeight)
        # print(f"先验收益率{implied_ret}")
        P,Q = self.get_views_P_Q_matrix(stock_cc_ret = df)
        omega = self.get_views_omega(mkt_cov = mkt_cov , P = P) 
        # 后验收益率
        posterior_ret = self.calc_posterior_combined_return(
            implied_ret = implied_ret,
            mkt_cov = mkt_cov, 
            P=P,
            Q=Q, 
           omega=omega
            )
        # print(f"后验收益率{posterior_ret}")
        return posterior_ret
        # w = self.get_weight_bl(posterior_ret, mkt_cov, lambd)
        
        # symbolWeights = pd.DataFrame({"code":df.columns,
        # "weight":w.round(3)}
        # )
        # print("权重：",w.round(3))
        
        # return symbolWeights
class Kelly:
    def optWeights(self,df):
        mean_returns = df.mean()
        cov_matrix = df.cov()
        precision_matrix = pd.DataFrame(np.linalg.inv(cov_matrix), index=df.columns.tolist(), columns=df.columns.tolist())
        kelly_wt = precision_matrix.dot(mean_returns)
        print(kelly_wt)
        maxV = kelly_wt.max()
        print(maxV)
        minV = kelly_wt.min()
        def f(x):
            return 1.0/(1+np.exp(-x))
        # def f(x):
        #     x = (x - minV) / (maxV - minV)
        #     return x
        kelly_wt = kelly_wt.apply(f)
        kelly_wt = kelly_wt/kelly_wt.sum()
        df = pd.DataFrame(kelly_wt,columns=["weight"])
        print(df)
        return df
if __name__ == '__main__':
    #===========测试用的收益率序列==========
    # symbols = [
    # 'SZ.000651',       ##格力电器   
    # 'SH.600519',       ##贵州茅台  
    # 'SH.601318',       ##中国平安               
    # 'SZ.000858',       ##五粮液  
    # 'SH.600887',       ##伊利股份  
    # 'SZ.000333',       ##美的集团   
    # 'SH.601166',       ##兴业银行  
    # 'SH.601328',       ##交通银行  
    # 'SH.600104'        ##上汽集团 
    # ]
    # df = genSymbolsReturn(
    #    symbols
    #     ) # 生成每日收益率序列
 
    # meanVariance = MeanVariance()
    # # 最优夏普
    # w = meanVariance.optWeights(df = df,type="minSharpe")
    # print("====MV=最优夏普====")
    # print(w)
    # # 最小方差
    # w = meanVariance.optWeights(df = df,type="minVar")
    # print("====MV=最小方差====")
    # print(w)
    # print("------------BlackLitterman------------")
    # print("------------利用贝叶斯收缩计算后验收益率然后代入马科维茨模型 ------------")
    # bl = BlackLitterman()
    # mk = genMarketValueWeight(symbols=symbols) # 最后一日数据的市值权重
    # # 计算后验夏普率
    # posteriorCombinedReturn = bl.getPosteriorCombinedReturn(df=df,marketValueWeight=mk)
    # print(posteriorCombinedReturn)
    # w = meanVariance.optWeights(df = df,type="minSharpe",expectedRet =posteriorCombinedReturn )
    # print(w)
    # w = meanVariance.optWeights(df = df,type="minVar",expectedRet =posteriorCombinedReturn )
    # print(w)
    # # ===========三方库===========
    # # # Optimize for maximal Sharpe ratio
    # mu = expected_returns.mean_historical_return(df,returns_data = True)
    # S = risk_models.sample_cov(df)
    # print(mu)
    # print(S)
    # ef = EfficientFrontier(mu, S)
    # raw_weights = ef.max_sharpe()
    # print(raw_weights)
    # k = Kelly()
    # k.optWeights(df = df)
    
# https://zhuanlan.zhihu.com/p/135320360
    p =0.6 # 胜率
    b = 1  # 赔率
    f =(p*b-(1-p))/b # 仓位值
    import math
    print("凯利值即仓位：",f)
    # 用 f代入
    maxf =  p*math.log(1+b*f)+(1-p)*math.log(1-f)
    # 用 0.5f 代入
    halfmaxf =  p*math.log(1+b*0.5*f)+(1-p)*math.log(1-0.5*f)
    print("全凯利预期收益：",maxf)
    print("半凯利预期收益：",halfmaxf)



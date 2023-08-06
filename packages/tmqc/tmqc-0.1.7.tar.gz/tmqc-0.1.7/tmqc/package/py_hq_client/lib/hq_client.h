/*
*	行情仓库对应的客户端DLL
*/
#pragma once
#ifndef __HQ_DEPOT_CLIENT_H__
#define __HQ_DEPOT_CLIENT_H__

#ifdef HQCLIENT_EXPORTS
#define HQCLIENT_API __declspec(dllexport)
#else
#define HQCLIENT_API //__declspec(dllimport)
#endif


#ifdef __cplusplus
extern "C" {
#endif

// 启动
HQCLIENT_API int hq_client_start(int argc = 0, char** argv = nullptr);

// 停止
HQCLIENT_API void hq_client_stop();


#ifdef __cplusplus
} /* extern "C" */
#endif


#include <vector>
#include <string>

#pragma pack(push,1)

// 行情结构体
namespace HQS {

    // 交易所类型
    enum MARKET_TYPE {
        // 任意交易所
        AnyMT       = 0,
        // 上交所
        ShangHai    = 1,
        // 深交所
        ShenZhen    = 2,
    };

    // 证券类型
    enum HQ_TYPE {
        // 任意类型
        AnyHQ       = 0,
        // 股票类型
        Stock       = 1,
        // 期权类型
        Option      = 2,
        // 期货类型
        Future      = 3,
    };

    // K 线类型
    enum BAR_TYPE {
        // 日线类型
        Day         = 0,
        // 分钟线类型
        Minute      = 1,
        // tick线类型
        Tick        = 2,
    };

    // 认购/认沽
    enum COP {
        // 认购
        CALL        = 0,
        // 认沽
        PUT         = 1,
    };

    // 时间点
    struct TimePos {
        // 日期 yyyymmdd
        int date      = 0;
        // 时间 HHMMSSmmm
        int time      = 0;
    };

    // 证券基本信息
    struct CodeInfo {
        // 交易所
        MARKET_TYPE mk  = MARKET_TYPE::ShangHai;
        // 证券类型
        HQ_TYPE hq      = HQ_TYPE::Option;
        // 证券代码 - 0 为请求全部行情 - 服务端会根据情况进行下发
        int code        = 0;
    };

    // 行情信息
    struct HQInfo {
        // 证券基本信息
        CodeInfo cinfo;
        // 时间点
        TimePos tpos;

        // 行情
        double open      = 0.0;
        double high      = 0.0;
        double low       = 0.0;
        double close     = 0.0;
        double volume    = 0.0;
    };

    // 期权基本信息
    struct OptInfo {
		// 证券代码 
		int code                = 10001000;
        // 交易日
        int yyyymmdd            = 20010101;
        // 期数
        int yyyymm              = 200101;
        // 交易所
        MARKET_TYPE mk          = MARKET_TYPE::ShangHai;
        // 认购/认沽
        COP cop                 = COP::CALL;
        // 行权日
        int exercise_date       = 20010101;
        // 交易代码
        std::string trade_code  = "510050C2103A03000";
        // 合约简称
        std::string nick_name   = "50ETF购3月2957A";
        // 行权价格
        double exercise_price   = 0.0;
        // 合约单位
        int contract_unit       = 10000;
    };

}

#pragma pack(pop)


// 推送数据
HQCLIENT_API void hq_client_push(HQS::BAR_TYPE bar, const HQS::HQInfo& hq);

// 获取数据
HQCLIENT_API const std::vector<HQS::HQInfo>& hq_client_fetch(HQS::BAR_TYPE bar, const HQS::CodeInfo& cinfo, const HQS::TimePos& from, const HQS::TimePos& to);

// 订阅实时行情(tick级别) - 每次断开后需要重新订阅
HQCLIENT_API void hq_client_subscribe(const HQS::CodeInfo& cinfo);

// 获取实时行情 - 若不存在则返回空
HQCLIENT_API const HQS::HQInfo* hq_client_try_take();

// 当前是否连接中(持续订阅)
HQCLIENT_API bool hq_client_is_connect();

// 推送当日期权情况
HQCLIENT_API void hq_client_push_opt_info(const HQS::OptInfo& optInfo);

// 获取某日期权列表信息 - 可包括当日
HQCLIENT_API const std::vector<HQS::OptInfo>& hq_client_get_day_opt_info(int yyyymmdd);


#endif	// __HQ_DEPOT_CLIENT_H__
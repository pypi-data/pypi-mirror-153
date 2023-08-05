#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("..")
sys.path.append("./interface")
sys.path.append("./libs")
sys.path.append("./insight")
sys.path.insert(0, "..")
sys.path.insert(1, "./interface")
sys.path.insert(2, "./libs")
sys.path.insert(3, "./insight")
from com.interface.mdc_gateway_base_define import ESubscribeActionType, ESecurityIDSource, ESecurityType, \
    EMarketDataType, MDPlaybackExrightsType
import com.insight.common
import com.insight.query
import com.insight.playback
import com.insight.subscribe


# ************************************处理数据订阅************************************
# 处理订阅的股票Tick数据，格式为json格式
# 订阅的证券类型为ESecurityType.StockType
def onSubscribe_MD_TICK_StockType(mdStock):
    pass
    # print(mdStock)


# 处理订阅的指数Tick数据，格式为json格式
# 订阅的证券类型为ESecurityType.IndexType
def onSubscribe_MD_TICK_IndexType(mdIndex):
    pass
    # print(mdIndex)


# 处理订阅的债券Tick数据，格式为json格式
# 订阅的证券类型为ESecurityType.BondType
def onSubscribe_MD_TICK_BondType(mdBond):
    pass
    # print(mdBond)


# 处理订阅的基金Tick数据，格式为json格式
# 订阅的证券类型为ESecurityType.FundType
def onSubscribe_MD_TICK_FundType(mdFund):
    pass
    # print(mdFund)


# 处理订阅的期权Tick数据，格式为json格式
# 订阅的证券类型为ESecurityType.OptionType
def onSubscribe_MD_TICK_OptionType(mdOption):
    pass
    # print(mdOption)


# 处理订阅的期权Tick数据，格式为json格式
# 订阅的证券类型为ESecurityType.OptionType
def onSubscribe_MD_TICK_FuturesType(mdFuture):
    pass
    # print(mdFuture)


# 处理订阅的逐笔成交，格式为json格式
# 订阅的证券类型为ESecurityType.MD_TRANSACTION
def onSubscribe_MD_TRANSACTION(mdTransaction):
    pass
    # print(mdTransaction)


# 处理订阅的逐笔委托，格式为json格式
# 订阅的证券类型为ESecurityType.MD_ORDER
def onSubscribe_MD_ORDER(mdOrder):
    pass
    # print(mdOrder)


# 处理订阅的K线指标模型，格式为json格式
# 订阅的数据类型为EMarketDataType.MD_KLINE_15S 返回#15秒钟K线
# 订阅的数据类型为EMarketDataType.MD_KLINE_1MIN 返回#1分钟K线
# 订阅的数据类型为EMarketDataType.MD_KLINE_5MIN 返回#5分钟K线
# 订阅的数据类型为EMarketDataType.MD_KLINE_15MIN 返回#15分钟K线
# 订阅的数据类型为EMarketDataType.MD_KLINE_30MIN 返回#30分钟K线
# 订阅的数据类型为EMarketDataType.MD_KLINE_60MIN 返回#60分钟K线
# 订阅的数据类型为EMarketDataType.MD_KLINE_1D 返回#日K线
def onSubscribe_MD_KLINE(marketdatajson):
    if marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_15S:  # 15秒钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_1MIN:  # 1分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_5MIN:  # 5分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_15MIN:  # 15分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_30MIN:  # 30分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_60MIN:  # 60分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_1D:  # 日K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)

    # print(marketdatajson)


# 处理订阅的资金流向数据，格式为json格式
# 订阅的证券类型为ESecurityType.AD_FUND_FLOW_ANALYSIS
def onSubscribe_AD_FUND_FLOW_ANALYSIS(mdFundFlowAnalysis):
    pass
    # print(mdFundFlowAnalysis)


# 处理订阅的融券通数据，格式为json格式
# 订阅的证券类型为ESecurityType.MD_SECURITY_LENDING
def onSubscribe_MD_SECURITY_LENDING(mdSecurityLending):
    pass
    # print(mdSecurityLending)


# ************************************处理回放数据************************************
# 处理回放的股票Tick数据，格式为json格式
# 回放的证券类型为ESecurityType.StockType
def onPlayback_MD_TICK_StockType(mdStock):
    pass
    print(mdStock)


# 处理回放的指数Tick数据，格式为json格式
# 回放的证券类型为ESecurityType.IndexType
def onPlayback_MD_TICK_IndexType(mdIndex):
    pass
    # print(mdIndex)


# 处理回放的债券Tick数据，格式为json格式
# 回放的证券类型为ESecurityType.BondType
def onPlayback_MD_TICK_BondType(mdBond):
    pass
    # print(mdBond)


# 处理回放的基金Tick数据，格式为json格式
# 回放的证券类型为ESecurityType.FundType
def onPlayback_MD_TICK_FundType(mdFund):
    pass
    # print(mdFund)


# 处理回放的期权Tick数据，格式为json格式
# 回放的证券类型为ESecurityType.OptionType
def onPlayback_MD_TICK_OptionType(mdOption):
    pass
    # print(mdOption)


# 处理回放的期权Tick数据，格式为json格式
# 回放的证券类型为ESecurityType.OptionType
def onPlayback_MD_TICK_FuturesType(mdFuture):
    pass
    # print(mdFuture)


# 处理回放的逐笔成交，格式为json格式
# 回放的证券类型为ESecurityType.MD_TRANSACTION
def onPlayback_MD_TRANSACTION(mdTransaction):
    pass
    # print(mdTransaction)


# 处理回放的逐笔委托，格式为json格式
# 回放的证券类型为ESecurityType.MD_ORDER
def onPlayback_MD_ORDER(mdOrder):
    pass
    # print(mdOrder)


# 处理回放的K线指标模型，格式为json格式
# 回放的数据类型为EMarketDataType.MD_KLINE_15S 返回#15秒钟K线
# 回放的数据类型为EMarketDataType.MD_KLINE_1MIN 返回#1分钟K线
# 回放的数据类型为EMarketDataType.MD_KLINE_5MIN 返回#5分钟K线
# 回放的数据类型为EMarketDataType.MD_KLINE_15MIN 返回#15分钟K线
# 回放的数据类型为EMarketDataType.MD_KLINE_30MIN 返回#30分钟K线
# 回放的数据类型为EMarketDataType.MD_KLINE_60MIN 返回#60分钟K线
# 回放的数据类型为EMarketDataType.MD_KLINE_1D 返回#日K线
def onPlayback_MD_KLINE(marketdatajson):
    if marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_15S:  # 15秒钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_1MIN:  # 1分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_5MIN:  # 5分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_15MIN:  # 15分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_30MIN:  # 30分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_60MIN:  # 60分钟K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)
    elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_1D:  # 日K线
        mdKLine = marketdatajson["mdKLine"]
        pass
        # print(mdKLine)

    # print(marketdatajson)


# 处理回放的资金流向数据，格式为json格式
# 回放的证券类型为ESecurityType.AD_FUND_FLOW_ANALYSIS
def onPlayback_AD_FUND_FLOW_ANALYSIS(mdFundFlowAnalysis):
    pass
    # print(mdFundFlowAnalysis)


# 处理回放的融券通数据，格式为json格式
# 回放的证券类型为ESecurityType.MD_SECURITY_LENDING
def onPlayback_MD_SECURITY_LENDING(mdSecurityLending):
    pass
    # print(mdSecurityLending)


# 处理回放的状态，格式为string格式
def onPlaybackStatus(status):
    pass
    # print(status)


# 处理回放请求返回结果，格式为string格式
def onPlaybackResponse(response):
    pass
    # print(response)


def onPlaybackControlResponse(response):
    pass
    print(response)


# ************************************处理查询请求返回结果************************************
# 处理查询历史上所有的指定证券的基础信息 query_mdcontant_type()的返回结果
# 处理查询今日最新的指定证券的基础信息 query_last_mdcontant_type()的返回结果
# 处理查询历史上所有的指定证券的基础信息 query_mdcontant_id()的返回结果
# 处理查询今日最新的指定证券的基础信息 query_last_mdcontant_id()的返回结果
# 处理查询指定证券的ETF的基础信息 query_ETFinfo()的返回结果
# 处理查询指定证券的最新一条Tick数据 query_last_mdtick()的返回结果
def onQueryResponse(queryresponse):
    pass
    for resonse in iter(queryresponse):
        print(resonse)


# ************************************用户登录************************************
# 登陆
# user 用户名
# password 密码
def login():
    # 登陆前 初始化
    uatuser = "USER016189SIT001"
    uatpassword = "123!@#qweQWE"
    user = "USER016189TMN01"
    password = "User016189"
    result = com.insight.common.login(user, password)
    print(result)


# ************************************数据订阅************************************
# 根据证券数据来源订阅行情数据,由三部分确定行情数据
# 行情源(SecurityIdSource):XSHG(沪市)|XSHE(深市)|...
# 证券类型(SecurityType):BondType(债)|StockType(股)|FundType(基)|IndexType(指)|OptionType(期权)|...
# 数据类型(MarketDataTypes):MD_TICK(快照)|MD_TRANSACTION(逐笔成交)|MD_ORDER(逐笔委托)|...
def subscribe_by_type():
    # element
    # params1: ESecurityIDSource枚举值 --行情源
    # params2: ESecurityType的枚举值 --证券类型
    # params3: EMarketDataType的枚举值集合 --数据类型
    datatype = ESubscribeActionType.COVERAGE
    marketdatatypes = {"ESecurityIDSource": ESecurityIDSource.XSHG, "ESecurityType": ESecurityType.StockType,
                       "EMarketDataType": EMarketDataType.MD_SECURITY_LENDING}
    com.insight.subscribe.subscribe_by_type(marketdatatypes, datatype)


# 根据证券ID来源订阅行情数据
def subscribe_by_id():
    datatype = ESubscribeActionType.COVERAGE
    HTSCSecurityID = {"HTSCSecurityID": "002371.SZ", "ESecurityType": ESecurityType.StockType,
                      "EMarketDataType": EMarketDataType.MD_TICK}
    com.insight.subscribe.subscribe_by_id(HTSCSecurityID, datatype)


# ************************************数据查询************************************
# 查询findata数据
def query_fin_info():
    query_type = 1102010003
    params = {"HTSC_SECURITY_ID": "510050.SH", "START_DATE": "20210101", "END_DATE": "20210107"}
    result = com.insight.query.query_fin_info(query_type, params)
    if isinstance(result, list):
        for response in iter(result):
            print(response)
    else:
        print(result)


# 查询历史上所有的指定证券的基础信息 --结果返回在onQueryResponse
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_mdcontant_type():
    # params:security_idsource 为 ESecurityIDSource枚举值
    # params:security_type 为 ESecurityType枚举值
    # 沪市 股票
    security_idsource = ESecurityIDSource.XSHG
    security_type = ESecurityType.StockType
    idsource_and_type = {"ESecurityIDSource": security_idsource, "ESecurityType": security_type}
    com.insight.query.query_basicInfo_by_type(idsource_and_type, False)


# 查询今日最新的指定证券的基础信息 -- 结果返回在onQueryResponse
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_last_mdcontant_type():
    # 按市场查询
    # 沪市 股票

    security_idsource = ESecurityIDSource.XSHG
    security_type = ESecurityType.StockType
    idsource_and_type = {"ESecurityIDSource": security_idsource, "ESecurityType": security_type}
    com.insight.query.query_basicInfo_by_type(idsource_and_type, True)


# 查询历史上所有的指定证券的基础信息 -- 结果返回在onQueryResponse
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_mdcontant_id():
    # params:security_idsource 为 ESecurityIDSource枚举值
    # params:security_type 为 ESecurityType枚举值
    # params:security_id_list 为 标的集合
    security_id_list = ["601688.SH", "002714.SZ"]  # 置空表示不额外查询某些标的
    com.insight.query.query_basicInfo_by_id(security_id_list, False)


# 查询今日最新的指定证券的基础信息 -- 结果返回在onQueryResponse
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_last_mdcontant_id():
    # 按市场查询
    # 沪市 股票

    # params:security_id_list 为 标的集合
    security_id_list = ["601688.SH"]  # 置空表示不额外查询某些标的
    com.insight.query.query_basicInfo_by_id(security_id_list, True)


# 查询指定证券的ETF的基础信息 -- 在data_handle.py 数据回调接口OnMarketData()中marketdata.marketDataType = MD_ETF_BASICINFO
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_ETFinfo():
    # params:securityIDSource 为 ESecurityIDSource枚举值
    # params:securityType 为 ESecurityType枚举值
    com.insight.query.query_ETFinfo(ESecurityIDSource.XSHG, ESecurityType.FundType)


# 查询指定证券的最新一条Tick数据 -- 在data_handle.py 数据回调接口OnMarketData()中marketdata.marketDataType = MD_TICK
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_last_mdtick():
    # params:security_idsource 为 ESecurityIDSource枚举值
    # params:security_type 为 ESecurityType枚举值
    # 沪市 股票
    com.insight.query.query_last_tick_by_type(ESecurityIDSource.XSHG, ESecurityType.StockType)


# ************************************回放************************************
# 回放接口 (注意：securitylist 和 securityIdList取并集!!!)
# 回放限制
# 对于回放而言，时间限制由股票只数和天数的乘积决定，要求 回放只数 × 回放天数 × 证券权重 ≤ 450，交易时间段内回放功能 乘积<=200。
# Tick/Transaction/Order回放时间范围限制是30天，每支证券权重为1，即可以回放15只股票30天以内的数据或450支股票1天内数据。
# 日K数据回放时间范围限制是365天，每支证券权重为0.005。
# 分钟K线数据回放时间范围限制是90天，每支证券权重0.05。
# 数据最早可以回放到 2017年1月2日
def play_back():
    # 回放数据类型 EMarketDataType 详情请参阅 数据手册EMarketDataType
    # 示例：MD_TICK
    marketdata_type = EMarketDataType.MD_TICK

    # 是否复权 EPlaybackTaskStatus 详情请参阅 数据手册EPlaybackTaskStatus
    # 示例： 不复权
    exrights_type = MDPlaybackExrightsType.DEFAULT_EXRIGHTS_TYPE

    # 回放时间起：start_time 注意格式
    # 回放时间止：stop_time  注意格式
    # 回放时间起止间隔 不超过上述 时间范围限制
    start_time = "20220420090000"
    stop_time = "20220420150000"

    # security_id_list 为回放 标的列表,不需要使用请置空
    security_id_list = ["601688.SH", "000014.SZ"]

    # 特别注意！！！！
    # security_id_list 注意回放限制
    com.insight.playback.playback(security_id_list, marketdata_type, exrights_type, start_time, stop_time)


# 盘中回放接口 --securitylist 和 securityIdList取并集
# Can only query data for one day
def play_back_oneday():
    # 回放数据类型 EMarketDataType 详情请参阅 数据手册EMarketDataType
    # 示例：MD_TICK
    marketdata_type = EMarketDataType.MD_TICK

    # 是否复权 EPlaybackTaskStatus 详情请参阅 数据手册EPlaybackTaskStatus
    # 示例： 不复权
    exrights_type = MDPlaybackExrightsType.DEFAULT_EXRIGHTS_TYPE

    # 是否按照mdtime排序
    isMdtime = True

    # security_id_list 为回放 标的列表,不需要使用请置空
    security_id_list = ["601688.SH", "000014.SZ"]

    # 特别注意！！！！
    # security_id_list 注意回放限制
    com.insight.playback.play_back_oneday(security_id_list, marketdata_type, exrights_type, isMdtime)


# 获取当前版本号
def get_version():
    print(com.insight.common.get_version())


# 释放资源
def fini():
    com.insight.common.fini()


# 使用指导：登陆 -> 订阅/查询/回放 -> 退出
def main():
    # 登陆部分调用
    get_version()
    login()
    # 订阅部分接口调用

    # subscribe_by_type()
    # subscribe_by_id()
    # 查询部分接口调用
    query_fin_info()
    # query_mdcontant_type()
    # query_last_mdcontant_type()
    # query_mdcontant_id()
    # query_last_mdcontant_id()

    # query_ETFinfo()
    # query_last_mdtick()
    # 回放部分接口调用
    # play_back()
    # play_back_oneday()
    # 退出释放资源
    fini()


if __name__ == "__main__":
    # insight SDK 采用网络异步方式 ---- 请求访问和数据返回 异步交互
    # 这里是 functional_test.py 是 登陆、订阅、查询、回测（也称回放）操作部分
    # 以订阅为例： functional_test.py 中，执行登陆->订阅,操作结束后,数据通过 data_handle.py中 OnRecvMarkertData()的成员方法回调返回（回调详情请参照使用手册）
    main()

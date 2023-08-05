#!/usr/bin/python3
import json
from com.functional_test import onSubscribe_MD_TICK_StockType, onSubscribe_MD_TICK_IndexType, \
    onSubscribe_MD_TICK_BondType, onSubscribe_MD_TICK_FundType, onSubscribe_MD_TICK_OptionType, \
    onSubscribe_MD_TICK_FuturesType, onSubscribe_MD_KLINE, onSubscribe_MD_TRANSACTION, onSubscribe_MD_ORDER, \
    onSubscribe_AD_FUND_FLOW_ANALYSIS, onSubscribe_MD_SECURITY_LENDING, onPlayback_MD_TICK_FuturesType, \
    onPlayback_MD_TRANSACTION, onPlayback_MD_ORDER, onPlayback_MD_KLINE, onPlayback_AD_FUND_FLOW_ANALYSIS, \
    onPlayback_MD_SECURITY_LENDING, onPlayback_MD_TICK_OptionType, onPlayback_MD_TICK_FundType, \
    onPlayback_MD_TICK_BondType, onPlayback_MD_TICK_IndexType, onPlayback_MD_TICK_StockType, onPlaybackStatus, \
    onPlaybackResponse, onPlaybackControlResponse, onQueryResponse
from com.interface.mdc_gateway_interface import GatewayInterface
from com.interface.mdc_gateway_base_define import EMarketDataType, EPlaybackTaskStatus

global interface
interface = GatewayInterface()


def get_interface():
    return interface


class OnRecvMarketData:
    def __init__(self):
        pass

    def OnMarketData(self, marketdatajson):
        try:
            if marketdatajson["marketDataType"] == EMarketDataType.MD_TICK:  # .MD_TICK 快照
                if "mdStock" in marketdatajson:  # 股票
                    onSubscribe_MD_TICK_StockType(marketdatajson["mdStock"])
                elif "mdIndex" in marketdatajson:  # 指数
                    onSubscribe_MD_TICK_IndexType(marketdatajson["mdIndex"])
                elif "mdBond" in marketdatajson:  # 债券
                    onSubscribe_MD_TICK_BondType(marketdatajson["mdBond"])
                elif "mdFund" in marketdatajson:  # 基金
                    onSubscribe_MD_TICK_FundType(marketdatajson["mdFund"])
                elif "mdOption" in marketdatajson:  # 期权
                    onSubscribe_MD_TICK_OptionType(marketdatajson["mdOption"])
                elif "mdFuture" in marketdatajson:  # 期权
                    onSubscribe_MD_TICK_FuturesType(marketdatajson["mdFuture"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_TRANSACTION:  # .MD_TRANSACTION:逐笔成交
                if "mdTransaction" in marketdatajson:
                    onSubscribe_MD_TRANSACTION(marketdatajson["mdTransaction"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_ORDER:  # .MD_ORDER:逐笔委托
                if "mdOrder" in marketdatajson:
                    onSubscribe_MD_ORDER(marketdatajson["mdOrder"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_CONSTANT:  # .MD_CONSTANT:静态信息
                if "mdConstant" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdConstant"]["HTSCSecurityID"])
                # MD_KLINE:实时数据只提供15S和1MIN K线
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_15S or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_1MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_5MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_15MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_30MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_60MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_1D:
                if "mdKLine" in marketdatajson:
                    onSubscribe_MD_KLINE(marketdatajson)
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_TWAP_1S or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_TWAP_1MIN:  # .TWAP:TWAP数据
                if "mdTwap" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdTwap"]["MDTime"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_VWAP_1S or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_VWAP_1MIN:  # .VWAP:VWAP数据
                if "mdVwap" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdVwap"]["MDTime"])
            elif marketdatajson["marketDataType"] == EMarketDataType.AD_FUND_FLOW_ANALYSIS:  # .AD_FUND_FLOW_ANALYSIS:
                if "mdFundFlowAnalysis" in marketdatajson:
                    onSubscribe_AD_FUND_FLOW_ANALYSIS(marketdatajson["mdFundFlowAnalysis"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_ETF_BASICINFO:  # .MD_ETF_BASICINFO:ETF成分股信息
                if "mdETFBasicInfo" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdETFBasicInfo"]["MDTime"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_SECURITY_LENDING:  # .MD_SECURITY_LENDING
                if "mdSecurityLending" in marketdatajson:
                    onSubscribe_MD_SECURITY_LENDING(marketdatajson["mdSecurityLending"])
        except BaseException as e:
            print("onMarketData error happened!" + marketdatajson)
            print(e)

    def OnPlaybackMarketData(self, marketdatajson):
        try:
            if marketdatajson["marketDataType"] == EMarketDataType.MD_TICK:  # .MD_TICK 快照
                if "mdStock" in marketdatajson:  # 股票
                    onPlayback_MD_TICK_StockType(marketdatajson["mdStock"])
                elif "mdIndex" in marketdatajson:  # 指数
                    onPlayback_MD_TICK_IndexType(marketdatajson["mdIndex"])
                elif "mdBond" in marketdatajson:  # 债券
                    onPlayback_MD_TICK_BondType(marketdatajson["mdBond"])
                elif "mdFund" in marketdatajson:  # 基金
                    onPlayback_MD_TICK_FundType(marketdatajson["mdFund"])
                elif "mdOption" in marketdatajson:  # 期权
                    onPlayback_MD_TICK_OptionType(marketdatajson["mdOption"])
                elif "mdFuture" in marketdatajson:  # 期权
                    onPlayback_MD_TICK_FuturesType(marketdatajson["mdFuture"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_TRANSACTION:  # .MD_TRANSACTION:逐笔成交
                if "mdTransaction" in marketdatajson:
                    onPlayback_MD_TRANSACTION(marketdatajson["mdTransaction"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_ORDER:  # .MD_ORDER:逐笔委托
                if "mdOrder" in marketdatajson:
                    onPlayback_MD_ORDER(marketdatajson["mdOrder"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_CONSTANT:  # .MD_CONSTANT:静态信息
                if "mdConstant" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdConstant"]["HTSCSecurityID"])
                # MD_KLINE:实时数据只提供15S和1MIN K线
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_KLINE_15S or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_1MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_5MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_15MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_30MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_60MIN or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_KLINE_1D:
                if "mdKLine" in marketdatajson:
                    onPlayback_MD_KLINE(marketdatajson)
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_TWAP_1S or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_TWAP_1MIN:  # .TWAP:TWAP数据
                if "mdTwap" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdTwap"]["MDTime"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_VWAP_1S or marketdatajson[
                "marketDataType"] == EMarketDataType.MD_VWAP_1MIN:  # .VWAP:VWAP数据
                if "mdVwap" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdVwap"]["MDTime"])
            elif marketdatajson["marketDataType"] == EMarketDataType.AD_FUND_FLOW_ANALYSIS:  # .AD_FUND_FLOW_ANALYSIS:
                if "mdFundFlowAnalysis" in marketdatajson:
                    onPlayback_AD_FUND_FLOW_ANALYSIS(marketdatajson["mdFundFlowAnalysis"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_ETF_BASICINFO:  # .MD_ETF_BASICINFO:ETF成分股信息
                if "mdETFBasicInfo" in marketdatajson:
                    timestr = json.dumps(marketdatajson["mdETFBasicInfo"]["MDTime"])
            elif marketdatajson["marketDataType"] == EMarketDataType.MD_SECURITY_LENDING:  # .MD_SECURITY_LENDING
                if "mdSecurityLending" in marketdatajson:
                    onPlayback_MD_SECURITY_LENDING(marketdatajson["mdSecurityLending"])
        except BaseException as e:
            print("onMarketData error happened!" + marketdatajson)
            print(e)

    def OnPlaybackPayload(self, playloadstr):
        try:
            interface.set_service_value(4)
            # print(playloadstr)
            playloadjson = json.loads(playloadstr)
            if "taskId" in playloadjson:
                print("Parse Message id:" + playloadjson["taskId"])
            marketDataStream = playloadjson["marketDataStream"]
            if "isFinished" in marketDataStream:
                print(marketDataStream)
                print("OnPlaybackPayload total number=%d, serial=%d, isfinish=%d" % (
                    marketDataStream["totalNumber"], marketDataStream["serial"], marketDataStream["isFinished"]))
            else:
                print("OnPlaybackPayload total number=%d, serial=%d" % (
                    marketDataStream["totalNumber"], marketDataStream["serial"]))
            marketDataList = marketDataStream["marketDataList"]
            marketDatas = marketDataList["marketDatas"]
            for data in iter(marketDatas):
                self.OnPlaybackMarketData(data)
        except BaseException as e:
            print(e)

    def OnPlaybackStatus(self, statusstr):
        statusresult = "error happened in OnPlaybackStatus"
        try:
            statusjson = json.loads(statusstr)
            statusresult = f'OnPlaybackStatus playback status={statusjson["taskStatus"]}'
            interface.set_service_value(statusjson["taskStatus"])
            if statusjson["taskStatus"] == EPlaybackTaskStatus.CANCELED or statusjson[
                "taskStatus"] == EPlaybackTaskStatus.COMPLETED or statusjson[
                "taskStatus"] == EPlaybackTaskStatus.FAILED:
                interface.mutex.acquire()
                if statusjson["taskId"] in interface.task_id_status:
                    del interface.task_id_status[statusjson["taskId"]]
                interface.mutex.release()
        except BaseException as e:
            print(e)
        onPlaybackStatus(statusresult)

    def OnPlaybackResponse(self, responsestr):
        responseresult = "error happened in OnPlaybackResponse"
        try:
            responsejson = json.loads(responsestr)
            if "isSuccess" in responsejson:
                if responsejson["isSuccess"]:
                    responseresult = f'OnPlaybackResponse Message id: {responsejson["taskId"]}'
                else:
                    responseresult = f'OnPlaybackResponse failed --> {responsejson["errorContext"]["message"]}'
            else:
                responseresult = f'OnPlaybackResponse :{responsestr}'
        except BaseException as e:
            print(e)
        onPlaybackResponse(responseresult)

    def OnPlaybackControlResponse(self, responsestr):
        responseresult = "error happened in OnPlaybackControlResponse"
        try:
            responsejson = json.loads(responsestr)
            if "isSuccess" in responsejson:
                if responsejson["isSuccess"]:
                    print(responsejson["currentReplayRate"])
                    responseresult = f'OnPlaybackControlResponse Message id:{responsejson["taskId"]}'
                else:
                    responseresult = f'OnPlaybackControlResponse failed!!! reason ->{responsejson["errorContext"]["message"]}'
            else:
                responseresult = f'OnPlaybackControlResponse :{responsestr}'
        except BaseException as e:
            print(e)
        onPlaybackControlResponse(responseresult)

    def OnServiceMessage(self, marketDataStr):
        try:
            interface.set_service_value(1)
            marketDataJson = json.loads(marketDataStr)
            self.OnMarketData(marketDataJson)
        except BaseException as e:
            print("error happened in OnServiceMessage")
            print(e)

    def OnSubscribeResponse(self, responsestr):
        try:
            responsejson = json.loads(responsestr)
            issucess = responsejson["isSuccess"]
            if issucess:
                print("Subscribe Success!!!")
            else:
                # print(gateway.getErrorCodeValue(response.errorContext.errorCode))
                print("Subscribe failed!!! reason ->" + (responsestr))
        except BaseException as e:
            print("error happened in OnServiceMessage")
            print(e)

    def OnFinInfoQueryResponse(self, responsestr):
        try:
            responsejson = json.loads(responsestr)
            print(responsejson)
            if "isSuccess" in responsejson:
                if responsejson["isSuccess"]:
                    print("OnFinInfoQueryResponse sucess")
                else:
                    print("OnFinInfoQueryResponse failed!!! reason -> %s" % (responsejson["errorContext"]["message"]))
                    interface.set_query_exit(True)
            else:
                print("OnFinInfoQueryResponse failed!!! reason -> %s" % (responsejson["errorContext"]["message"]))
                interface.set_query_exit(True)
        except BaseException as e:
            print("error happened in OnFinInfoQueryResponse")
            print(e)

    def OnQueryResponse(self, responsestr):
        try:
            responsejson = json.loads(responsestr)
            if "isSuccess" in responsejson:
                if responsejson["isSuccess"]:
                    marketDataStream = responsejson["marketDataStream"]
                    print(
                        "query response total number=%d, serial=%d" % (
                            marketDataStream["totalNumber"], marketDataStream["serial"]))
                    marketDataList = marketDataStream["marketDataList"]
                    marketDatas = marketDataList["marketDatas"]
                    onQueryResponse(marketDatas)
                    if "isFinished" in marketDataStream:
                        interface.set_query_exit(marketDataStream["isFinished"] == 1)
                else:
                    print("OnQueryResponse failed!!! reason -> %s" % (responsejson["errorContext"]["message"]))
                    interface.set_query_exit(True)
            else:
                print("OnQueryResponse failed!!! reason -> %s" % (responsejson["errorContext"]["message"]))
                interface.set_query_exit(True)
        except BaseException as e:
            print("error happened in OnQueryResponse")
            print(e)

    def OnGeneralError(self, contextstr):
        try:
            contextjson = json.loads(contextstr)
            # print(gateway.getErrorCodeValue(context.errorCode))
            print("OnGeneralError!!! reason -> %s" % (contextjson["message"]))
        except BaseException as e:
            print("error happened in OnGeneralError")
            print(e)

    def OnLoginSuccess(self):
        interface.login_success = True
        print("OnLoginSuccess!!!")

    def OnLoginFailed(self, error_no, message):
        interface.login_success = False
        try:
            print("OnLoginFailed!!! reason -> %s" % message)
        except BaseException as e:
            print("error happened in OnLoginFailed")
            print(e)

    def OnNoConnections(self):
        print("OnNoConnections!!!")
        interface.set_reconnect(True)
        interface.set_no_connections(True)

    def OnReconnect(self):
        print("OnReconnect!!!")
        interface.set_reconnect(True)
        interface.set_reconnect_count(interface.get_reconnect_count() + 1)

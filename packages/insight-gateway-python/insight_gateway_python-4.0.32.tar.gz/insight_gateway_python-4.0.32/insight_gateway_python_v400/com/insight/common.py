#!/usr/bin/python3
# -*- coding: utf-8 -*-

import com.data_handle
from com.interface.mdc_gateway_base_define import EMarketDataType, ESecurityIDSource, ESecurityType, \
    ESubscribeActionType, MDPlaybackExrightsType, GateWayServerConfig, QueryServerConfig


# 登陆
# params1: 用户名
# params2: 密码
# params3:
# params2: 密码
def login(Username, Password, IP=GateWayServerConfig.IP, Port=GateWayServerConfig.PORT,
          backupIP=GateWayServerConfig.BACK_LIST):
    # 登陆前 初始化
    result = ""
    if not ((type(Port) == int) and 0 < Port < GateWayServerConfig.MaxPortNum):
        result = "Port has invalid format"
        return result
    Initial()
    ret = com.data_handle.get_interface().login(IP, Port, Username, Password, GateWayServerConfig.ISTOKEN,
                                                GateWayServerConfig.CERTFOLDER, backupIP,
                                                QueryServerConfig.QUERY_ADDRESS,
                                                QueryServerConfig.QUERY_CERT,
                                                QueryServerConfig.QUERY_IS_SSL)

    if ret != 0:
        result = f'(login failed!!! reason:{com.data_handle.get_interface().get_error_code_value(ret)})'
        return result
    result = "login success"
    return result


def loginUAT(Username, Password, IP=GateWayServerConfig.UAT_IP, Port=GateWayServerConfig.UAT_PORT,
             backupIP=GateWayServerConfig.UAT_BACK_LIST):
    # 登陆前 初始化
    result = ""
    if not ((type(Port) == int) and 0 < Port < GateWayServerConfig.MaxPortNum):
        result = "Port has invalid format"
        return result
    Initial()
    ret = com.data_handle.get_interface().login(IP, Port, Username, Password, GateWayServerConfig.ISTOKEN,
                                                GateWayServerConfig.CERTFOLDER, backupIP,
                                                QueryServerConfig.UAT_QUERY_ADDRESS,
                                                QueryServerConfig.UAT_QUERY_CERT,
                                                QueryServerConfig.UAT_QUERY_IS_SSL)

    if ret != 0:
        result = f'(login failed!!! reason:{com.data_handle.get_interface().get_error_code_value(ret)})'
        return result
    result = "login success"
    return result


def loginSIT(Username, Password, IP=GateWayServerConfig.SIT_IP, Port=GateWayServerConfig.SIT_PORT,
             backupIP=GateWayServerConfig.SIT_BACK_LIST):
    # 登陆前 初始化
    result = ""
    if not ((type(Port) == int) and 0 < Port < GateWayServerConfig.MaxPortNum):
        result = "Port has invalid format"
        return result
    Initial()
    ret = com.data_handle.get_interface().login(IP, Port, Username, Password, GateWayServerConfig.ISTOKEN,
                                                GateWayServerConfig.CERTFOLDER, backupIP,
                                                QueryServerConfig.SIT_QUERY_ADDRESS,
                                                QueryServerConfig.SIT_QUERY_CERT,
                                                QueryServerConfig.SIT_QUERY_IS_SSL)

    if ret != 0:
        result = f'(login failed!!! reason:{com.data_handle.get_interface().get_error_code_value(ret)})'
        return result
    result = "login success"
    return result


# 获取当前版本号
def get_version():
    return com.data_handle.get_interface().get_version()


# 释放资源
def release():
    fini()


# 配置
def config(open_trace=True, open_file_log=True, open_cout_log=True):
    com.data_handle.get_interface().init(open_trace, open_file_log, open_cout_log)


# 登陆前 初始化 -- 修改ip映射,流量与日志开关设置,回调函数注册,接管系统日志,自我处理日志
def Initial():
    # 添加ip映射
    # get_interface().add_ip_map("168.63.17.150", "127.0.0.1")
    # 流量与日志开关设置
    # open_trace trace流量日志开关 # params:open_file_log 本地日志文件开关  # params:open_cout_log 控制台日志开关
    open_trace = True
    open_file_log = True
    open_cout_log = True
    com.data_handle.get_interface().init(open_trace, open_file_log, open_cout_log);

    # 注册回调和接管日志
    # 1.注册回调接口，不注册无法接收数据、处理数据，不会回调data_handle
    callback = com.data_handle.OnRecvMarketData()
    com.data_handle.get_interface().setCallBack(callback)

    # 2.接管日志
    # 若想关闭系统日志,自我处理日志,打开本方法
    # 打开本方法后,日志在insightlog.py的PyLog类的方法log(self,line)中也会体现,其中 line为日志内容）
    # use_init = True 系统日志以 get_interface().init 配置的方式记录
    # use_init = False 系统不再记录或打印任何日志,日志只有自行处理部分处理


# 释放资源
def fini():
    com.data_handle.get_interface().fini()

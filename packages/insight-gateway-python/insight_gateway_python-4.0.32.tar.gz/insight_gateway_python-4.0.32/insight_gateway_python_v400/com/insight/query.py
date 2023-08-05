import com.data_handle


def query_fin_info(query_type, params):
    return com.data_handle.get_interface().queryfininfosynchronous(query_type, params)


def query_basicInfo_by_type(dictmarketdatatype, isToday=True):
    security_id_list = []  # 置空表示不额外查询某些标的
    listmarketdatatype = []
    listmarketdatatype.append(dictmarketdatatype)
    if isToday:
        query_last_mdcontant(listmarketdatatype, security_id_list)
    else:
        query_mdcontant(listmarketdatatype, security_id_list)


def query_basicInfo_by_id(listsecurityid, isToday=True):
    listmarketdatatype = []  # 置空表示不额外查询某些标的
    if isToday:
        query_last_mdcontant(listmarketdatatype, listsecurityid)
    else:
        query_mdcontant(listmarketdatatype, listsecurityid)


# 查询历史上所有的指定证券的基础信息 -- 在data_handle.py 数据回调接口OnMarketData()中marketdata.marketDataType = MD_CONSTANT
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_mdcontant(security_idsource_and_types, security_id_list):
    com.data_handle.get_interface().queryMdContantCallback(security_idsource_and_types, security_id_list)


# 查询今日最新的指定证券的基础信息 -- 在data_handle.py 数据回调接口OnMarketData()中marketdata.marketDataType = MD_CONSTANT
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_last_mdcontant(security_idsource_and_types, security_id_list):
    # 按市场查询
    # 沪市 股票
    com.data_handle.get_interface().queryLastMdContantCallback(security_idsource_and_types, security_id_list)


# 查询指定证券的ETF的基础信息 -- 在data_handle.py 数据回调接口OnMarketData()中marketdata.marketDataType = MD_ETF_BASICINFO
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_ETFinfo(securityIDSource, securityType):  # 查询指定证券的ETF的基础信息
    # params:securityIDSource 为 ESecurityIDSource枚举值
    # params:securityType 为 ESecurityType枚举值
    security_idsource_and_types = []
    # 沪市 股票
    idsource_and_type = {"ESecurityIDSource": securityIDSource, "ESecurityType": securityType}
    security_idsource_and_types.append(idsource_and_type)

    # securityIDSourceAndTypes 与 securityIdList并集
    security_id_list = []  # 置空表示不额外查询某些标的
    # params:security_id_list 为 标的集合
    com.data_handle.get_interface().queryETFInfoCallback(security_idsource_and_types, security_id_list)


# 查询指定证券的最新一条Tick数据 -- 在data_handle.py 数据回调接口OnMarketData()中marketdata.marketDataType = MD_TICK
# params:securityIdSource 为市场ESecurityIDSource 枚举值;securityType 为 ESecurityType枚举值
def query_last_tick_by_type(securityIDSource, securityType):  # 通过证券类型和数据源查询最新Tick数据
    # params:security_idsource 为 ESecurityIDSource枚举值
    # params:security_type 为 ESecurityType枚举值
    # 沪市 股票

    security_idsource_and_types = []
    idsource_and_type = {"ESecurityIDSource": securityIDSource, "ESecurityType": securityType}
    security_idsource_and_types.append(idsource_and_type)

    # security_id_list 标的 列表
    security_id_list = []  # 置空表示不额外查询某些标的
    # security_idsource_and_types 与 security_id_list 并集
    com.data_handle.get_interface().queryLastMdTickCallback(security_idsource_and_types, security_id_list)

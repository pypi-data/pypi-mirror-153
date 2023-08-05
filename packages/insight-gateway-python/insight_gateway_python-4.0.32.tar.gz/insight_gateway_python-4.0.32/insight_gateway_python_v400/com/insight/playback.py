
from datetime import datetime
import com.data_handle

# 回放接口 (注意：securitylist 和 securityIdList取并集!!!)
# 回放限制
# 对于回放而言，时间限制由股票只数和天数的乘积决定，要求 回放只数 × 回放天数 × 证券权重 ≤ 450，交易时间段内回放功能 乘积<=200。
# Tick/Transaction/Order回放时间范围限制是30天，每支证券权重为1，即可以回放15只股票30天以内的数据或450支股票1天内数据。
# 日K数据回放时间范围限制是365天，每支证券权重为0.005。
# 分钟K线数据回放时间范围限制是90天，每支证券权重0.05。
# 数据最早可以回放到 2017年1月2日
def playback(listsecurity, marketdata_type, exrights_type, start_time, stop_time):
    # 回放数据类型 EMarketDataType 详情请参阅 数据手册EMarketDataType
    # 示例：MD_TICK
    com.data_handle.get_interface().playCallback(listsecurity, marketdata_type, exrights_type, start_time, stop_time)


# 盘中回放接口 --securitylist 和 securityIdList取并集
# Can only query data for one day
def play_back_oneday(listsecurity, marketdata_type, exrights_type, isMdtime):
    # 回放数据类型 EMarketDataType 详情请参阅 数据手册EMarketDataType
    # 示例：MD_TICK
    cur_time = datetime.now()

    date_str = cur_time.strftime('%Y%m%d')
    print(date_str)

    start_time = f"{date_str}000000"
    stop_time = f"{date_str}235959"

    # 特别注意！！！！
    # security_id_list 注意回放限制
    print(listsecurity)
    com.data_handle.get_interface().playCallback(listsecurity, marketdata_type, exrights_type, start_time, stop_time, isMdtime)

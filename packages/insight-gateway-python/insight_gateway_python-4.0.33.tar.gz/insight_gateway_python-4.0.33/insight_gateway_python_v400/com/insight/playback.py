
from datetime import datetime
import com.data_handle

# �طŽӿ� (ע�⣺securitylist �� securityIdListȡ����!!!)
# �ط�����
# ���ڻطŶ��ԣ�ʱ�������ɹ�Ʊֻ���������ĳ˻�������Ҫ�� �ط�ֻ�� �� �ط����� �� ֤ȯȨ�� �� 450������ʱ����ڻطŹ��� �˻�<=200��
# Tick/Transaction/Order�ط�ʱ�䷶Χ������30�죬ÿ֧֤ȯȨ��Ϊ1�������Իط�15ֻ��Ʊ30�����ڵ����ݻ�450֧��Ʊ1�������ݡ�
# ��K���ݻط�ʱ�䷶Χ������365�죬ÿ֧֤ȯȨ��Ϊ0.005��
# ����K�����ݻط�ʱ�䷶Χ������90�죬ÿ֧֤ȯȨ��0.05��
# ����������Իطŵ� 2017��1��2��
def playback(htscsecurityID_and_types, exrights_type, start_time, stop_time):
    # �ط��������� EMarketDataType ��������� �����ֲ�EMarketDataType
    # ʾ����MD_TICK
    com.data_handle.get_interface().playCallback(htscsecurityID_and_types, exrights_type, start_time, stop_time)


# ���лطŽӿ� --securitylist �� securityIdListȡ����
# Can only query data for one day
def play_back_oneday(htscsecurityID_and_types, exrights_type, isMdtime):
    # �ط��������� EMarketDataType ��������� �����ֲ�EMarketDataType
    # ʾ����MD_TICK
    cur_time = datetime.now()

    date_str = cur_time.strftime('%Y%m%d')
    print(date_str)

    start_time = f"{date_str}000000"
    stop_time = f"{date_str}235959"

    # �ر�ע�⣡������
    # security_id_list ע��ط�����
    print(htscsecurityID_and_types)
    com.data_handle.get_interface().playCallback(htscsecurityID_and_types, exrights_type, start_time, stop_time, isMdtime)

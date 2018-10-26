from jaqs_fxdayu.data import DataView  # 可以视为一个轻量级的数据库，数据格式基于pandas，方便数据的调用和处理
from jaqs_fxdayu.data import RemoteDataService  # 数据服务，用于下载数据
import os
import warnings

warnings.filterwarnings("ignore")
dataview_folder = '../Factor'

if not (os.path.isdir(dataview_folder)):
    os.makedirs(dataview_folder)


# 数据下载
def save_dataview():
    data_config = {
        "remote.data.address": "tcp://data.quantOS.org:8910",
        "remote.data.username": "18566262672",
        "remote.data.password": "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTI3MDI3NTAyMTIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTg1NjYyNjI2NzIifQ.O_-yR0zYagrLRvPbggnru1Rapk4kiyAzcwYt2a3vlpM"
    }
    ds = RemoteDataService()
    ds.init_from_config(data_config)

    dv = DataView()
    props = {'start_date': 20140101, 'end_date': 20180101, 'universe': '000300.SH',
             'fields': "volume,pb,pe,ps,roe,float_mv,sw1",
             'freq': 1,
             'timeout': 180}

    dv.init_from_config(props, ds)
    dv.prepare_data()
    dv.save_dataview(dataview_folder)  # 保存数据文件到指定路径，方便下次直接加载


save_dataview()

# 加载数据

dv = DataView()
dv.load_dataview(dataview_folder)

print(dv.get_ts("pe").head())

import numpy as np

#定义信号过滤条件-非指数成分
def mask_index_member():
    df_index_member = dv.get_ts('index_member')
    mask_index_member = df_index_member == 0
    return mask_index_member

# 定义可买卖条件——未停牌、未涨跌停
def limit_up_down():
    trade_status = dv.get_ts('trade_status')
    mask_sus = trade_status == 0
    # 涨停
    dv.add_formula('up_limit', '(close - Delay(close, 1)) / Delay(close, 1) > 0.095', is_quarterly=False, add_data=True)
    # 跌停
    dv.add_formula('down_limit', '(close - Delay(close, 1)) / Delay(close, 1) < -0.095', is_quarterly=False, add_data=True)
    can_enter = np.logical_and(dv.get_ts('up_limit') < 1, ~mask_sus) # 未涨停未停牌
    can_exit = np.logical_and(dv.get_ts('down_limit') < 1, ~mask_sus) # 未跌停未停牌
    return can_enter,can_exit

mask = mask_index_member()
can_enter,can_exit = limit_up_down()

from jaqs_fxdayu.research import SignalDigger
obj = SignalDigger(output_folder='./output',
                   output_format='pdf')
# 处理因子 计算目标股票池每只股票的持有期收益，和对应因子值的quantile分类

obj.process_signal_before_analysis(signal=dv.get_ts("pe"),
                                   price=dv.get_ts("close_adj"),
                                   high=dv.get_ts("high_adj"), # 可为空
                                   low=dv.get_ts("low_adj"),# 可为空
                                   group=dv.get_ts("sw1"),# 可为空
                                   n_quantiles=5,# quantile分类数
                                   mask=mask,# 过滤条件
                                   can_enter=can_enter,# 是否能进场
                                   can_exit=can_exit,# 是否能出场
                                   period=5,# 持有期
                                   benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                   commission = 0.0008,
                                   )
signal_data = obj.signal_data


import matplotlib.pyplot as plt
print(obj.create_full_report())
plt.show()

from jaqs_fxdayu.research.signaldigger.analysis import analysis
result = analysis(signal_data, is_event=False, period=5)

print("——ic分析——")
print(result["ic"])
print("——选股收益分析——")
print(result["ret"])
print("——最大潜在盈利/亏损分析——")
print(result["space"])
import matplotlib.pyplot as plt
obj.create_full_report()
plt.show()


obj.process_signal_before_analysis(signal=dv.get_ts("pe"),
                                   price=dv.get_ts("close_adj"),
                                   high=dv.get_ts("high_adj"), # 可为空
                                   low=dv.get_ts("low_adj"),# 可为空
                                   group=dv.get_ts("sw1"),# 可为空
                                   n_quantiles=5,# quantile分类数
                                   mask=mask,# 过滤条件
                                   can_enter=can_enter,# 是否能进场
                                   can_exit=can_exit,# 是否能出场
                                   period=30,# 持有期
                                   benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                   commission = 0.0008,
                                   )
signal_data = obj.signal_data


import matplotlib.pyplot as plt
print(obj.create_full_report())
plt.show()

from jaqs_fxdayu.research.signaldigger.analysis import analysis
result = analysis(signal_data, is_event=False, period=30)

print("——ic分析——")
print(result["ic"])
print("——选股收益分析——")
print(result["ret"])
print("——最大潜在盈利/亏损分析——")
print(result["space"])
import matplotlib.pyplot as plt
obj.create_full_report()
plt.show()

obj.process_signal_before_analysis(signal=dv.get_ts("pe"),
                                   price=dv.get_ts("close_adj"),
                                   high=dv.get_ts("high_adj"), # 可为空
                                   low=dv.get_ts("low_adj"),# 可为空
                                   group=dv.get_ts("sw1"),# 可为空
                                   n_quantiles=5,# quantile分类数
                                   mask=mask,# 过滤条件
                                   can_enter=can_enter,# 是否能进场
                                   can_exit=can_exit,# 是否能出场
                                   period=60,# 持有期
                                   benchmark_price=dv.data_benchmark, # 基准价格 可不传入，持有期收益（return）计算为绝对收益
                                   commission = 0.0008,
                                   )
signal_data = obj.signal_data


import matplotlib.pyplot as plt
print(obj.create_full_report())
plt.show()

from jaqs_fxdayu.research.signaldigger.analysis import analysis
result = analysis(signal_data, is_event=False, period=60)

print("——ic分析——")
print(result["ic"])
print("——选股收益分析——")
print(result["ret"])
print("——最大潜在盈利/亏损分析——")
print(result["space"])
import matplotlib.pyplot as plt
obj.create_full_report()
plt.show()

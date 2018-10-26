import pandas as pd
from datetime import datetime
import alphalens

#5.1
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


factor = dv.get_ts("ps")
factor.index = pd.Index(map(lambda x: datetime.strptime(str(x),"%Y%m%d") , factor.index)) #索引调整为datetime日期格式
factor = factor.stack()#处理成MultiIndex格式（alphalens分析因子必须的格式）

print(factor.head())

def change_index(df):
    df.index = pd.Index(map(lambda x: datetime.strptime(str(x),"%Y%m%d") , df.index)) #索引调整为datetime日期格式
    return df

prices = dv.get_ts("close_adj") #获取价格
prices = change_index(prices)
print(prices.head())


#计算目标股票池每只股票的持有期收益，和对应因子值的quantile分类
factor_data = alphalens.utils.get_clean_factor_and_forward_returns(factor, prices, quantiles=5, periods=(1,5,10))
print(factor_data.head())


import matplotlib.pyplot as plt
mean_return_by_q, std_err_by_q = alphalens.performance.mean_return_by_quantile(factor_data, by_date=True, demeaned=True)

alphalens.plotting.plot_cumulative_returns_by_quantile(mean_return_by_q, 1)
alphalens.plotting.plot_cumulative_returns_by_quantile(mean_return_by_q, 5)
alphalens.plotting.plot_cumulative_returns_by_quantile(mean_return_by_q, 10)
plt.show()

ic = alphalens.performance.factor_information_coefficient(factor_data)
print(ic.head())

alphalens.plotting.plot_ic_hist(ic) #因子IC分布
plt.show()

# 月均IC热度图
mean_monthly_ic = alphalens.performance.mean_information_coefficient(factor_data, by_time='M')
alphalens.plotting.plot_monthly_ic_heatmap(mean_monthly_ic)#因子月均IC表现
plt.show()

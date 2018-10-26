from jaqs_fxdayu.data import DataView
import warnings

warnings.filterwarnings("ignore")
dataview_folder = '../Factor'
dv = DataView()
dv.load_dataview(dataview_folder)

from jaqs_fxdayu.research.signaldigger import process

Open = dv.get_ts("open_adj")
High = dv.get_ts("high_adj")
Low = dv.get_ts("low_adj")
Close = dv.get_ts("close_adj")
trade_status = dv.get_ts('trade_status')
mask_sus = trade_status == 0
# 剔除掉停牌期的数据　再计算指标
open_masked = process._mask_df(Open,mask=mask_sus)
high_masked = process._mask_df(High,mask=mask_sus)
low_masked = process._mask_df(Low,mask=mask_sus)
close_masked = process._mask_df(Close,mask=mask_sus)

from jaqs_fxdayu.data import signal_function_mod as sfm
cci = sfm.ta(ta_method='CCI',
             ta_column=0,
             Open=open_masked,
             High=high_masked,
             Low=low_masked,
             Close=close_masked,
             Volume=None
             )
dv.append_df(cci,'CCI')
dv.get_ts('CCI').tail()



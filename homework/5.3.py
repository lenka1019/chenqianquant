from jaqs_fxdayu.data import DataView
import warnings

warnings.filterwarnings("ignore")
dataview_folder = '../Factor'
dv = DataView()
dv.load_dataview(dataview_folder)


dv.add_formula("Divert", "Corr(volume,close_adj,20)", is_quarterly=False).head()

# 添加到数据集dv里，则计算结果之后可以反复调用
dv.add_formula("Divert", "Corr(volume,close_adj,20)", is_quarterly=False, add_data=True)
dv.get_ts("Divert").head()


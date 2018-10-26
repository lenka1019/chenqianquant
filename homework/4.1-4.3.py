import numpy as np
import talib as ta
import pandas as pd
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

#4.1
stock1 = pd.read_excel('sz50.xlsx',sheetname='600104.XSHG',index_col='datetime')
stock2 = pd.read_excel('sz50.xlsx',sheetname='600518.XSHG',index_col='datetime')

five_day_df = pd.concat([stock1.close.pct_change(5),stock2.close.pct_change(5)],keys=['stock1','stock2'],axis=1)
print(five_day_df.tail(5))
print(five_day_df.cov())

#4.2
n=6
p=1/6
s = np.random.binomial(n,p,60) #生成随机数
fig = plt.figure(figsize=(15,5))
plt.hist(s,bins = [0,1,2,3,4,5,6],align='left')
plt.xlabel('Value')
plt.ylabel('Occurences')
plt.legend(['BionomialRandomVariable'])
plt.show() #平均每轮筛子为6的次数

#4.3
stock3 = pd.read_excel('sz50.xlsx',sheetname='600030.XSHG',index_col='datetime')
cci = ta.CCI(stock3.high.values, stock3.low.values, stock3.close.values, timeperiod= 10)
fig = plt.figure(figsize=(15,7))
plt.plot(cci)
plt.show()


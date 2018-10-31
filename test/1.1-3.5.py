#1.1 boolean表示布尔型数据类型，判断真假，float为浮点型数据类型，int为整数型数据类型
#1.2
import numpy as np
import talib as ta
import pandas as pd
import warnings


warnings.filterwarnings('ignore')

list_1= list(range(1,100,2)) #1-99奇数
list_2= list(range(2,100,2)) #1-99偶数
sum_1 = sum(list_1)
sum_2 = sum(list_2)
print(sum_1-sum_2)

#1.3
s='yoyo'
print(list(s))

#2.1 先取1-99整数，再以3为步长，取第三个整数一直到最后一个数，然后取倒数十个数，最后将最终取得所有数打印下来
#for i in range(1,100)[2::3][-10:]:
#    print(i)

#2.2

class thigh:
    def __init__(self,time):
        self.time=time
class tlow:
    def __init__(self,time):
        self.time=time
class timegap:
    def __init__(self,time1,time2):
        self.time1=thigh(time1)
        self.time2=tlow(time2)
    def calc(self,time1,time2):
        return self.time1.time-self.time2.time

one = timegap(15,7)
two = timegap(66,20)
print({'one dif':one.calc(15,7)})
print({'two dif':two.calc(66,20)})


#3.1
dt = pd.read_excel('sz50.xlsx',sheetname=0,index_col='datetime')
print(dt.columns) #查看列名
dt_1 = np.transpose(dt) #对数据转置

#3.2
data = pd.read_excel('sz50.xlsx',sheetname='600029.XSHG',index_col='datetime')
closevalue = np.array(data.close.values) #收盘价转换成Numpy的Array格式
ema = ta.EMA(closevalue,10)[-5:] #计算EMA并返回最后5个值
print(ema)


#3.3
import pandas as pd
symbol=['600029.XSHG','600050.XSHG','601318.XSHG']
data_dict = {}
for s in symbol:
    data =  pd.read_excel('sz50.xlsx',sheetname=s, index_col='datetime')
    data_dict[s] = data.loc['2017-01-03':'2017-11-20']
PN = pd.Panel(data_dict)
print(PN)
print(PN.shape)

#3.4
PN2 = PN.transpose(2,0,1) #交换item、major、minor的位置
#print(PN2.to_frame)
arr1 = np.array(PN2)   #转成array格式
print(arr1[0,0:,-20:])   #切片


#3.5
arr = np.arange(25).reshape(5,5)
print(arr)

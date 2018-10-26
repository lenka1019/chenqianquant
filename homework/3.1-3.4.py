import numpy as np
import pandas as pd
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

#3.1
data = pd.read_excel('sz50.xlsx',sheetname=0,index_col='datetime')
print(data)
Series = data.open
print(Series.tail(5))

#3.2
arr84 = np.arange(32).reshape(8,4)
print(arr84)

#3.3
arr = np.arange(10)
arr[5:8]=(12,12,12)
print(arr)

#3.4
time1= datetime(2017,1,2,4,5)
time2= datetime(2017,3,4,6,7)
cha= time2-time1
print(cha)
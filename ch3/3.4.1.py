from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

sec = pdr.get_data_yahoo('005930.KS', start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')
print(sec.head(10))

tmp_msft = msft.drop(columns='Volume')
print(tmp_msft.tail())

print(sec.index)
print(sec.columns)

import  matplotlib.pyplot as plt

plt.plot(sec.index, sec.Close/1000, 'b', label='삼성')
plt.plot(msft.index, msft.Close, 'r--', label='마소')
plt.legend(loc='best')
plt.show()

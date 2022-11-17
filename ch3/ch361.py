import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from scipy import stats
import matplotlib.pyplot as plt

dow = pdr.get_data_yahoo('^DJI', '2000-01-04')
kospi = pdr.get_data_yahoo('^KS11', '2000-01-04')

# 3.6.2
d = (dow.Close / dow.Close.loc['2000-01-04']) * 100
k = (kospi.Close / kospi.Close.loc['2000-01-04']) * 100

# 3.6.3
# print(len(dow)); print(len(kospi))
df = pd.DataFrame({'X': dow['Close'], 'Y': kospi['Close']})
df = df.fillna(method='bfill').fillna(method='ffill')
# print(df)


# r_value = df['DOW'].corr(df['KOSPI'])
# print('상관계수 > {}'.format(r_value))
# print("결정계수 > {}".format(r_value ** 2))

regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:.2f} * X + {regr.intercept:.2f}'


plt.figure(figsize=(7, 7))
# plt.scatter(df['DOW'], df['KOSPI'], marker='.')
# # plt.plot(d.index, d, 'r--', label='Dow')
# # plt.plot(k.index, k, 'b', label='KOSPI')
# # plt.grid(True)
# # plt.legend(loc='best')
# plt.xlabel('Dow')
# plt.ylabel('KOSPI')
# plt.show()
plt.plot(df.X, df.Y, '.')
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
plt.legend(['DOW x KOSPI', regr_line])
plt.title(f'DOW x KOSPI (R = {regr.rvalue:.2f}')
plt.xlabel('DOW')
plt.ylabel('KOSPI')
plt.show()


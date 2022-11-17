import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import mplfinance as mpf

# 맨뒤 숫자
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]

# 전체 페이지 읽기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'
for page in range(1, int(last_page) + 1):
    page_url = '{}&page={}'.format(sise_url, page)
    df = df.append(pd.read_html(page_url, header=0)[0])

# 차트 출력 데이터프레임 가공
df = df.dropna()
df = df.iloc[0:30]
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# 캔들차트 그리기
kwargs = dict(title='Chart', type='candle', mav=(2,4,6), volume=True, ylabel='ohlc')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)
# mpf.plot(df, title='Candle chart', type='candle')


# 날짜, 종가 칼럼 차트 그리기
# plt.title('셀트리온 종가')
# plt.xticks(rotation=45)
# plt.plot(df['날짜'], df['종가'], 'co-')
# plt.grid(color='gray', linestyle='--')
# plt.show()
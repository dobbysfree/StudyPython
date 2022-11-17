from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    print(pgrr.a['href'])
    print(pgrr.prettify())
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]
    print(last_page)

df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    df = df.append(pd.read_html(page_url, header=0)[0])

df = df.dropna()
print(df)
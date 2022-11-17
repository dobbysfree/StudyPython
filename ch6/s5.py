import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
from ch5 import Analyzer

class DualMomentum:
    def __init__(self):
        """생성자: KRX 종목코드를 구하기 위한 MarketDB 객체 생성"""
        self.mk = Analyzer.MarketDB()

    def get_rltv(self, start_date, end_date, stock_count):
        connection = pymysql.connect(host='192.168.1.96', port=8706, db='db_study', user='devasaq', passwd='ZXCdsaqwe321!', autocommit=True)
        cursor = connection.cursor()

        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print('end_date : {} -> returned None'.format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(self.mk.codes):
            sql = f"select close from daily_price where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            old_price = int(result[0])
            sql = f"select close from daily_price where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        df = df.head(stock_count)
        df.index = pd.Index(range(stock_count))

        connection.close()
        print(df)
        print(f"\nRelative momentum ({start_date} ~ {end_date}) : {df['returns'].mean():.2f}% \n")
        return df

    """절대 모멘텀은 자산의 가치가 상승하고 있을 때만 투자하고 아닐때는 단기 국채를 매수하거나 현금을 보유하는 전략"""
    def get_abs(self, rltv_momentum, start_date, end_date):
        stocklist= list(rltv_momentum['code'])
        connection = pymysql.connect(host='192.168.1.96', port=8706, db='db_study', user='devasaq', passwd='ZXCdsaqwe321!', autocommit=True)
        cursor = connection.cursor()

        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print('end_date : {} -> returned None'.format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(self.mk.codes):
            sql = f"select close from daily_price where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            old_price = int(result[0])
            sql = f"select close from daily_price where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        connection.close()
        print(df)
        print(f"\nAbasolute momentum ({start_date} ~ {end_date}) : {df['returns'].mean():.2f}% \n")
        return
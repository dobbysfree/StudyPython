from ch5 import Analyzer
mk = Analyzer.MarketDB()
aa = mk.get_daily_price('005930', '2020-07-21', '2020.08.03')
print(aa)
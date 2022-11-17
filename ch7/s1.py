from datetime import datetime
import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)  #RSI 지표로 사용할 변수 지정
    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

cerebro = bt.Cerebro() # Cerebro 클래스는 백트레이더의 핵심 클래스로서, 데이터를 취합하고 백테스트 또는 라이브 트레이딩 실행 뒤 결과 출력
cerebro.addstrategy(MyStrategy)
data = bt.feeds.YahooFinanceData(dataname='036570.KS', fromdate=datetime(2010, 1, 1), todate=datetime(2020, 8, 7))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value: {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value: {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot()

import backtrader as bt
from datetime import datetime

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY : 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'SELL : 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELD')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')


cerebro = bt.Cerebro() # Cerebro 클래스는 백트레이더의 핵심 클래스로서, 데이터를 취합하고 백테스트 또는 라이브 트레이딩 실행 뒤 결과 출력
cerebro.addstrategy(MyStrategy)
data = bt.feeds.YahooFinanceData(dataname='036570.KS', fromdate=datetime(2017, 1, 1), todate=datetime(2020, 8, 7))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0014)
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
# cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value: {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value: {cerebro.broker.getvalue():,.0f} KRW')
# cerebro.plot()
cerebro.plot(style='candlestick')
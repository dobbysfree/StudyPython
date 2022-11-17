import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt
from ch5 import Analyzer

mk = Analyzer.MarketDB()
raw_df = mk.get_daily_price('삼성전자', '2018-05-04', '2020-08-10')

def MinMaxScaler(data):
    """최소값과 최대값을 이용하여 0~1값으로 변환"""
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    return numerator / (denominator + 1e-7)

#데이터 전처리
dfx = raw_df[['open', 'high', 'low', 'volume', 'close']]
dfx = MinMaxScaler(dfx) #계산 속도 향상을 위해 데이터의 스케일을 0~1로 변경
dfy = dfx[['close']]
x = dfx.values.tolist()
y = dfy.values.tolist()

data_x = []
data_y = []
window_size = 10 #10일 간의 OHLVC 데이터
for i in range(len(y) - window_size):
    _x = x[i: i + window_size]
    _y = y[i + window_size]
    data_x.append(_x)
    data_y.append(_y)
print(_x, "\n->", _y)

# 훈련용 데이터셋(70%)
train_size = int(len(data_y) * 0.7)
train_x = np.array(data_x[0:train_size])
train_y = np.array(data_y[0:train_size])

# 테스트용 데이터셋(30%)
test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size:len(data_x)])
test_y = np.array(data_y[train_size:len(data_y)])

# 모델 생성
model = Sequential() # 시퀀셜 모델 객체를 생성
model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, 5)))
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_x, train_y, epochs=60, batch_size=30) # 학습
pred_y = model.predict(test_x) # 예측

plt.figure()
plt.plot(test_y, color='red', label='real SEC stock price')
plt.plot(pred_y, color='blue', label='predicted SEC stock price')
plt.title('SEC stock price prediction')
plt.xlabel('time')
plt.ylabel('stock price')
plt.legend()
plt.show()

print("SEC tomorrow's price : ", raw_df.close[-1]*pred_y[-1]/dfy.close[-1])
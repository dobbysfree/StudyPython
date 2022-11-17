import matplotlib.pyplot as plt
import tensorflow as tf

x_data = [1, 2, 3, 4, 5]
y_data = [2, 3, 4, 5, 6] # y = 1 * x + 1

w = tf.Variable(0.7) # 가중치 w를 임의의 값 0.7 초기화
b = tf.Variable(0.7) # 편향 b를 임의의 값 0.7 초기화
learn_rate = 0.01 # 학습률은 보통 0.01 ~ 0.001 사이의 값으로 설정

print(f'step|    w|    b| cost')
print(f'____|_____|_____|     ')

for i in range(1, 1101):
    with tf.GradientTape() as tape: # 내부의 계산과정을 tape에 기록, 나중에 tape.gradient()함수를 이용 미분값 계산
        hypothesis = w * x_data + b # 가설은 w * x + b
        cost = tf.reduce_mean((hypothesis - y_data) ** 2)  # 손실 비용을 오차제곱평균으로 구함
    dw, db = tape.gradient(cost, [w, b]) # w와 b에 대해 손실을 미분해서 dw, db값을 구한다.

    w.assign_sub(learn_rate * dw) # 텐서플로의 assign_sub는 파이썬의 a = a - b의 연산과 동일 w값에서 '학습률 * dw)를 뺀값을 새로운 w값으로 설정
    b.assign_sub(learn_rate * db)

    if i in [1, 3, 5, 10, 1000, 1100]:
        print(f'{i:4d}| {w.numpy():.2f}| {b.numpy():.2f}| {cost:.2f}')
        plt.figure(figsize=(7, 7))
        plt.title(f'[Step {i:d}] h(x) = { w.numpy():.2f}x + {b.numpy():.2f}')
        plt.plot(x_data, y_data, 'o')
        plt.plot(x_data, w * x_data + b, 'r', label='hypothesis')
        plt.xlabel('x_data')
        plt.ylabel('y_data')
        plt.xlim(0, 6)
        plt.ylim(1, 7)
        plt.legend(loc='best')
        plt.show()
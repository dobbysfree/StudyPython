import numpy as np

X = np.array([10, 20]) #(x1, x2)값을 임의의 값인 10, 20
W1 = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]]) # 2행3열 임의 가중치
B1 = np.array([1, 2, 3])

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

A1 = np.dot(X, W1) + B1 # 1층 입력 신호를 계산
print(A1)

Z1 = sigmoid(A1)
print(Z1)

W2 = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
B2 = np.array([0.1, 0.2])

A2 = np.dot(Z1, W2) + B2
Y = sigmoid(A2)

print(Y)
#gradient descent code
import numpy as np
import random
from math import inf
from sklearn.datasets import load_boston
from icecream import ic
data=load_boston()#波士顿房价预测


def d_k(Y,y_hat_list,X):
    n = len(Y)
    gradient = 0
    for x_i, y_i, y_hat_i in zip(list(X), list(Y), list(y_hat_list)):
        gradient += (y_i - y_hat_i) * x_i*1/abs(y_i-y_hat_i)
    return -1 / n * gradient

def d_b(Y,y_hat_list):
    n = len(Y)
    gradient = 0
    for y_i, y_hat_i in zip(list(Y), list(y_hat_list)):
        gradient += (y_i - y_hat_i) * 1 / abs(y_i - y_hat_i)
    return -1 / n * gradient


def get_price(x,k,b):
    return k*x+b


def final_loss(Y,y_hat_list):
    return (1/len(Y))*sum([y_i-y_hat for y_i,y_hat in zip(Y,y_hat_list)])

def get_res():
    trying = 100000
    learning_rate = 1e-04
    X, Y = data['data'][:, 5], data['target']
    m_loss = float(inf)
    best_k = random.random() * 200 - 100
    best_b= random.random() * 200 - 100
    for i in range(trying):
        y_hat_list = [get_price(x, best_k, best_b) for x in X]
        now_loss=final_loss(Y,y_hat_list)
        if now_loss<m_loss:
            m_loss=now_loss
            if i%50==0:
                print('when time is:{},get best_k{} best_b:{},and the loss is:{}'.format(i, best_k, best_b,
                                                                                         m_loss))
        k_direction=d_k(Y,y_hat_list,X)
        b_direction=d_b(Y,y_hat_list)
        best_k+=-k_direction*learning_rate
        best_b+=-b_direction*learning_rate

if __name__=="__main__":
    get_res()
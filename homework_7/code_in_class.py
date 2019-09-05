from collections import Counter
from scipy.spatial.distance import cosine
import numpy as np
import random
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
random_data=np.random.random((20,2))
# print(random_data)
# print(random_data[0])
X=random_data[:,0]
y=random_data[:,1]
# print(X.shape)
# print(X)
def assmuing_function(x):
    return 13.4*x+5+random.randint(-5,5)
y=[assmuing_function(x) for x in X]
plt.scatter(X,y)
# plt.show()

y=np.array(y)
# print(y)
# print(X.reshape(-1,1))
reg=LinearRegression().fit(X.reshape(-1,1),y)
reg.score(X.reshape(-1,1),y)
# print(reg.score(X.reshape(-1,1),y))
# print(reg.coef_)
# print(reg.intercept_)
def f(x):
    return reg.coef_*x+reg.intercept_

plt.scatter(X,y)
plt.plot(X,f(X),color='red')
# plt.show()

def model(X,y):
    return [(Xi,yi) for Xi,yi in zip(X,y)]

def distance(x1,x2):
    return cosine(x1,x2)

def predict(x,k=5):
    most_similars=sorted(model(X,y),key=lambda xi:distance(xi[0],x))[:k]
    print(Counter([x[-1] for x in most_similars]).most_common(1))
# predict(X)


fname='sqlResult_1558435.csv'
content=pd.read_csv(fname,encoding='gb18030')
content.head()
print(len(content))
# xinhua_news=content[content['source']=='新华社']
xinhua_news = content[content['source'] == '新华社']
print(len(xinhua_news)/len(content))

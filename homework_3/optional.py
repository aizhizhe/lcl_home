import math,random
import matplotlib.pyplot as plt
def cal_distance(x1,x2):
    return math.sqrt(math.pow(int(x1[0])-int(x2[0]),2)+math.pow(int(x1[1])-int(x2[1]),2))


def k_salsman(k):
    global P
    global K
    global S
    global res
    global scatters
    scatters={}
    P=(random.randint(-100, 100),random.randint(-100, 100))
    scatters['0']=P
    latitudes = [random.randint(-100, 100) for _ in range(k)]
    longitude = [random.randint(-100, 100) for _ in range(k)]
    S = [P]
    res={}
    for i in range(len(latitudes)):
        res[str(i+1)]=(latitudes[i],longitude[i])
    K=[str(i) for i in range(1,len(res.keys())+1)]
    return latitudes,longitude

def distance(scatter,K):
    #求点scatter到list K中的哪一个点的距离最短，以及最短距离是多少
    total_dis={}
    for index in K:
        distan = cal_distance(res[index],scatter)
        total_dis[index]=distan
    t=sorted(total_dis.items(),key=lambda m:m[-1])[0]
    return t[-1],t[0]

def r(k):
    if k==1:
        return less(S[k-1],1)
    else:
        return r(k-1)+less(S[k-1],1)

def less(i,j):
    (distan,scat)=distance(i,K)
    scatters[scat]=res[scat]
    S.append(res[scat])
    K.remove(scat)
    return distan

if __name__=="__main__":
    latitudes, longitude=k_salsman(20)
    r(20)
    print(scatters)
    plt.scatter(latitudes, longitude)
    plt.scatter(scatters['0'][0], scatters['0'][1], color='r')
    x=[]
    y=[]
    for data in scatters:
        x.append(scatters[data][0])
        y.append(scatters[data][1])
    plt.plot(x,y)
    plt.show()

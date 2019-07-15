import re
import urllib.request,math
from collections import Counter
def get_text(url):
    headers = {'User_Agent': ''}
    response = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(response)
    result = html.read().decode('utf-8')
    return result
def get_res(pattern,text):
    des_data=re.findall(pattern,text)
    return des_data
def subway_url(url,pattern):
    result=get_text(url)
    des_data=get_res(pattern,result)
    return des_data
def subway_url1(url,pattern1,pattern2):
    result=get_text(url)
    des_text=get_res(pattern1,result)[0]
    des_data=get_res(pattern2,des_text)
    return des_data
def get_all_url():
    url = "https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"
    pattern = '<a target=_blank href="([\s\S]*?)">([\s\S]*?)</a>'
    des_data=subway_url(url,pattern)
    head="https://baike.baidu.com"
    s={}
    for w,k in des_data:
        if "线" in k and k not in s:
            s[k]=[head+w]
    return s
def get_station(sub_url,pattern1,pattern2):
    des=subway_url1(sub_url,pattern1,pattern2)
    return des

def get_all_substation():
    pattern1 = '<table log-set-param="table_view"[\s\S]*? data-sort="sortDisabled">(?:<caption>[\s\S]*?列表</caption>)?([\s\S]*?)</table>'#
    pattern2='<a target=_blank href="[\s\S]*?">([\s\S]*?)</a>' #<a target="_blank" href=[\s\S]*?>([\s\S]*?)</a>
    all_url=get_all_url()
    subwaydict={}
    for subway,url in all_url.items():
        des=get_station(url[0],pattern1,pattern2)
        subwaydict[subway]=des
    for sub in subwaydict:
        sta=[]
        for station in subwaydict[sub]:
            if "站" in station:
                sta.append(station.replace("<i>",""))
        subwaydict[sub]=sta
    return subwaydict
def get_sta_relation(subwaydict):
    station = {}
    for sub in subwaydict:
        for i, sta in enumerate(subwaydict[sub]):
            if sta+'-'+sub not in station:
                station[sta+'-'+sub] = []
            if i - 1 >= 0:
                station[sta+'-'+sub].append(subwaydict[sub][i - 1]+'-'+sub)
            if i + 1 <= len(subwaydict[sub]) - 1:
                station[sta+'-'+sub].append(subwaydict[sub][i + 1]+'-'+sub)
    sta_info=Counter([sta.split('-')[0] for sta in station])
    sta_trans=[sta for sta in sta_info if sta_info[sta]>1]
    new_sta={}
    for sta in station:
        # if sta.split('-')[0] in sta_trans:
            # if sta not in new_sta:
            #     new_sta[sta.split('-')[0]+'-'+'换乘']=[]
            # new_sta[sta.split('-')[0] + '-' + '换乘'].extend(station[sta])
        if sta.split('-')[0] not in [x.split('-')[0] for x in new_sta]:
            new_sta[sta]=station[sta]
        else:
            for stas in new_sta:
                if stas.split('-')[0]==sta.split('-')[0]:
                    new_sta[stas]+=station[sta]
                    break
            new_sta[sta]=new_sta[stas]
    return new_sta

def shortest_path_first(pathes):
    if len(pathes) <= 1: return pathes
    return sorted(pathes,key=len)

def search1(start, destination, connection_grpah, sort_candidate):
    pathes = [[start]]

    visitied = list()

    while pathes:  # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visitied: continue
        if '-' not in froninter:
            for station_a in connection_grpah:
                if station_a.split('-')[0]==froninter:
                    froninter=station_a
                    break
        # successors = connection_grpah[froninter]
        successors = connection_grpah[froninter]

        for city in successors:
            if city in path: continue  # eliminate loop
            if city.split('-')[0] in [x.split('-')[0] for x in path]: continue

            new_path = path + [city]

            pathes.append(new_path)

            if city.split('-')[0]  == destination: return new_path

        visitied.append(froninter)

        pathes = sort_candidate(pathes)  # 我们可以加一个排序函数 对我们的搜索策略进行控制
def search(start, destination, connection_grpah, sort_candidate):
    sss=[]
    # tion=[x.split('-')[0] for x in connection_grpah]
    # if "站" not in start:
    #     start+="站"
    # if "站" not in destination:
    #     destination+="站"
    # if start not in tion:
    #     return start+"站点不存在"
    # if destination not in tion:
    #     return destination+"站点不存在"
    pathes = [[start]]
    visitied = list()
    while pathes:  # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]
        if froninter in visitied: continue
        # froninter1=froninter
        if '-' not in froninter:
            for station_a in connection_grpah:
                if station_a.split('-')[0]==froninter:
                    froninter=station_a
                    break
        if froninter == "新街口站-北京地铁4号线" and path==['中关村站', '海淀黄庄站-北京地铁4号线', '人民大学站-北京地铁4号线', '魏公村站-北京地铁4号线', '国家图书馆站-北京地铁4号线', '动物园站-北京地铁4号线', '西直门站-北京地铁4号线']:
            print(connection_grpah[froninter])
        successors = connection_grpah[froninter]
        # new_s=[]#[" " for i in range(len(successors))]
        # for i,city in enumerate(successors):
            # if city.split('-')[1]!=froninter.split('-')[1]:
            #     for j in range(len(successors)-1,-1,-1):
            #         if new_s[j]==" ":
            #             new_s[j]=city
            #             break
            # if:
            # for jk in range(len(successors)):
                # if new_s[jk]==" ":
                # c=0
                # if city.split('-')[1] == froninter.split('-')[1]:
                #     new_s.append(city)
                #     c+=1
                    # break
        for city in successors:
            if city in path: continue  # eliminate loop
            if city.split('-')[0] in [x.split('-')[0] for x in path]:continue
            new_path = path+[city]
            pathes.append(new_path)
            if city.split('-')[0] == destination: return new_path
        visitied.append(froninter)
        pathes = sort_candidate(pathes)
    # pathes = sort_candidate(pathes)  # 我们可以加一个排序函数 对我们的搜索策略进行控制
    # return sss
if __name__=="__main__":
    subwaydict=get_all_substation()
    simple_connection_info=get_sta_relation(subwaydict)
    # print(simple_connection_info['国家图书馆站-北京地铁4号线'])
    des=search('中关村站', '平安里站', simple_connection_info, sort_candidate=shortest_path_first)
    print(des)
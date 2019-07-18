import re
import urllib.request,math
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
                sta.append(station)
        subwaydict[sub]=sta
    return subwaydict
def get_sta_relation(subwaydict):
    station = {}
    for sub in subwaydict:
        for i, sta in enumerate(subwaydict[sub]):
            if sta not in station:
                station[sta] = []
            if i - 1 >= 0:
                station[sta].append(subwaydict[sub][i - 1])
            if i + 1 <= len(subwaydict[sub]) - 1:
                station[sta].append(subwaydict[sub][i + 1])
    return station

def shortest_path_first(pathes):
    if len(pathes) <= 1: return pathes
    return sorted(pathes,key=len)
def search(start, destination, connection_grpah, sort_candidate):
    if "站" not in start:
        start+="站"
    if "站" not in destination:
        destination+="站"
    if start not in connection_grpah:
        return start+"站点不存在"
    if destination not in connection_grpah:
        return destination+"站点不存在"
    pathes = [[start]]
    visitied = list()
    while pathes:  # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]
        if froninter in visitied: continue
        successors = connection_grpah[froninter]
        for city in successors:
            if city in path: continue  # eliminate loop
            new_path = path+[city]
            pathes.append(new_path)
            if city == destination: return new_path
        visitied.append(froninter)
    pathes = sort_candidate(pathes)  # 我们可以加一个排序函数 对我们的搜索策略进行控制
    return pathes
if __name__=="__main__":
    subwaydict=get_all_substation()
    simple_connection_info=get_sta_relation(subwaydict)
    des=search('中关村站', '草房站', simple_connection_info, sort_candidate=shortest_path_first)
    print(des)
# coding=gbk
import re
import urllib.request,math
from collections import Counter

def get_text(url):
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
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
def subway_url1(url,pattern1,   pattern2):
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
        if sta.split('-')[0] not in [x.split('-')[0] for x in new_sta]:
            new_sta[sta]=station[sta]
        else:
            for stas in new_sta:
                if stas.split('-')[0]==sta.split('-')[0]:
                    new_sta[stas]+=station[sta]
                    break
            new_sta[sta]=new_sta[stas]
    return new_sta

def station_priority(path):
    subway=[]
    for station in path:
        subway.append(station.split("-")[1])
    subway=list(set(subway))
    return len(subway)

def shortest_path_first(pathes):
    ways={}
    res=[]
    if len(pathes) <= 1: return pathes
    for path in pathes:
        num=station_priority(path)
        if num not in ways:
            ways[num]=[]
        ways[num].append(path)
    sorway=sorted(ways.items(),key=lambda m:m[0])
    for data in sorway:
        if isinstance(data[1][0],list):
            for da in data[1]:
                res.append(da)
        else:
            res.extend(data[1])
    return res
def shortest_path_first1(pathes):
    if len(pathes) <= 1: return pathes
    return  sorted(pathes,key=len)

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
                    path[0]=station_a
                    break
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
    tion=[x.split('-')[0] for x in connection_grpah]
    if "站" not in start:
        start+="站"
    if "站" not in destination:
        destination+="站"
    if start not in tion:
        return start+"站点不存在"
    if destination not in tion:
        return destination+"站点不存在"
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
        successors = connection_grpah[froninter]
        for city in successors:
            if city in path: continue  # eliminate loop
            if city.split('-')[0] in [x.split('-')[0] for x in path]:continue
            new_path = path+[city]
            pathes.append(new_path)
            if city.split('-')[0] == destination: return new_path
        visitied.append(froninter)
        pathes = sort_candidate(pathes)

if __name__=="__main__":
    subwaydict=get_all_substation()
    #subwaydict={'北京地铁1号线': ['黑石头站', '高井站', '福寿岭站', '苹果园站', '古城站', '衙门口站', '八角游乐园站', '八宝山站', '玉泉路站', '五棵松站', '万寿路站', '公主坟站', '军事博物馆站', '木樨地站', '南礼士路站', '复兴门站', '西单站', '天安门西站', '天安门东站', '王府井站', '东单站', '建国门站', '永安里站', '国贸站', '大望路站', '四惠站', '四惠东站', '高碑店站', '传媒大学站', '双桥站', '管庄站', '八里桥站', '通州北苑站', '果园站', '九棵树站', '梨园站', '临河里站', '土桥站', '花庄站'], '复八线': ['黑石头站', '高井站', '福寿岭站', '苹果园站', '古城站', '衙门口站', '八角游乐园站', '八宝山站', '玉泉路站', '五棵松站', '万寿路站', '公主坟站', '军事博物馆站', '木樨地站', '南礼士路站', '复兴门站', '西单站', '天安门西站', '天安门东站', '王府井站', '东单站', '建国门站', '永安里站', '国贸站', '大望路站', '四惠站', '四惠东站', '高碑店站', '传媒大学站', '双桥站', '管庄站', '八里桥站', '通州北苑站', '果园站', '九棵树站', '梨园站', '临河里站', '土桥站', '花庄站'], '北京地铁13号线': ['西直门站', '大钟寺站', '知春路站', '五道口站', '上地站', '西二旗站', '龙泽站', '回龙观站', '霍营站', '立水桥站', '北苑站', '望京西站', '芍药居站', '光熙门站', '柳芳站', '东直门站'], '北京地铁八通线': ['四惠站', '土桥站'], '北京地铁5号线': ['宋家庄站', '刘家窑站', '蒲黄榆站', '天坛东门站', '磁器口站', '崇文门站', '东单站', '灯市口站', '东四站', '张自忠路站', '北新桥站', '雍和宫站', '和平里北街站', '和平西桥站', '惠新西街南口站', '惠新西街北口站', '大屯路东站', '北苑路北站', '立水桥南站', '立水桥站', '天通苑南站', '天通苑站', '天通苑北站'], '北京地铁8号线': ['朱辛庄站', '朱辛庄站', '中国美术馆站、珠市口站-瀛海站', '金鱼胡同站-前门站', '瀛海站'], '北京地铁10号线': ['巴沟站', '苏州街站', '海淀黄庄站', '知春里站', '知春路站', '西土城站', '牡丹园站', '健德门站', '北土城站', '安贞门站', '惠新西街南口站', '芍药居站', '太阳宫站', '三元桥站', '亮马桥站', '农业展览馆站', '团结湖站', '呼家楼站', '金台夕照站', '国贸站', '双井站', '劲松站', '潘家园站', '十里河站', '分钟寺站', '成寿寺站', '宋家庄站', '石榴庄站', '大红门站', '角门东站', '角门西站', '草桥站', '纪家庙站', '首经贸站', '丰台站', '泥洼站', '西局站', '六里桥站', '莲花桥站', '公主坟站', '西钓鱼台站', '慈寿寺站', '车道沟站', '长春桥站', '火器营站', '巴沟站'], '北京地铁机场线': ['东直门站', '三元桥站', '3号航站楼站', '2号航站楼站'], '北京地铁4号线': ['公益西桥站', '角门西站', '马家堡站', '北京南站', '陶然亭站', '菜市口站', '宣武门站', '西单站', '灵境胡同站', '西四站', '平安里站', '新街口站', '西直门站', '动物园站', '国家图书馆站', '魏公村站', '人民大学站', '海淀黄庄站', '中关村站', '北京大学东门站', '圆明园站', '西苑站', '北宫门站', '安河桥北站'], '北京地铁15号线': ['清华东路西口站', '六道口站', '北沙滩站', '奥林匹克公园站', '安立路站', '大屯路东站', '关庄站', '望京西站', '望京站', '望京东站', '崔各庄站', '马泉营站', '孙河站', '国展站', '花梨坎站', '后沙峪站', '南法信站', '石门站', '顺义站', '俸伯站'], '北京地铁昌平线': ['西土城站<sup class="sup--normal" data-sup="39" data-ctrmap=":39,">\n[39]</sup><a class="sup-anchor" name="ref_[39]_2157525">&nbsp;', '京张高铁（出站）', '北京市郊铁路S2线（出站）', '西二旗站', '生命科学园站', '朱辛庄站', '巩华城站', '沙河站', '沙河高教园站', '南邵站', '北邵洼站', '昌平东关站', '昌平站', '昌平北站', '十三陵景区站', '昌平西山口站'], '北京地铁大兴线': ['天宫院站', '生物医药基地站', '义和庄站', '黄村火车站', '黄村西大街站', '清源路站', '枣园站', '高米店南站', '高米店北站', '西红门站', '新宫站', '公益西桥站', '角门西站', '马家堡站', '北京南站', '陶然亭站', '菜市口站', '宣武门站', '西单站', '灵境胡同站', '西四站', '平安里站', '新街口站', '西直门站', '动物园站', '国家图书馆站', '魏公村站', '人民大学站', '海淀黄庄站', '中关村站', '北京大学东门站', '圆明园站', '西苑站', '北宫门站', '安河桥北站'], '北京地铁房山线': ['阎村东站', '苏庄站', '良乡南关站', '良乡大学城西站', '良乡大学城站', '良乡大学城北站', '广阳城站', '篱笆房站', '长阳站', '稻田站', '大葆台站', '郭公庄站', '首经贸站', '丰益桥南站'], '北京地铁亦庄线': ['宋家庄站', '肖村站', '岛式站台', '小红门站', '岛式站台', '旧宫站', '侧式站台', '亦庄桥站', '亦庄文化园站', '万源街站', '荣京东街站', '荣昌东街站', '同济南路站', '经海路站', '次渠南站', '岛式站台', '次渠站', '亦庄火车站'], '北京地铁9号线': ['郭公庄站', '丰台科技园站', '岛式站台', '科怡路站', '丰台南路站', '丰台东大街站', '七里庄站', '六里桥站', '侧式站台', '六里桥东站', '北京西站', '军事博物馆站', '白堆子站', '白石桥南站', '国家图书馆站'], '北京地铁6号线': ['金安桥站', '苹果园站', '杨庄站', '西黄村站', '廖公庄站', '田村站', '海淀五路居站', '慈寿寺站', '花园桥站', '白石桥南站', '二里沟站', '车公庄西站', '车公庄站', '平安里站', '北海北站', '南锣鼓巷站', '东四站', '朝阳门站', '东大桥站', '呼家楼站', '金台路站', '十里堡站', '青年路站', '褡裢坡站', '黄渠站', '常营站', '草房站', '物资学院路站', '通州北关站', '通运门站', '北运河西站', '北运河东站', '郝家府站', '东夏园站', '潞城站'], '北京地铁14号线': ['园博园站', '大瓦窑站', '郭庄子站', '大井站', '七里庄站', '西局站', '东管头站', '丽泽商务区站', '菜户营站', '西铁营站', '景风门站', '北京南站', '陶然桥站', '永定门外站', '景泰站', '蒲黄榆站', '方庄站', '十里河站', '北工大西门站', '平乐园站', '九龙山站', '大望路站', '金台路站', '朝阳公园站', '枣营站', '东风北桥站', '将台站', '高家园站', '望京南站', '阜通站', '望京站', '东湖渠站', '来广营站', '善各庄站'], '北京地铁7号线': ['北京西站', '湾子站', '达官营站', '广安门内站', '菜市口站', '虎坊桥站', '珠市口站', '桥湾站', '磁器口站', '广渠门内站', '广渠门外站', '双井站', '九龙山站', '大郊亭站', '百子湾站', '化工站', '南楼梓庄站', '欢乐谷景区站', '垡头站', '双合站', '焦化厂站', '黄厂村站', '豆各庄站', '黑庄户站', '万盛南街西口站', '云景东路站', '小马庄站', '高楼金站', '环球影城站'], '北京地铁16号线': ['宛平站', '榆树庄站', '看丹站', '富丰桥站', '丰台南路站', '丰台站', '丰益桥南站', '丽泽商务区站', '红莲南里站', '达官营站', '木樨地站', '玉渊潭东门站', '甘家口站', '二里沟站', '国家图书馆站', '万寿寺站', '苏州桥站', '苏州街站', '万泉河桥站', '西苑站', '农大南路站', '马连洼站', '西北旺站', '永丰南站', '永丰站', '屯佃站', '稻香湖路站', '温阳路站', '北安河站'], '北京地铁西郊线': ['巴沟站', '颐和园西门站', '茶棚站', '植物园站', '香山站'], '北京地铁S1线': ['苹果园站</i>', '金安桥站', '四道桥站', '桥户营站', '上岸站', '栗园庄站', '小园站', '石厂站'], '北京地铁燕房线': ['阎村东站', '紫草坞站', '阎村站', '星城站', '大石河东站', '马各庄站', '饶乐府站', '房山城关站', '燕山站', '老城区站</i>', '顾册站</i>'], '北京地铁2号线': ['西直门站', '积水潭站', '鼓楼大街站', '安定门站', '雍和宫站', '东直门站', '东四十条站', '朝阳门站', '建国门站', '北京站', '崇文门站', '前门站', '和平门站', '宣武门站', '长椿街站', '复兴门站', '阜成门站', '车公庄站']}
    simple_connection_info=get_sta_relation(subwaydict)
    #最短路径
    des=search1('中关村站-北京地铁4号线', '平安里站', simple_connection_info, sort_candidate=shortest_path_first1)
    print(des)
    #最小换乘
    des1 = search1('中关村站-北京地铁4号线', '平安里站', simple_connection_info, sort_candidate=shortest_path_first)
    print(des1)

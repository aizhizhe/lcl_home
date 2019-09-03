from calcul_sentence import data_preparing
import jieba.posseg as pseg
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # 基于TF-IDF的词频转向量库
from sklearn.cluster import KMeans
import gensim

def get_sen_list(op,sentence):
    senten_list = op.pre_data(sentence)
    return senten_list


def get_words(filename,stop_file):
    op=data_preparing(stop_file)
    with open(filename,"r",encoding="utf-8") as f:
        words_list=[get_sen_list(op,x.split("\t")[-1]) for x in f.read().splitlines()]
    return words_list


def jieba_cut(comment):
    word_list = []  # 建立空列表用于存储分词结果
    seg_list = pseg.cut(comment)  # 精确模式分词[默认模式]
    for word in seg_list:
        if word.flag in ['ns', 'n', 'vn', 'v', 'nr']:  # 选择属性
            word_list.append(word.word)  # 分词追加到列表
    return word_list

def get_sentence_emding(sen_list,model):
    sen_emb=np.zeros(192)
    length=len(sen_list)
    for word in sen_list:
        if word in model.wv:
            w_emd=model.wv[word]
        else:
            w_emd=np.zeros(192)
        sen_emb+=w_emd
    return sen_emb/length

def load_model(model_name):
    model = gensim.models.Word2Vec.load(model_name)
    return model

def julei(filename,stop_file):
    with open(filename,"r",encoding="utf-8") as f:
        com=f.read().splitlines()
    comment_list=get_words(filename,stop_file)
    model = load_model("wikiand_all_news_model.model")
    res = []
    for data in comment_list:
        lins = get_sentence_emding(data, model)
        res.append(lins.tolist())
    X=np.array(res)
    # vectorizer = TfidfVectorizer(tokenizer=jieba_cut, use_idf=True)  # 创建词向量模型
    # X = vectorizer.fit_transform(comment_list)  # 将评论关键字列表转换为词向量空间模型
    # K均值聚类
    model_kmeans = KMeans(n_clusters=20)  # 创建聚类模型对象
    model_kmeans.fit(X)  # 训练模型
    # 聚类结果汇总
    cluster_labels = model_kmeans.labels_  # 聚类标签结果
    res_data={}
    result=model_kmeans.fit_predict(X)
    for i,data in enumerate(com):
        if result[i] not in res_data:
            res_data[result[i]]=[]
        res_data[result[i]].append((data.split("\t")[0],data.split("\t")[1]))
    f=open("lcl_data.txt","w",encoding="utf-8")
    for j in res_data:
        print(j,list(set(res_data[j])))
        if j==0:
            for da in list(set(res_data[j])):
                f.write(da[0]+"\t"+da[1]+"\n")
    f.close()


if __name__=="__main__":
    julei("sentences1.txt","哈工大停用词表扩展.txt")
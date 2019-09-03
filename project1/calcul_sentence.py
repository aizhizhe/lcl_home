'''
建立两个字典
编号：人名
编号：句子
数据预处理，对句子的处理，分词，去停用词，数字0化，大小写转换，多空格用一个替代,全角转半角
然后计算句子之间的相似度，对相似度句子进行排序，使用的是sen2vec计算句子相似度。
提取句子相似度排名靠前的前20个。
'''
import jieba
import gensim
import re
import numpy as np
from collections import defaultdict

class data_preparing(object):
    def __init__(self,stop_filename):
        with open(stop_filename,"r",encoding="utf-8") as f:
            self.stop_words=f.read().splitlines()

    def sub_zero(self,sentence):
        return re.subn("\d+","0",sentence)[0]

    def sub_more_space(self,sentence):
        return re.subn("\s+", " " ,sentence)[0]

    def capital_to_small(self,sentence):
        return sentence.lower()

    def q_to_b(self,q_str):
        """
        全角转半角
        """
        b_str = ""
        for uchar in q_str:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif 65374 >= inside_code >= 65281:  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            b_str += chr(inside_code)
        return b_str

    def drop_stopwords(self,sentence):
        sen_list=jieba.lcut(sentence)
        for data in sen_list[:]:
            if data in self.stop_words:
                sen_list.remove(data)
        return sen_list


    def pre_data(self,sentence):
        new_sen=self.sub_zero(sentence)
        new_sen=self.sub_more_space(new_sen)
        new_sen=self.capital_to_small(new_sen)
        new_sen=self.q_to_b(new_sen)
        new_sen=self.drop_stopwords(new_sen)
        return new_sen

def load_model(model_name):
    model = gensim.models.Word2Vec.load(model_name)
    return model

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

def get_cosin(v1,v2):
    v1m=np.sqrt(v1.dot(v1))
    v2m=np.sqrt(v2.dot(v2))
    if v2m != 0 and v1m != 0:
        sim = (v1.dot(v2)) / (v1m * v2m)
    else:
        sim = 0
    return sim

def get_topk_embding(num,sentence,filename,model_name,stop_file):
    op=data_preparing(stop_file)
    senten1=op.pre_data(sentence)
    model=load_model(model_name)
    f_r=open(filename,"r",encoding="utf-8")
    v1=get_sentence_emding(senten1,model)
    for line in f_r:
        senten2=op.pre_data(line.strip("\n"))
        v2=get_sentence_emding(senten2,model)
        pass

def get_topk_embding1(sentence1,sentence2,model):
    v1=get_sentence_emding(sentence1,model)
    v2=get_sentence_emding(sentence2,model)
    sim=get_cosin(v1,v2)
    return sim


def get_per_and_say(filename,stop_file):
    say_word={}
    words={}
    op = data_preparing(stop_file)
    with open(filename, "r", encoding="utf-8") as f:
        says=list(set(f.read().splitlines()))
    for i,line in enumerate(says):
        sen=line.strip("\n").split("\t")
        key=sen[0]
        value=op.pre_data(sen[1])
        say_word[i]=key
        words[i]=value
    return say_word,words


def get_says_simlar_dict(model_name,filename, stop_file):
    model = load_model(model_name)
    say_word, words = get_per_and_say(filename, stop_file)
    words_sim={}
    for key in words:
        if key not in words_sim:
            words_sim[key]=[]
        for keys in words:
            if key!=keys:
                sim=get_topk_embding1(words[key],words[keys],model)
                if sim>0.5:
                    words_sim[key].append((keys,sim))
        words_sim[key]=sorted(words_sim[key], key=lambda x: x[1], reverse=True)
    return words_sim

def get_related_words(initial_words,words_sim):
    have_seen_solution={}
    unseen = [initial_words]
    for i,data in enumerate(unseen):
        unseen[i]=(data,1)
    seen = defaultdict(int)
    max_size = 10 # could be greater
    while unseen and len(seen) < max_size:
        node = unseen.pop(0)
        if node[0] not in have_seen_solution:
            if node[0] in words_sim:
                have_seen_solution[node[0]]=words_sim[node[0]]
            else:
                have_seen_solution[node[0]]=[]
        new_expanding =[x for x in have_seen_solution[node[0]]]
        unseen += new_expanding
        seen[node[0]] +=1*node[1]
    return seen


def get_num_sim_sentence(filename,stop_file,model_name):
    say_word, words = get_per_and_say(filename, stop_file)
    words_sim=get_says_simlar_dict(model_name,filename,stop_file)
    new_words={}
    for key in words:
        new_words[key]="".join(words[key])
    with open("samilar.txt","a",encoding="utf-8") as f:
        for senkey in new_words:
            f.writelines([str(senkey)+"\t"+new_words[x]+"\n" for x in get_related_words(senkey,words_sim)])
    return words_sim

if __name__=="__main__":
    #首先使用kmeans进行分类，之后进行对每一类进行优化分类。使用广度优先
    get_num_sim_sentence("sentences1.txt","哈工大停用词表扩展.txt","wikiand_all_news_model.model")
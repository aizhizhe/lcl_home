from gensim.test.utils import common_texts,get_tmpfile
from gensim.models import  Word2Vec
from gensim.models import KeyedVectors
from gensim.models.word2vec import LineSentence
import math
import gensim
import pandas as pd
import re,time
import jieba
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from collections import defaultdict

class w2v(object):
    def __init__(self,model_name):
        self.model_name=model_name
        path = get_tmpfile(self.model_name)


    def save_model(self):
        f=open("my.txt","r",encoding="utf-8")#这里面的文本需要是每一行都是用空格隔开的词
        sentences = LineSentence(f)  #经过处理之后[["今天","上午","开会"],["昨天","晚上"]]
        model=Word2Vec(sentences,size=100,window=5,min_count=1,workers=4)
        model.save(self.model_name)


    def continue_train(self,model_name,filename):
        f = open(filename, "r", encoding="utf-8")
        sentences = LineSentence(f)
        model=Word2Vec.load(model_name)
        # model=self.load_model_not_bin(model_name)
        model.build_vocab(sentences,update=True)#极其重要
        model.train(sentences,total_examples=343600,epochs=5)
        model.save("wikiandnews_model.model")


    def save_model_not_bin(self,filename,model):
        model.wv.save_word2vec_format(filename, binary=False)
        return filename


    def save_model_bin(self,filename,model):
        model.wv.save_word2vec_format(filename, binary=True)
        return filename

    def load_model_not_bin(self,filename):
        model_text=KeyedVectors.load_word2vec_format(filename, binary=False)
        return model_text


    def load_model_bin(self,filename):
        model_bin=KeyedVectors.load_word2vec_format(filename, binary=True)
        return model_bin


    def load_model(self,model_name):
        model=gensim.models.Word2Vec.load(model_name)
        return model


    def show_word2vec(self,model,word):
        vector=model.wv[word]
        return vector


    def get_similar_topk(self,word,model):
        items=model.most_similar(word)
        for item in items:
            print(item[0],item[1])




# def split(node):
#     return re.subn("(\d|\.)+", "", node)[0]
#
# csv_path="D:\\lcl_s\\sqlResult_1558435.csv"
# content=pd.read_csv(csv_path,encoding='gb18030')
# content=content.fillna('') #表示原对象不变，其他的用''填充
# news_content=content['content'].tolist()
# # print(len(news_content))
#
# def cut(string):return ' '.join(jieba.lcut(string))
# test=cut("3点到5点")
# # print(test)
#
# def token(string):return re.findall('[\d|\w]+',string)  #匹配字母数字下划线
# test1=token('这是一个测试\n\n\n好的好的好的')
# # print(test1)
# news_content=[token(n) for n in news_content]
# news_content=[' '.join(n) for n in news_content]
# news_content=[cut(n) for n in news_content]
# # print(news_content[1])
# def write_to_file():
#     with open('new_sentences.txt','w',encoding="utf8") as f:
#         for sen in news_content:
#             f.write(sen+'\n')
# write_to_file()
# model=Word2Vec(LineSentence('new_sentences.txt'),size=35,workers=8)
# model.save("new.model")
# model=Word2Vec.load("new.model")
# model.wv.save_word2vec_format("new_model.txt", binary=False)
# model_text=KeyedVectors.load_word2vec_format("new_model.txt", binary=False)
# entit=model_text.most_similar("建议",topn=30)
# for ent in entit:
#     # print(ent[0],ent[1])
#     pass
# # print(news_content[0])
# def document_frequency(word):#统计多少个文档中出现某个词语
#     return sum(1 for n in news_content if word in n)
#
# def idf(word):
#     return math.log10(len(news_content)/document_frequency(word))
#
# def tf(word,document):
#     document_words=document.split()
#     return sum(1 for w in document_words if w==word)/len(document_words)
#
# print(news_content[11])
# # print(document_frequency("的"))

op=w2v("wikiandnews_model")
op.continue_train("D:\\lcl_s\\new.model","D:\\lcl_s\\reduce_zhiwiki.txt")#reduce_zhiwiki.txt
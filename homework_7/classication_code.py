import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba,re
import gensim
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import jieba.posseg as pseg

class data_preparing(object):
    def __init__(self,stop_filename):
        with open(stop_filename,"r",encoding="utf-8") as f:
            self.stop_words=f.read().splitlines()

    def sub_zero(self,sentence):
        sentence=str(sentence)
        sentence=sentence.replace("\u3000","")
        sentence = sentence.replace("\\n","")
        sentence = sentence.replace("\n", "")
        if sentence:
            return re.subn("\d+","0",sentence)[0]
        return "NON"

    def sub_more_space(self,sentence):
        if sentence:
            return re.subn("\s+", " " ,sentence)[0]
        return "NON"

    def capital_to_small(self,sentence):
        if sentence:
            return sentence.lower()
        return "NON"


    def q_to_b(self,q_str):
        """
        全角转半角
        """
        if q_str:
            b_str = ""
            for uchar in q_str:
                inside_code = ord(uchar)
                if inside_code == 12288:  # 全角空格直接转换
                    inside_code = 32
                elif 65374 >= inside_code >= 65281:  # 全角字符（除空格）根据关系转化
                    inside_code -= 65248
                b_str += chr(inside_code)
            return b_str
        return "NON"


    def drop_stopwords(self,sentence):
        if sentence:
            sen_list=jieba.lcut(sentence)
            for data in sen_list[:]:
                if data in self.stop_words:
                    sen_list.remove(data)
            if sen_list:
                return sen_list
        return "NON"


    def pre_data(self,sentence):
        new_sen=self.sub_zero(sentence)
        new_sen=self.sub_more_space(new_sen)
        new_sen=self.capital_to_small(new_sen)
        new_sen=self.q_to_b(new_sen)
        new_sen=self.drop_stopwords(new_sen)
        return new_sen


class G_sentence_w2v(object):
    def get_sentence_w2v(self,model,sen_list):
        # model=gensim.models.Word2Vec.load(model)
        sen_emb = np.zeros(192)
        for word in sen_list:
            if word in model.wv:
                w_emd = model.wv[word]
            else:
                w_emd = np.zeros(192)
            sen_emb += w_emd
        return sen_emb/len(sen_list)

    def get_sen_vec(self,news,model):
        X=[self.get_sentence_w2v(model,dalist).tolist() for dalist in news]
        X=np.array(X)
        return X


def jieba_cut(comment):
    word_list = []  # 建立空列表用于存储分词结果
    seg_list = pseg.cut(comment)  # 精确模式分词[默认模式]
    for word in seg_list:
        if word.flag in ['ns', 'n', 'vn', 'v', 'nr']:  # 选择属性
            word_list.append(word.word)  # 分词追加到列表
    return word_list


def get_possible_one(predict_list,real_Y,real_X):
    for i,data in enumerate(predict_list):
        if int(data)==1 and int(real_Y[i])==0:
            print(real_X[i])


def pre_one_news(sentences,stop_file,model,knn,real_Y):
    op = data_preparing(stop_file)
    sen_list=[]
    for sen in sentences:
        new_sen=op.pre_data(sen)
        sen_list.append(new_sen)
    X=["".join(da) for da in sen_list]
    predict_X_vec = G_sentence_w2v().get_sen_vec(X, model)
    res_list=knn.predict(predict_X_vec)
    get_possible_one(res_list, real_Y, X)


def get_datalist(fname,stop_file):
    # fname='sqlResult_1558435.csv'
    op = data_preparing(stop_file)
    content=pd.read_csv(fname,encoding='gb18030')
    xinhua_news=[]
    other_news=[]
    for i,data in enumerate(content['content']):
        new_data = op.pre_data(data)
        if new_data and new_data != "NON":
            if content['source'][i]=='新华社':
                xinhua_news.append(new_data)
            else:
                other_news.append(new_data)
    news=xinhua_news+other_news
    y1=np.zeros(len(other_news)).tolist()
    y2=np.ones(len(xinhua_news)).tolist()
    Y=y2+y1
    return news,Y

def train_predict_evaluation_model(classifier,train_features,train_labels,test_features,test_labels):
    classifier.fit(train_features,train_labels)
    predictions=classifier.predict(test_features)
    res=classification_report(test_labels,predictions)
    return res,predictions


def train_data(fname,stop_file,model_file):
    model = gensim.models.Word2Vec.load(model_file)
    X,Y=get_datalist(fname,stop_file)
    train_X,test_X,train_Y,test_Y=train_test_split(["".join(da) for da in X],Y,test_size=0.3,train_size=0.7)
    train_Y=np.array(train_Y)
    test_Y = np.array(test_Y)
    #也可以使用tfidf，但是效果不好
    # vectorizer = TfidfVectorizer(tokenizer=jieba_cut, use_idf=True)  # 创建词向量模型
    # trainX = vectorizer.fit_transform(train_X)  # 将评论关键字列表转换为词向量空间模型
    # testX=vectorizer.transform(test_X)
    train_X_vec=G_sentence_w2v().get_sen_vec(train_X,model)
    test_X_vec = G_sentence_w2v().get_sen_vec(test_X, model)
    knn = KNeighborsClassifier()
    logis = LogisticRegression()
    lr=MultinomialNB()
    svm=SVC()
    RF=RandomForestClassifier()
    DecisionTree=DecisionTreeClassifier()
    res,predicions=train_predict_evaluation_model(knn,train_X_vec, train_Y,test_X_vec,test_Y)
    res1, predicions1 = train_predict_evaluation_model(logis, train_X_vec, train_Y, test_X_vec, test_Y)
    res2, predicions2 = train_predict_evaluation_model(lr, train_X_vec, train_Y, test_X_vec, test_Y)
    res3, predicions3 = train_predict_evaluation_model(svm, train_X_vec, train_Y, test_X_vec, test_Y)
    res4, predicions4 = train_predict_evaluation_model(RF, train_X_vec, train_Y, test_X_vec, test_Y)
    res5, predicions5 = train_predict_evaluation_model(DecisionTree, train_X_vec, train_Y, test_X_vec, test_Y)
    print("KNN=====\n",res)
    print("logistic=====\n", res1)
    print("bayes=====\n", res2)
    print("svm=====\n", res3)
    print("RF=====\n", res4)
    print("DecisionTree=====\n", res5)
    # get_possible_one(predicions, test_Y, test_X)
    # knn = KNeighborsClassifier()
    # 训练knn
    # knn.fit(train_X_vec, train_Y)
    # res_list = knn.predict(test_X_vec)
    # target_names=list(set(test_Y))
    # print(classification_report(test_Y,res_list))
    # get_possible_one(predicions,test_Y,test_X)


if __name__=="__main__":
    train_data('sqlResult_1558435.csv',"哈工大停用词表扩展.txt","../project/wikiand_all_news_model.model")


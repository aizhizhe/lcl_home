"""
作业
2. 使用新数据源完成语言模型的训练

"""
from collections import Counter
import jieba
import re

def file_op(filename,op):
    f=open(filename,op,encoding="utf-8")
    return f
def token(line):
    return "".join(re.findall("\w+",line))
def split_words(line):
    linelist=jieba.lcut(line)
    return linelist
def clean_data(line,split=" ++$++ "):
    line=line.strip('\n').split(split)
    return line[2]

def get_worddict(filename):
    f_r=file_op(filename,"r")
    res=[['BEGIN']+jieba.lcut(token(clean_data(line)))+['END'] for line in f_r]
    words=[]
    for wordslist in res:
        words+=wordslist
    return words
def get_2_w(words):
    two_words=["".join(x for x in words[i:i+2]) for i in range(len(words)-1)]
    return {k:v for k,v in Counter(two_words).items()}
def get_word(words):
    return {k:v for k,v in Counter(words).items()}
def count_w(word):
    global worddict
    if word not in worddict:
        return 1
    return worddict[word]
def count_2w(words):
    global wordsdict
    if words not in wordsdict:
        return 1
    return wordsdict[words]
def pro(word,next_w):
    return count_2w(word+next_w)/(count_w(next_w) +1)

def count_ngram(line):
    p=1
    linelist=split_words(line)
    for i,word in enumerate(linelist[:-1]):
        next_w=linelist[i+1]
        p*=pro(word,next_w)
    return p

def get_p(line):
    global wordsdict,worddict
    wordslist=get_worddict("train.txt")
    worddict=get_word(wordslist)
    wordsdict=get_2_w(wordslist)
    p=count_ngram(line)
    return p
if __name__=="__main__":
    line="今天能不能上给上个保险啊"
    print(get_p(line))
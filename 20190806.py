import pandas as pd
import re,time
import jieba
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from collections import defaultdict
#取“说”的近似20个词，然后对于每一个近似词A再次取20个近似词，
# 如果在子轮次中出现的词C在父轮次C也出现，那么就将A,C作为“说”真正的近似词

# def split(node):
#     return re.subn("(\d|\.)+", "", node)[0]

def get_related_words(initial_words,model):
    have_seen_solution={}
    unseen = initial_words
    for i,data in enumerate(unseen):
        unseen[i]=(data,1)
    seen = defaultdict(int)
    max_size = 500  # could be greater
    while unseen and len(seen) < max_size:
        if len(seen) % 50 == 0:
            print('seen length : {}'.format(len(seen)))
        node = unseen.pop(0)
        if node[0] not in have_seen_solution:
            have_seen_solution[node[0]]={(w,s) for w, s in model.most_similar(node[0], topn=20)}
        new_expanding =[x for x in have_seen_solution[node[0]]]
        unseen += new_expanding
        seen[node[0]] +=1*node[1]
        # optimal: 1. score function could be revised
        # optimal: 2. using dymanic programming to reduce computing time
    return seen

# csv_path="sqlResult_1558435.csv"
# content=pd.read_csv(csv_path,encoding='gb18030')
# content=content.fillna('') #表示原对象不变，其他的用''填充
# news_content=content['content'].tolist()
# print(len(news_content))
#
# def cut(string):return ' '.join(jieba.lcut(string))
# test=cut("3点到5点")
# print(test)
#
# def token(string):return re.findall('[\d|\w]+',string)  #匹配字母数字下划线
# test1=token('这是一个测试\n\n\n好的好的好的')
# print(test1)
# news_content=[token(n) for n in news_content]
# news_content=[' '.join(n) for n in news_content]
# news_content=[cut(n) for n in news_content]
# print(news_content[1])
# def write_to_file():
#     with open('new_sentences.txt','w',encoding="utf8") as f:
#         for sen in news_content:
#             f.write(sen+'\n')
# write_to_file()
# model=Word2Vec(LineSentence('new_sentences.txt'),size=35,workers=8)
# model.save("new.model")
model=Word2Vec.load("pre_say/wikiandnews_model.model")
# model.wv.save_word2vec_format("new_model.txt", binary=False)
# model_text=KeyedVectors.load_word2vec_format("new_model.txt", binary=False)
# entit=model_text.most_similar("建议",topn=30)
# for ent in entit:
#     print(ent[0],ent[1])


related_words = get_related_words(['说', '表示'], model)
res=sorted(related_words.items(), key=lambda x: x[1], reverse=True)
print(res)


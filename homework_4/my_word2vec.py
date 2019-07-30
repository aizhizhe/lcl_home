import jieba
import gensim
from pylab import *
mpl.rcParams['font.sans-serif']=['SimHei']
from gensim.corpora import WikiCorpus
from langconv import *
import os
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)


class w2v(object):
	def __init__(self,w_filename,read_filename):
		'''
		initialization
		:param w_filename: wikidatafile after pre-processing
		:param read_filename:the original wikifile
		'''
		self.writeto_wikifile=w_filename
		self.zhwiki_name = read_filename
		self.model=None

	def load_wikidata(self):
		'''
		load wikidata and data pre-processing
		:return:
		'''
		i=0
		f=open(self.writeto_wikifile,'w',encoding="utf-8")
		wiki=WikiCorpus(self.zhwiki_name,lemmatize=False,dictionary={})
		for text in wiki.get_texts():
			seg=""
			for temp_sentence in text:
				temp_sentence=Converter('zh-hans').convert(temp_sentence)
				seg+=" ".join(jieba.lcut(temp_sentence))
			f.write(seg+'\n')
			i=i+1
			if(i%200==0):
				print("Saved"+str(i)+"articles")
		f.close()


	def train_w2v_model(self):
		'''train model and save'''
		wiki_news = open(self.writeto_wikifile, 'r', encoding='utf-8')
		self.model = Word2Vec(LineSentence(wiki_news), sg=0, size=192, window=5, min_count=5, workers=9)
		self.model.save('zhiwiki_news.word2vec')


	def judge_model(self):
		if not self.model:
			if os.path.exists("zhiwiki_news.word2vec"):
				self.model = gensim.models.Word2Vec.load("zhiwiki_news.word2vec")
			else:
				self.train_w2v_model()

	def test_sim_of_two_words(self,oneword,otherword):
		self.judge_model()
		print(self.model.similarity(oneword, otherword))


	def test_most_sim(self,word):
		self.judge_model()
		if word in self.model.wv.index2word:
			print(self.model.most_similar(word))

	def tsne_plot(self):
		self.judge_model()
		"Creates and TSNE model and plots it"
		labels = []
		tokens = []
		num=0
		for word in self.model.wv.vocab:
			num+=1
			if num==1000:
				break
			tokens.append(self.model[word])
			labels.append(word)

		tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
		new_values = tsne_model.fit_transform(tokens)

		x = []
		y = []
		for value in new_values:
			x.append(value[0])
			y.append(value[1])

		plt.figure(figsize=(32, 32))
		for i in range(len(x)):
			plt.scatter(x[i], y[i])
			plt.annotate(labels[i],
						 xy=(x[i], y[i]),
						 xytext=(5, 2),
						 textcoords='offset points',
						 ha='right',
						 va='bottom')
		# plt.show()
		plt.savefig("filename.png")


if __name__=='__main__':
	word2vec=w2v("reduce_zhiwiki.txt","E:\\拷贝文件\\最近文件桌面正常使用\\代码\\zhwiki-latest-pages-articles.xml.bz2")
	word2vec.test_most_sim("西红柿")
	# word2vec.load_wikidata()
	# word2vec.train_w2v_model()
	# word2vec.tsne_plot()



"""
Source:
https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/
"""
import re
import numpy as np
from pprint import pprint
import json

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import os.path
# spacy for lemmatization
import spacy
from nltk.corpus import stopwords
import collections
from heapq import heappush, heappop
import pickle
def sent_to_words(sentences):
	for sentence in sentences:
		yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))


def remove_stopwords(texts, stop_words):
	return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts, bigram_mod):
	return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts, bigram_mod):
	return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(nlp, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
	texts_out = []
	for sent in texts:
		doc = nlp(" ".join(sent)) 
		texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
	return texts_out


def main():

	stop_words = stopwords.words('english')
	stop_words.extend(['ref', 'type', 'target', 'imag', 'method', 'figur'])

	data = []
	title_to_idx = {}
	cnt = 0
	with open('test/test.dat', 'r') as f:
		line  = f.readline()
		data.append(line)
		cnt
		title_to_idx[cnt] = line[:100].split(" |")[0]
		while line:
			cnt += 1
			line  = f.readline()
			title_to_idx[cnt] = line[:100].split(" |")[0]
			data.append(line)

	data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
	data = [re.sub('\s+', ' ', sent) for sent in data]
	data = [re.sub("\'", "", sent) for sent in data]

	data_words = list(sent_to_words(data))

	bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
	trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

	bigram_mod = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)

	data_words_nostops = remove_stopwords(data_words, stop_words)
	data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

	nlp = spacy.load('en', disable=['parser', 'ner'])
	data_lemmatized = lemmatization(nlp, data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])


	id2word = corpora.Dictionary(data_lemmatized)

	texts = data_lemmatized
	corpus = [id2word.doc2bow(text) for text in texts]

	if not os.path.isfile('gensim_model'):
		tpc = 7
		lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
													id2word=id2word,
													num_topics=tpc, 
													random_state=100,
													update_every=1,
													chunksize=100,
													passes=10,
													alpha='auto',
													per_word_topics=True)

		lda_model.save("gensim_model")
		print("gensim_model saved ... ")
	else:
		lda_model = lda_model = gensim.models.ldamodel.LdaModel.load("gensim_model")

	with open('gensim-topic_core.txt','w+') as file:
		for topic_id, comb in lda_model.print_topics():
			file.write(str([(topic.split("*")[1]).replace("\"", "").replace(" ", "") for topic in comb.split("+") ])+"\n")


	# pprint(lda_model.print_topics())
	# doc_lda = lda_model[corpus]
	get_document_topics = [lda_model.get_document_topics(item) for item in corpus]
	print("===============")
	print(len(title_to_idx))
	print(len(get_document_topics))
	print("===============")
	print(get_document_topics[:10])
	print("===============")

	output = collections.defaultdict(list)
	mapping = {0:"Dataset", 1:"Graphic", 2:"Video", 3:"Similarity", 4:"Object Detection", 5:"Convolution", 6:"Points"}

	for idx, ll in enumerate(get_document_topics):
		heap = []
		for topic, prob in ll:
			heappush(heap, (prob, mapping[topic]))
			if len(heap) > 2:
				heappop(heap)
		while heap:
			output[title_to_idx[idx]].append(heappop(heap))

	with open('gensim-topic-mapping.p', 'wb') as fp:
		pickle.dump(data, fp)
	with open('gensim-topic-mapping.txt','w+') as file:
		for key, val in output.items():
			file.write(str(key) + " " + str(val) + "\n")

	def metrics():
		print('\nPerplexity: ', lda_model.log_perplexity(corpus))
		coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
		coherence_lda = coherence_model_lda.get_coherence()
		print('\nCoherence Score: ', coherence_lda)	

	# metrics()

	# for tpc in [4, 5, 6, 7, 8]:
	# 	print("=====" + str(tpc) + "=====")
	# 	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
	# 												id2word=id2word,
	# 												num_topics=tpc, 
	# 												random_state=100,
	# 												update_every=1,
	# 												chunksize=100,
	# 												passes=10,
	# 												alpha='auto',
	# 												per_word_topics=True)
	# metrics()

if __name__ == "__main__":
	main()
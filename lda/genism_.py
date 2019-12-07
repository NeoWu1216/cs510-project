"""
Source:
https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#2prerequisitesdownloadnltkstopwordsandspacymodelforlemmatization
"""
import re
import numpy as np
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy
from nltk.corpus import stopwords

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
	with open('test/test.dat', 'r') as f:
		line  = f.readline()
		data.append(line)
		while line:
			line  = f.readline()
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


	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
												id2word=id2word,
												num_topics=8, 
												random_state=100,
												update_every=1,
												chunksize=100,
												passes=10,
												alpha='auto',
												per_word_topics=True)

	pprint(lda_model.print_topics())
	doc_lda = lda_model[corpus]



if __name__ == "__main__":
	main()
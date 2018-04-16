# -*- coding: UTF-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import dit
from dit.divergences import jensen_shannon_divergence

def GetWordProb (Corpus):
	countvectorizer = CountVectorizer()
	WordSenCount = np.array(countvectorizer.fit_transform(Corpus).toarray())
	Words = countvectorizer.get_feature_names()
	WordCount = np.sum(WordSenCount, axis = 0)
	WordProb = [(c / np.sum(WordCount)) for c in WordCount]
	return Words, WordProb

def JSDivergence (Corpus_P, Corpus_Q):
	Words_P, WordProb_P = GetWordProb(Corpus_P)
	Words_Q, WordProb_Q = GetWordProb(Corpus_Q)
	P = dit.ScalarDistribution(Words_P, WordProb_P)
	Q = dit.ScalarDistribution(Words_Q, WordProb_Q)
	return jensen_shannon_divergence([P, Q])
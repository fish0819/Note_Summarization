# -*- coding: UTF-8 -*-
from googletrans import Translator
translator = Translator()
sen = '3. 計算the payoff table showing the payoff for each選項in each event'
sen = translator.translate(sen).text
print (sen)

for i in range(10):
	print (hex(ord(str(i))))

# coding: utf-8 
# from nltk.tokenize import StanfordSegmenter
# from nltk.parse.corenlp import CoreNLPParser

# segmenter = StanfordSegmenter(
# 	path_to_sihan_corpora_dict= '/home/linusp/stanford/segmenter/data/',
# 	path_to_model= '/home/linusp/stanford/segmenter/data/pku.gz',
# 	path_to_dict= '/home/linusp/stanford/segmenter/data/dict-chris6.ser.gz'
# )
# res = segmenter.segment('Guangdong University of Foreign Studies is located in Guangzhou.')
# print  (type (res))
# print (res.encode( 'utf-8' ))



# SentenceList = []
# with open ('Supplement-A.txt', 'r', encoding = 'UTF-8') as inFile:
# 	SentenceList = inFile.readlines()
# SentenceList = [s.replace('\n', '').strip() for s in SentenceList]
# print (SentenceList)

# text = '	  Hello world!\n  \n	 What a good day.   '
# print (text)
# print ([s.strip() for s in text.splitlines()])
# text = text.strip()
# print (text)


# with open ('Supplement-A.txt', 'r') as inFile:
# 	LineList = inFile.readlines()
# text = ''
# for i in range(len(LineList)):
# 	if LineList[i] == '': text += '\n'
# 	elif LineList[i][-1] == '-': text += LineList[i][:len(LineList[i])]
# 	else: text += (LineList[i] + ' ')
# print (text)



# import re # for regular expression
# text = 'gfgfdAAA1234ZZZuijjkAAAA123333ZZZZZ'
# m = re.search('AAA(.+?)ZZZ', text)
# print (m)
# if m:
# 	print (m.group(0))
# 	print (m.group(1))
# m = re.search(', \d', 'Algebraic solution, in linear programming, 614–615')
# if m:
# 	print (m.start())
# m = re.search(', \d', 'Algebraic')
# if m:
# 	print (m.start())

# pattern = re.compile('\.[A-Z]')
# text = 'A good day.Hi!'
# print (pattern.match(text))
# result = re.search('\.[A-Z]', text)
# if result:
# 	print (result)
# 	print (result.group(0))

# from sklearn.metrics.pairwise import cosine_similarity

# print (cosine_similarity([1, 2, 0], [2, 2, 1]))


# import numpy
# from numpy import linalg # l2 norm

# List_x = [0, 1, 3, 2]
# List_y = [1, 1, 0, 1]

# dotProduct = numpy.dot(List_x, List_y)
# print ('dotProduct:', dotProduct)
# norm_x = linalg.norm(List_x)
# norm_y = linalg.norm(List_y)
# print ('norm_x', norm_x)
# print ('norm_y', norm_y)
# if norm_x * norm_y > 0:
# 		print (dotProduct / norm_x * norm_y)
# else: print (0)
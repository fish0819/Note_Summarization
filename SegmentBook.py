# -*- coding: UTF-8 -*-
import nltk.data # split text on sentences
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np # average and standard deviation
from numpy import linalg # l2 norm
import math # check inf
import re
import sys
import GetDocuments
import TSF

SUBJECT = 'DS'
CHAPTER = 'ch7'
THRESHOLD_DISSIM = 0.3
SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
THRESHOLD_DISSIM = float(sys.argv[3])
print (SUBJECT, CHAPTER, THRESHOLD_DISSIM)

# parameter setting
K = 10 # the number of sentences in a block

# get content
BOOK_FOLDER = 'book/' + SUBJECT + '/'
BOOK_FILE_NAME = CHAPTER + '.txt'
BOOKPARA_FILE_NAME = CHAPTER + '_TSF.txt'
with open (BOOK_FOLDER + BOOK_FILE_NAME, 'r', encoding = 'UTF-8') as inFile:
    RawParagraphList = inFile.readlines()
RawParagraphList = [s.replace('\n', '').strip() for s in RawParagraphList]
#nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
SentenceList = []
for para in RawParagraphList:
    SentenceList += senTokenizer.tokenize(para)
    for sid in range(len(SentenceList)):
        SentenceList[sid] = SentenceList[sid].strip()
        if re.match('(\d)+$', SentenceList[sid]): SentenceList[sid] = ''
        if re.match('(\d)+\.$', SentenceList[sid]): SentenceList[sid] = ''
    SentenceList = [s for s in SentenceList if (len(s) > 0)]

ParaSenList = TSF.SegementPara(SentenceList, K, THRESHOLD_DISSIM)

with open (BOOK_FOLDER + BOOKPARA_FILE_NAME, 'w', encoding = 'utf-8') as outFile:
  for para in ParaSenList:
      for sen in para:
          outFile.write(sen + '\n')
      outFile.write('\n')

# for para in ParaSenList:
#   for sen in para:
#       print (sen)
#   print ()

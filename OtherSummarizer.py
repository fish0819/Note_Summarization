# -*- coding: utf-8 -*-
import sys
import os
import GetDocuments
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.random import RandomSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

SUBJECT = 'OM'
CHAPTER = 'supplementA'
SELECTEDRATIO = 0.1

SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
SELECTEDRATIO = abs(round(float(sys.argv[3]), 1))
print (SUBJECT, CHAPTER, SELECTEDRATIO)

BOOK_FOLDER = 'book/' + SUBJECT + '/'
SUMMARY_FOLDER = 'result/' + SUBJECT + '/others/'
BOOKPARA_FILE_NAME = CHAPTER + '_TSF.txt'

if not os.path.isdir(SUMMARY_FOLDER):
	os.makedirs(SUMMARY_FOLDER)

BookParaList = GetDocuments.GetBookParaText(BOOK_FOLDER + BOOKPARA_FILE_NAME)
TOTALSENNUM = 0
BookSenList = ''
for p in BookParaList:
	TOTALSENNUM += len(p)
	BookSenList += ' '.join(p) + '\n'
SELECTEDSENNUM = int(round(TOTALSENNUM * SELECTEDRATIO))
LANGUAGE = "english"
# parser = PlaintextParser.from_file(BOOK_FOLDER + BOOKPARA_FILE_NAME, Tokenizer(LANGUAGE))
parser = PlaintextParser.from_string(BookSenList, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)

SummarizerList = [['Random', RandomSummarizer(stemmer)], ['Luhn', LuhnSummarizer(stemmer)], ['TextRank', TextRankSummarizer(stemmer)], ['LexRank', LexRankSummarizer(stemmer)], ['LSA', LsaSummarizer(stemmer)], ['SumBasic', SumBasicSummarizer(stemmer)]]

for i in range(len(SummarizerList)):
	SummarizerList[i][1].stop_words = get_stop_words(LANGUAGE)
	SUMMARY_FILE_NAME = 'Summary_' + SummarizerList[i][0] + '_' + CHAPTER + '.txt'
	with open(SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'w', encoding = 'utf-8') as outFile:
		for sentence in SummarizerList[i][1](parser.document, SELECTEDSENNUM):
			outFile.write(sentence._text + '\n')

''' Jensen-Shannon Divergence '''
import sys
from os import listdir
import os.path
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import dit
from dit.divergences import jensen_shannon_divergence
import csv
import GetDocuments
import JSDivergence as jsd

SUBJECT = 'OM'
CHAPTER = 'ch7'

SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
THRESHOLD_COSSIM = sys.argv[3]
print (SUBJECT, CHAPTER, THRESHOLD_COSSIM)

NOTE_FOLDER = 'note/' + SUBJECT + '/' + CHAPTER + '/'
BOOK_FOLDER = 'book/' + SUBJECT + '/'
JSD_FOLDER = 'result/'
TSFBOOK_FILE_NAME = CHAPTER + '_TSF.txt'
SUMMARY_FOLDER = 'result/' + SUBJECT + '/others/'
MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '.csv'
JSD_FILE_NAME = SUBJECT + '_others_jsd.csv'

StopWords = GetDocuments.GetStopWords('stopwords.txt')
SelectedParaSenList = []
SelectedParaSenNum = []

NoteParaList = GetDocuments.GetNoteParaText(NOTE_FOLDER + MIXEDNOTEPARA_FILE_NAME)
BookParaList = GetDocuments.GetBookParaText(BOOK_FOLDER + TSFBOOK_FILE_NAME)
totalSenNum = 0
for para in BookParaList:
	totalSenNum += len(para)

NoteCorpus = []
for np in NoteParaList:
	NoteCorpus += np
BookCorpus = []
for BP in BookParaList:
	BookCorpus += BP

Summarizers = ['Random', 'Luhn', 'TextRank', 'LexRank', 'LSA']
NSJSDList = []
BSJSDList = []
for i in range(len(Summarizers)):
	SUMMARY_FILE_NAME = 'Summary_' + Summarizers[i] + '_' + CHAPTER + '.txt'
	with open(SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'r', encoding = 'utf-8') as inFile:
		SelectedSenList = inFile.readlines()
	totalSelectedSenNum = len(SelectedSenList)
	# jsd for entire summary and note
	SummaryCorpus = SelectedSenList
	NSJSDList.append(jsd.JSDivergence(NoteCorpus, SummaryCorpus))
	BSJSDList.append(jsd.JSDivergence(BookCorpus, SummaryCorpus))

''' write file '''
needTitle = True
title = ['Subject', 'Chapter', 'Summarizer', 'JS(N,S)', 'JS(B,S)', 'Total_SelectSenNum', 'Total_BookSenNum']
if os.path.isfile(JSD_FOLDER + JSD_FILE_NAME): needTitle = False
with open (JSD_FOLDER + JSD_FILE_NAME, 'a', newline='', encoding = 'utf-8') as outFile: # append
	writer = csv.writer(outFile, delimiter = ',')
	if needTitle:
		writer.writerow(title)
	for i in range(len(Summarizers)):
		writer.writerow([SUBJECT, CHAPTER, Summarizers[i], NSJSDList[i], BSJSDList[i], totalSelectedSenNum, totalSenNum])
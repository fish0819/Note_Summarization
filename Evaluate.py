# -*- coding: UTF-8 -*-
''' prameter setting '''
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
alpha = 0.1
beta = 0.1
gamma = 0.8
THRESHOLD_COSSIM = 0.2

# # used to decide alpha, beta and gamma
# UselessList = ['Summarization', 'result', '\\', '_cossim']
# rawArgument = sys.argv[2]
# for u in UselessList: rawArgument = rawArgument.replace(u, ' ')
# tmpArgList = rawArgument.split()
# SUBJECT = tmpArgList[0]
# CHAPTER = tmpArgList[2].replace('Summary_', '').replace('.csv', '')
# [alpha, beta, gamma] = tmpArgList[1].split(',')
# THRESHOLD_COSSIM = float(sys.argv[3])

# used to decide threshold of fscore
SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
alpha = abs(round(float(sys.argv[3]), 1))
beta = abs(round(float(sys.argv[4]), 1))
if alpha + beta > 1: sys.exit()
gamma = abs(round(1 - alpha - beta, 1))
THRESHOLD_COSSIM = float(sys.argv[5])
THRESHOLD_SCORE = abs(round(float(sys.argv[6]), 2))
print (SUBJECT, CHAPTER, alpha, beta, gamma, THRESHOLD_COSSIM, THRESHOLD_SCORE)

NOTE_FOLDER = 'note/' + SUBJECT + '/' + CHAPTER + '/'
BOOK_FOLDER = 'book/' + SUBJECT + '/'
JSD_FOLDER = 'result/'
TSFBOOK_FILE_NAME = CHAPTER + '_TSF.txt'
# SUMMARY_FOLDER = 'result/' + SUBJECT + '/' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + '/'
SUMMARY_FOLDER = 'result/' + SUBJECT + '/' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + '/' + str(THRESHOLD_SCORE) + '/'
SUMMARY_FILE_NAME = 'Summary_' + CHAPTER + '.csv'
MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '.csv'
# JSD_FILE_NAME = SUBJECT + '.csv'
# JSD_FILE_NAME = SUBJECT + '_thresscore.csv'
JSD_FILE_NAME = SUBJECT + '_jsd.csv'
# SELECTEDSENNUM_FILE_NAME = SUBJECT + '_thresscore_sennum.csv'

StopWords = GetDocuments.GetStopWords('stopwords.txt')
MatchPNList = []
SelectedParaSenList = []
totalSelectedSenNum = 0
with open (SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        if row['pid'] != '':
            npid, pid = int(row['npid']), int(row['pid'])
            pidlist = [match[0] for match in MatchPNList]
            if pid not in pidlist:
                MatchPNList.append([pid, [npid]])
                SelectedParaSenList.append(row['sentence'].lower().replace('[\'', '').replace('\']', '').replace('[]', '').split('\', \''))
                totalSelectedSenNum += len(SelectedParaSenList[-1])
            else:
                MatchPNList[pidlist.index(pid)][1].append(npid)
avgSelectedSenNum = totalSelectedSenNum / len(SelectedParaSenList)
MatchPNList, SelectedParaSenList = zip(*sorted(zip(MatchPNList, SelectedParaSenList)))

NoteParaList = GetDocuments.GetNoteParaText(NOTE_FOLDER + MIXEDNOTEPARA_FILE_NAME)
BookParaList = GetDocuments.GetBookParaText(BOOK_FOLDER + TSFBOOK_FILE_NAME)
totalSenNum = 0
for para in BookParaList:
    totalSenNum += len(para)

# find NoteCorpus and SummaryCorpus
NoteCorpus = []
for np in NoteParaList:
    NoteCorpus += np
SummaryCorpus = []
for m in range(len(MatchPNList)):
    SummaryCorpus += SelectedParaSenList[m]
    # for npid in MatchPNList[m]:
    #     NoteCorpus += NoteParaList[npid] # note para

# jsd for entire summary and note
BookCorpus = []
for BP in BookParaList:
    BookCorpus += BP
EntireDocumentJSD_NS = jsd.JSDivergence(NoteCorpus, SummaryCorpus)
EntireDocumentJSD_BS = jsd.JSDivergence(BookCorpus, SummaryCorpus)

''' write file '''
needTitle = True
title = ['Subject', 'Chapter', 'Alpha', 'Beta', 'Gamma', 'Threshold_FScore', 'JS(N,S)', 'JS(B,S)', 'Avg_SelectSenNum', 'Total_SelectSenNum', 'Total_BookSenNum']
if os.path.isfile(JSD_FOLDER + JSD_FILE_NAME): needTitle = False
with open (JSD_FOLDER + JSD_FILE_NAME, 'a', newline='', encoding = 'utf-8') as outFile: # append
    writer = csv.writer(outFile, delimiter = ',')
    if needTitle:
        writer.writerow(title)
    writer.writerow([SUBJECT, CHAPTER, alpha, beta, gamma, THRESHOLD_SCORE, EntireDocumentJSD_NS, EntireDocumentJSD_BS, avgSelectedSenNum, totalSelectedSenNum, totalSenNum])

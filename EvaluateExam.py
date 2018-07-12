# -*- coding: UTF-8 -*-
import sys
from os import listdir
import os.path
import nltk
import re
import numpy as np
import dit
from dit.divergences import jensen_shannon_divergence
import csv
import GetDocuments
import JSDivergence as jsd

ExamChapters = {
    'OM': [['ch1', 'supplementA', 'ch3', 'ch6', 'ch7', 'ch8'], ['ch9', 'ch15', 'ch16'], ['ch10', 'ch12']], 
    'DS': [['ch2', 'ch3'], ['ch4', 'ch5', 'ch6'], ['ch6', 'ch7', 'ch9']] 
}

SUBJECT = 'OM'
EXAM = 1
alpha = 0.2
beta = 0.5
gamma = 0.3
THRESHOLD_COSSIM = 0.2
THRESHOLD_SCORE = 0.2

SUBJECT = sys.argv[1]
EXAM = int(sys.argv[2])
alpha = abs(round(float(sys.argv[3]), 1))
beta = abs(round(float(sys.argv[4]), 1))
gamma = abs(round(1 - alpha - beta, 1))
THRESHOLD_COSSIM = float(sys.argv[5])
THRESHOLD_SCORE = abs(round(float(sys.argv[6]), 2))
EXAM_NAME = 'exam' + str(EXAM)
print (SUBJECT, EXAM_NAME, alpha, beta, gamma, THRESHOLD_COSSIM, THRESHOLD_SCORE)

EXAM_FOLDER = 'exam/' + SUBJECT + '/'
BOOK_FOLDER = 'book/' + SUBJECT + '/'
SUMMARY_FOLDER = 'result/' + SUBJECT + '/' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + '/' + str(THRESHOLD_SCORE) + '/'
JSD_FOLDER = 'result/'
ENEXAM_FILE_NAME = EXAM_NAME + '.txt'
JSD_FILE_NAME = SUBJECT + '_jsd_exam.csv'

StopWords = GetDocuments.GetStopWords('stopwords.txt')

# MatchPNList = []
# SelectedParaSenList = []
# totalSelectedSenNum = 0
# for c in ExamChapters[SUBJECT][EXAM - 1]:
#     SUMMARY_FILE_NAME = 'Summary_' + c + '.csv'
#     with open (SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
#         reader = csv.DictReader(inFile)
#         for row in reader:
#             if row['pid'] != '':
#                 npid, pid = int(row['npid']), int(row['pid'])
#                 pidlist = [match[0] for match in MatchPNList]
#                 if pid not in pidlist:
#                     MatchPNList.append([pid, [npid]])
#                     SelectedParaSenList.append(row['sentence'].lower().replace('[\'', '').replace('\']', '').replace('[]', '').split('\', \''))
#                     totalSelectedSenNum += len(SelectedParaSenList[-1])
#                 else:
#                     MatchPNList[pidlist.index(pid)][1].append(npid)
# avgSelectedSenNum = totalSelectedSenNum / len(SelectedParaSenList)    
# MatchPNList, SelectedParaSenList = zip(*sorted(zip(MatchPNList, SelectedParaSenList)))

# find ExamCorpus and SummaryCorpus
ExamCorpus = GetDocuments.GetExamText(EXAM_FOLDER + ENEXAM_FILE_NAME)
# SummaryCorpus = []
# for m in range(len(MatchPNList)):
#     SummaryCorpus += SelectedParaSenList[m]

# # jsd for entire summary and exam content
# EntireDocumentJSD_ES = jsd.JSDivergence(ExamCorpus, SummaryCorpus)

# # write file
# needTitle = True
# title = ['Subject', 'Exam', 'JS(E,S)']
# if os.path.isfile(JSD_FOLDER + JSD_FILE_NAME): needTitle = False
# with open (JSD_FOLDER + JSD_FILE_NAME, 'a', newline='', encoding = 'utf-8') as outFile: # append
#     writer = csv.writer(outFile, delimiter = ',')
#     if needTitle:
#         writer.writerow(title)
#     writer.writerow([SUBJECT, EXAM_NAME, EntireDocumentJSD_ES])


''' other summarizers '''
SUMMARY_FOLDER = 'result/' + SUBJECT + '/others/'
JSD_FILE_NAME = SUBJECT + '_jsd_others_exam.csv'
# Summarizers = ['Random', 'Luhn', 'TextRank', 'LexRank', 'LSA', 'SumBasic']
Summarizers = ['SumBasic']
ESJSDList = []
for c in ExamChapters[SUBJECT][EXAM - 1]:
    for i in range(len(Summarizers)):
        SUMMARY_FILE_NAME = 'Summary_' + Summarizers[i] + '_' + c + '.txt'
        try:
            with open(SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'r', encoding = 'utf-8') as inFile:
                SelectedSenList = inFile.readlines()
            totalSelectedSenNum = len(SelectedSenList)
            # jsd for entire summary and note
            SummaryCorpus = SelectedSenList
            ESJSDList.append(jsd.JSDivergence(ExamCorpus, SummaryCorpus))
        except:
            ESJSDList.append(None)

# write file
needTitle = True
title = ['Subject', 'Exam', 'Summarizer', 'JS(E,S)']
if os.path.isfile(JSD_FOLDER + JSD_FILE_NAME): needTitle = False
with open (JSD_FOLDER + JSD_FILE_NAME, 'a', newline='', encoding = 'utf-8') as outFile: # append
    writer = csv.writer(outFile, delimiter = ',')
    if needTitle:
        writer.writerow(title)
    for i in range(len(Summarizers)):
        writer.writerow([SUBJECT, EXAM_NAME, Summarizers[i], ESJSDList[i]])
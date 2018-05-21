# -*- coding: UTF-8 -*-
''' select sentences from book '''
# 摘要內容可能有重複段落唷
import csv
import os
import sys
from decimal import Decimal
import GetDocuments
import CalSenScore

THRESHOLD_SCORE = 0.5 # avg = 0.3572
alpha = 0.1
beta = 0.4
gamma = 0.5
SUBJECT = 'DS'
CHAPTER = 'ch7'
THRESHOLD_COSSIM = 0.1

# SUBJECT = sys.argv[1]
# CHAPTER = sys.argv[2]
# # alpha = abs(round(float(sys.argv[3]), 1)) / 10 # used to decide parameters
# # beta = abs(round(float(sys.argv[4]), 1)) / 10
# alpha = abs(round(float(sys.argv[3]), 1))
# beta = abs(round(float(sys.argv[4]), 1))
# if alpha + beta > 1: sys.exit()
# gamma = abs(round(1 - alpha - beta, 1))
# THRESHOLD_COSSIM = float(sys.argv[5])
# THRESHOLD_SCORE = abs(round(float(sys.argv[6]), 2))
print (SUBJECT, CHAPTER, alpha, beta, gamma, THRESHOLD_COSSIM, THRESHOLD_SCORE)

BOOK_FOLDER = 'book/' + SUBJECT + '/'
# SUMMARY_FOLDER = 'result/' + SUBJECT + '/' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + '/'
SUMMARY_FOLDER = 'result/' + SUBJECT + '/' + str(alpha) + ',' + str(beta) + ',' + str(gamma) + '/' + str(THRESHOLD_SCORE) + '/'
TOPIC_FOLDER = 'topic/' + SUBJECT + '/'
TOPIC_FILE_NAME = 'Topics_' + CHAPTER + '.csv'
MATCH_FOLDER = 'match/' + SUBJECT + '_' + str(THRESHOLD_COSSIM) + '/'
BOOKPARA_FILE_NAME = CHAPTER + '_TSF.txt'
SUMMARY_FILE_NAME = 'Summary_' + CHAPTER + '.csv'
NSBMATCH_FILE_NAME = 'NSBMatch_' + CHAPTER + '.csv'

# if os.path.isdir(SUMMARY_FOLDER):
#   if os.path.isfile(SUMMARY_FOLDER + SUMMARY_FILE_NAME): sys.exit()

if not os.path.isdir(SUMMARY_FOLDER):
    os.makedirs(SUMMARY_FOLDER)

Topics = GetDocuments.GetTopics(TOPIC_FOLDER + TOPIC_FILE_NAME)

MatchedNPList = []
MatchedpidList = []
with open (MATCH_FOLDER + NSBMATCH_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        if row['pid'] != '':
            MatchedNPList.append({'npid': int(row['npid']), 'pid':int(row['pid'])})
            if int(row['pid']) not in MatchedpidList:
                MatchedpidList.append(int(row['pid']))

BookParaList = GetDocuments.GetBookParaText(BOOK_FOLDER + BOOKPARA_FILE_NAME)

sum_NTWNum = 0
max_NTWNum = 0
min_NTWNum = 100
TOTAL_SEN = 0
for p in BookParaList:
    for s in p:
        NTWNum = CalSenScore.NonTopicWordNum(s, Topics)
        if max_NTWNum < NTWNum: max_NTWNum = NTWNum
        if min_NTWNum > NTWNum: min_NTWNum = NTWNum
        sum_NTWNum += NTWNum
        TOTAL_SEN += 1
avg_NTWNum = sum_NTWNum / TOTAL_SEN # 5.8898
print ('avg_NTWNum:', avg_NTWNum)

sum_score = 0
FinalSenList = []
SelectedParaSenList = []
for match in MatchedNPList:
    npid, pid = match['npid'], match['pid']
    SelectedParaSenList.append({'npid': npid, 'pid': pid, 'sentence': []})
    for s in BookParaList[pid]:
        if CalSenScore.CalSenScore(s, alpha, beta, gamma, avg_NTWNum, max_NTWNum, min_NTWNum, Topics) > THRESHOLD_SCORE:
            SelectedParaSenList[-1]['sentence'].append(s)
            FinalSenList.append(s)

if not os.path.isdir('result'):
    os.makedirs('result')
if not os.path.isdir(SUMMARY_FOLDER):
    os.makedirs(SUMMARY_FOLDER)
with open (SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as outFile:
    writer = csv.DictWriter(outFile, fieldnames = ['npid', 'pid', 'sentence'])
    writer.writeheader()
    for para in SelectedParaSenList:
        writer.writerow(para)

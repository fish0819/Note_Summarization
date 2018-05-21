# -*- coding: UTF-8 -*-
import csv
import sys
import GetDocuments
import JSDivergence as jsd
import numpy as np
import os

SUBJECT = 'OM'
CHAPTER = 'supplementA'

SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
THRESHOLD_COSSIM = float(sys.argv[3])
print (SUBJECT, CHAPTER, THRESHOLD_COSSIM)

BOOK_FOLDER = 'book/' + SUBJECT + '/'
SLIDE_FOLDER = 'ppt/' + SUBJECT + '/'
NOTE_FOLDER = 'note/' + SUBJECT + '/' + CHAPTER + '/'
RESULT_FOLDER = 'result/'
TOPIC_FOLDER = 'topic/' + SUBJECT + '/'
MATCH_FOLDER = 'match/' + SUBJECT + '_' + str(THRESHOLD_COSSIM) + '/'
TOPIC_FILE_NAME = 'Topics_' + CHAPTER + '.csv'
COMBINEDSLIDE_FILE_NAME = CHAPTER + '_slides.csv'
BOOKPARA_FILE_NAME = CHAPTER + '_TSF.txt'
MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '.csv'
NSBMATCH_FILE_NAME = 'NSBMatch_' + CHAPTER + '.csv'
BSMATCH_FILE_NAME = 'BSMatch_' + CHAPTER + '.csv'
BSCOMPARE_FILE_NAME = 'BSCompare_' + SUBJECT + '.csv'
# NSBMATCH_FILE_NAME = 'NSBMatch_nowiki' + CHAPTER + '.csv'
# BSMATCH_FILE_NAME = 'BSMatch_nowiki' + CHAPTER + '.csv'
# MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '_nowiki.csv'
# BSCOMPARE_FILE_NAME = 'BSCompare_' + SUBJECT + '_nowiki.csv'

Topics = GetDocuments.GetTopics(TOPIC_FOLDER + TOPIC_FILE_NAME)
SlideTextList = GetDocuments.GetSlideText(SLIDE_FOLDER + COMBINEDSLIDE_FILE_NAME)
BookParaList = GetDocuments.GetBookParaText(BOOK_FOLDER + BOOKPARA_FILE_NAME)
NoteParaList = GetDocuments.GetNoteParaText(NOTE_FOLDER + MIXEDNOTEPARA_FILE_NAME)

BMatchSList = []
with open (MATCH_FOLDER + BSMATCH_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
	reader = csv.DictReader(inFile)
	for row in reader:
		if row['pid'] == '': pid = None
		else: pid = int(row['pid'])
		BMatchSList.append(pid)

MatchNPList = []
MatchJSDList = []
matchSBCount = 0
matchCount = 0
with open (MATCH_FOLDER + NSBMATCH_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
	reader = csv.DictReader(inFile)
	for row in reader:
		NPCorpus = NoteParaList[int(row['npid'])]
		SLCorpus = BPCorpus = []
		if row['sid'] == '': sid = None
		else:
			sid = int(row['sid'])
			SLCorpus = SlideTextList[int(row['sid'])]
		if row['pid'] == '': pid = None
		else:
			pid = int(row['pid'])
			BPCorpus = BookParaList[int(row['pid'])]
		MatchNPList.append({'sid': sid, 'pid': pid})
		if len(BPCorpus) > 0 and len(SLCorpus) > 0:
			# MatchJSDList.append(jsd.JSDivergence(SLCorpus, BPCorpus)) # jsd of a slide and book para pair
			matchCount += 1
			if MatchNPList[-1]['pid'] == BMatchSList[MatchNPList[-1]['sid']]: matchSBCount += 1

needTitle = True
if os.path.isfile(RESULT_FOLDER + BSCOMPARE_FILE_NAME): needTitle = False
with open (RESULT_FOLDER + BSCOMPARE_FILE_NAME, 'a', newline = '', encoding = 'utf-8') as outFile:
	writer = csv.writer(outFile, delimiter = ',')
	if needTitle: writer.writerow(['Subject', 'Chapter', 'THRESHOLD_COSSIM', 'MatchSBCount', 'MatchNCount', 'TotalNotePara', 'SBMatchRatio', 'NoteMatchRatio'])
	# if len(MatchJSDList) == 0: avgJSD = None
	# else: avgJSD = np.average(MatchJSDList)
	if matchCount == 0: writer.writerow([SUBJECT, CHAPTER, THRESHOLD_COSSIM, matchSBCount, matchCount, len(MatchNPList), None, (matchCount / len(MatchNPList))])
	else: writer.writerow([SUBJECT, CHAPTER, THRESHOLD_COSSIM, matchSBCount, matchCount, len(MatchNPList), (matchSBCount / matchCount), (matchCount / len(MatchNPList))])

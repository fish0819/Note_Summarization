# -*- coding: UTF-8 -*-
''' combine sentences in different notes into paragraphs '''
from os import listdir
import os
import csv
from pptx import Presentation
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np # average, standard deviation, max
import sys
import GetDocuments

SUBJECT = 'DS'
CHAPTER = 'ch7'
THRESHOLD_COSSIM = 0.1

# SUBJECT = sys.argv[1]
# CHAPTER = sys.argv[2]
# THRESHOLD_COSSIM = float(sys.argv[3])
print (SUBJECT, CHAPTER, THRESHOLD_COSSIM)

NOTE_FOLDER = 'note/' + SUBJECT + '/' + CHAPTER + '/'
SLIDE_FOLDER = 'ppt/' + SUBJECT + '/'
TOPIC_FOLDER = 'topic/' + SUBJECT + '/'
COMBINEDSLIDE_FILE_NAME = CHAPTER + '_slides.csv'
TOPIC_FILE_NAME = 'Topics_' + CHAPTER + '.csv'
MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '.csv'
# MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '_nowiki.csv'

Topics = []
with open (TOPIC_FOLDER + TOPIC_FILE_NAME, 'r', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})

with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]

RawNoteWordsList = []
PunctuationMarks = ['.', '!', '?', ':', ';', '\'', '\"', ',', '，', '。', '！', '？', '：', '；', '「', '」', '『', '』', '※']
SpecialMarks = ['+', '-', '*', '/', '=', '\\', '<', '>', '~', '@', '#', '(', ')', '[', ']', '{', '}', '|', '^', '–', '—']

# get ppt slides
Slides = GetDocuments.GetSlides(SLIDE_FOLDER + COMBINEDSLIDE_FILE_NAME)

# get note sentences
NoteFileNames = [(NOTE_FOLDER + f) for f in listdir(NOTE_FOLDER) if '_en.txt' in f]
# NoteFileNames = [(NOTE_FOLDER + f) for f in listdir(NOTE_FOLDER) if '_en_nowiki.txt' in f]
print (NoteFileNames)
Notes = []
for FILE_NAME in NoteFileNames:
	with open(FILE_NAME, 'r', encoding = 'utf-8') as inFile:
		Note = [line.replace('\n', '') for line in inFile.readlines()]
		for nsid in range(len(Note)):
			Note[nsid] = {'topic': [], 'content': Note[nsid]}
			for term in Topics:
				if term['term_e'] in Note[nsid]['content'] or (term['abbr'] != '' and (' ' + term['abbr'] + ' ' in Note[nsid]['content'] or '(' + term['abbr'] + ')' in Note[nsid]['content'])):
					Note[nsid]['topic'].append(term['term_e'])
	Notes.append(Note)

Corpus = [] # ppt slides + note sentences
DocumentLenList = []
for S in Slides:
	Corpus.append(S['content'])
DocumentLenList.append(len(Slides))
for N in Notes:
	DocumentLenList.append(len(N))
	for NS in N:
		Corpus.append(NS['content'])
tfidf_vectorizer = TfidfVectorizer()
TFIDFs = tfidf_vectorizer.fit_transform(Corpus).toarray()

''' match note sentences to ppt slides '''
# calculate all cossim of note sentences with slides
NSenCossimList = []
CosSMatchNSList = []
start = DocumentLenList[0]
for nid in range(len(Notes)):
	NSenCossimList.append([])
	CosSMatchNSList.append([])
	for nsid in range(DocumentLenList[nid + 1]):
		NSenCossimList[nid].append([])
		i = start + nsid
		for j in range(DocumentLenList[0]):
			NSenCossimList[nid][nsid].append(cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0])
		tmpCossimList = np.array(NSenCossimList[nid][nsid])
		sid = np.argmax(tmpCossimList)
		CosSMatchNSList[nid].append((sid, NSenCossimList[nid][nsid][sid]))
		# print (nid, nsid, sid, NSenCossimList[nid][nsid][sid])
	start += DocumentLenList[nid + 1]

# check if the note sentence has the same topic with a slide
NSenTopicList = []
TopicSMatchNSList = []
for nid in range(len(Notes)):
	NSenTopicList.append([])
	TopicSMatchNSList.append([])
	for nsid in range(DocumentLenList[nid + 1]):
		NSenTopicList[nid].append([])
		for sid in range(DocumentLenList[0]):
			NSenTopicList[nid][nsid].append([])
		for term in Topics:
			if term['term_e'] in Notes[nid][nsid]['topic']:
				for sid in range(DocumentLenList[0]):
					if term['term_e'] in Slides[sid]['topic']: NSenTopicList[nid][nsid][sid].append(term['term_e'])

''' combine sentences in a note into paragraphs '''
CombinedNotes = []
for nid in range(len(Notes)):
	CombinedNotes.append([])
	for nsid in range(DocumentLenList[nid + 1]):
		# if there is not a slide which is really similar to the sentence, then discard it
		if CosSMatchNSList[nid][nsid][1] > THRESHOLD_COSSIM:
			# if the slide which this sentence match to is the same as the previous sentence do, then combined them
			if nsid > 0 and CosSMatchNSList[nid][nsid][0] == CosSMatchNSList[nid][nsid - 1][0] and len(CombinedNotes[nid]) > 0:
				CombinedNotes[nid][-1]['topic'] = list(set(CombinedNotes[nid][-1]['topic'] + Notes[nid][nsid]['topic']))
				CombinedNotes[nid][-1]['nsid_list'].append(nsid)
			else:
				CombinedNotes[nid].append({'topic': Notes[nid][nsid]['topic'], 'nsid_list': [nsid], 'sid': CosSMatchNSList[nid][nsid][0]})

MixedNoteParaList = []
for nid in range(len(Notes)):
	for para in CombinedNotes[nid]:
		if len(MixedNoteParaList) == 0 or not any(np['sid'] == para['sid'] for np in MixedNoteParaList):
			MixedNoteParaList.append({'content': '', 'topic': para['topic'], 'sid': para['sid']})
			for nsid in para['nsid_list']:
				MixedNoteParaList[-1]['content'] += Notes[nid][nsid]['content'] + '\n'
		else:
			tmpsidList = [np['sid'] for np in MixedNoteParaList]
			npid = tmpsidList.index(para['sid'])
			for nsid in para['nsid_list']:
				MixedNoteParaList[npid]['content'] += Notes[nid][nsid]['content'] + '\n'
				MixedNoteParaList[npid]['topic'] = list(set(MixedNoteParaList[npid]['topic'] + para['topic']))
with open (NOTE_FOLDER + MIXEDNOTEPARA_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as outFile:
	writer = csv.DictWriter(outFile, fieldnames = ['content', 'topic', 'sid'])
	writer.writeheader()
	for np in MixedNoteParaList:
		writer.writerow(np)
# -*- coding: UTF-8 -*-
''' match paragraphs '''
from os import listdir
import os
from docx import *
import csv
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np # average, standard deviation, max
from numpy import linalg # l2 norm
import sys
import GetDocuments

SUBJECT = 'DS'
CHAPTER = 'ch7'
THRESHOLD_COSSIM = 0.1
SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
THRESHOLD_COSSIM = float(sys.argv[3])
print (SUBJECT, CHAPTER, THRESHOLD_COSSIM)

NOTE_FOLDER = 'note/' + SUBJECT + '/' + CHAPTER + '/'
BOOK_FOLDER = 'book/' + SUBJECT + '/'
SLIDE_FOLDER = 'ppt/' + SUBJECT + '/'
MATCH_FOLDER = 'match/' + SUBJECT + '_' + str(THRESHOLD_COSSIM) + '/'
TOPIC_FOLDER = 'topic/' + SUBJECT + '/'
BOOK_FILE_NAME = CHAPTER + '.txt'
NTERM_FILE_NAME = 'NTerms_' + CHAPTER + '.csv'
BTERM_FILE_NAME = 'BTerms.csv'
TOPIC_FILE_NAME = 'Topics_' + CHAPTER + '.csv'
COMBINEDSLIDE_FILE_NAME = CHAPTER + '_slides.csv'
MIXEDNOTEPARA_FILE_NAME = 'MixedNote_' + CHAPTER + '_' + str(THRESHOLD_COSSIM) + '.csv'
NSBMATCH_FILE_NAME = 'NSBMatch_' + CHAPTER + '.csv'
BSMATCH_FILE_NAME = 'BSMatch_' + CHAPTER + '.csv'
BOOKPARA_FILE_NAME = CHAPTER + '_TSF.txt'

Topics = GetDocuments.GetTopics(TOPIC_FOLDER + TOPIC_FILE_NAME)
StopWords = GetDocuments.GetStopWords('stopwords.txt')
RawNoteWordsList = []
PunctuationMarks = ['.', '!', '?', ':', ';', '\'', '\"', ',', '，', '。', '！', '？', '：', '；', '「', '」', '『', '』', '※']
SpecialMarks = ['+', '-', '*', '/', '=', '\\', '<', '>', '~', '@', '#', '(', ')', '[', ']', '{', '}', '|', '^', '–', '—']

''' get ppt, book and note contentes '''
Slides = GetDocuments.GetSlides(SLIDE_FOLDER + COMBINEDSLIDE_FILE_NAME)
ParagraphList = GetDocuments.GetBookPara(BOOK_FOLDER + BOOKPARA_FILE_NAME, Topics)
MixedNoteParaList = GetDocuments.GetNotePara(NOTE_FOLDER + MIXEDNOTEPARA_FILE_NAME)

Corpus = [] # ppt slides + book paragraphs + note paragraphs
for S in Slides:
	Corpus.append(S['content'])
for P in ParagraphList:
	Corpus.append(P['content'])
for NP in MixedNoteParaList:
	Corpus.append(NP['content'])
tfidf_vectorizer = TfidfVectorizer()
TFIDFs = tfidf_vectorizer.fit_transform(Corpus).toarray()


''' match note paragraphs to ppt slides and book paragrpahs '''
# calculate all cossim of note paragraphs with slides and book paragraphs
NParaCossimList = []
CosMatchNPList = []
# CosSMatchNPList = []
# CosPMatchNPList = []
for npid in range(len(MixedNoteParaList)):
	NParaCossimList.append({'SCossim': [], 'PCossim': []})
	i = len(Slides) + len(ParagraphList) + npid
	for j in range(len(Slides) + len(ParagraphList)):
		if j < len(Slides):
			# NParaCossimList[npid]['SCossim'].append(cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0])
			pass
		else:
			NParaCossimList[npid]['PCossim'].append(cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0])
	# sid = np.argmax(np.array(NParaCossimList[npid]['SCossim']))
	# if NParaCossimList[npid]['SCossim'][sid] < THRESHOLD_COSSIM: sid = None
	sid = MixedNoteParaList[npid]['sid']
	pid = np.argmax(NParaCossimList[npid]['PCossim'])
	if NParaCossimList[npid]['PCossim'][pid] < THRESHOLD_COSSIM: pid = None
	CosMatchNPList.append({'npid': npid, 'sid': sid, 'pid': pid})
	if sid == None: CosMatchNPList[-1]['cossim_nps'] = None
	# else: CosMatchNPList[-1]['cossim_nps'] = NParaCossimList[npid]['SCossim'][sid]
	else: CosMatchNPList[-1]['cossim_nps'] = cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0]
	if pid == None: CosMatchNPList[-1]['cossim_npb'] = None
	else: CosMatchNPList[-1]['cossim_npb'] = NParaCossimList[npid]['PCossim'][pid]

# check if the note sentence has the same topic with a slide or a book paragraph
NParaTopicList = []
TopicSMatchNPList = []
TopicPMatchNPList = []
for npid in range(len(MixedNoteParaList)):
	NParaTopicList.append({'STopics': [], 'PTopics': []})
	for sid in range(len(Slides)):
		NParaTopicList[npid]['STopics'].append([])
	for pid in range(len(ParagraphList)):
		NParaTopicList[npid]['PTopics'].append([])
	for term in Topics:
		if term['term_e'] in MixedNoteParaList[npid]['topic']:
			for sid in range(len(Slides)):
				if term['term_e'] in Slides[sid]['topic']: NParaTopicList[npid]['STopics'][sid].append(term['term_e'])
			for pid in range(len(ParagraphList)):
				if term['term_e'] in ParagraphList[pid]['topic']: NParaTopicList[npid]['PTopics'][pid].append(term['term_e'])


''' match ppt slides to book paragraphs '''
# calculate all cossim betweeen slides and book paragraphs
SlideCossimList = []
CosPMatchSlideList = []
for i in range(len(Slides)):
	SlideCossimList.append([])
	for pid in range(len(ParagraphList)):
		j = pid + len(Slides)
		SlideCossimList[i].append(cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0])
	tmpCossimList = np.array(SlideCossimList[i])
	pid = np.argmax(tmpCossimList)
	if SlideCossimList[i][pid] < THRESHOLD_COSSIM: CosPMatchSlideList.append((None, None))
	else: CosPMatchSlideList.append((pid, SlideCossimList[i][pid]))


# check if the slide has the same topic with a book paragraph
SlideTopicList = []
TopicPMatchSlideList = []
for sid in range(len(Slides)):
	SlideTopicList.append([])
	TopicPMatchSlideList.append([])
	for pid in range(len(ParagraphList)):
		SlideTopicList[sid].append([])
	for term in Topics:
		if term['term_e'] in Slides[sid]['topic']:
			for pid in range(len(ParagraphList)):
				if term['term_e'] in ParagraphList[pid]['topic']: SlideTopicList[sid][pid].append(term['term_e'])


''' write files '''
if not os.path.isdir('match/'):
	os.makedirs('match/')
if not os.path.isdir(MATCH_FOLDER):
	os.makedirs(MATCH_FOLDER)

with open (MATCH_FOLDER + NSBMATCH_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as outFile:
	writer = csv.DictWriter(outFile, fieldnames = ['npid', 'sid', 'cossim_nps', 'pid', 'cossim_npb'])
	writer.writeheader()
	for match in CosMatchNPList:
		writer.writerow(match)

with open (MATCH_FOLDER + BSMATCH_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as outFile:
	writer = csv.writer(outFile, delimiter = ',')
	writer.writerow(['sid', 'pid', 'cossim'])
	for sid in range(len(Slides)):
		writer.writerow([sid, CosPMatchSlideList[sid][0], CosPMatchSlideList[sid][1]])

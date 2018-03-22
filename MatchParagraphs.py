# -*- coding: UTF-8 -*-
''' match paragraphs '''
from os import listdir
from os.path import isfile
from docx import *
import csv
from googletrans import Translator
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk

# nltk.download('averaged_perceptron_tagger')

''' combine notes '''
NOTE_FOLDER = 'note\\'
NoteFileNames = [(NOTE_FOLDER + f) for f in listdir(NOTE_FOLDER) if '.docx' in f]
# print (NoteFileNames)

Notes = []
for FILE_NAME in NoteFileNames:
	note = ''
	d = Document(FILE_NAME)
	for p in d.paragraphs:
		text = p.text.strip()
		if len(text) > 0:
			note += text + '\n'
	Notes.append(note)

Topics = []
with open ('Topics.csv', 'r', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})

# translate into english and remove stop words
with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]
translator = Translator()
RawNoteWordsList = []
PunctuationMarks = ['.', '!', '?']
for nid in range(len(Notes)):
	note = Notes[nid]
	WordsList = []
	for term in Topics:
		if len(term['term_c']) > 0: note = note.replace(term['term_c'], ' ' + term['term_e'] + ' ')
	note = note.splitlines()
	for lid in range(len(note)):
		rawLine = note[lid]
		line = ''
		prev = '' # 'c', 'e', 'd' or 'o' (other)
		curr = ''
		if re.search('(\d)+\.\D', rawLine):
			rawLine = rawLine[:]
		for i in range(len(rawLine)):
			if rawLine[i] >= u'\u4e00' and rawLine[i] <= u'\u9fff': curr = 'c'
			elif (rawLine[i] >= u'\u0041' and rawLine[i] <= u'\u005a') or (rawLine[i] >= u'\u0061' and rawLine[i] <= u'\u007a'): curr = 'e'
			elif rawLine[i] >= u'\u0030' and rawLine[i] <= u'\u0039': curr = 'd'
			else: curr = 'o'
			if i == 0:
				prev = curr
				line = rawLine[i]
				continue
			if rawLine[i] == '?': print (rawLine[i-1], prev + '\t' + rawLine[i], curr )
			if curr != prev and (prev != 'd' and curr != 'd') and (rawLine[i] != '-' and rawLine[i - 1] != '-'):
				line += ' '
				prev = curr
			line += rawLine[i]
		line = ' '.join([translator.translate(w).text.lower() for w in line.split()]).replace(' 、 ', ', ').replace(' ， ', ', ')
		for sw in StopWords:
			line = line.replace(' ' + sw + ' ', ' ')
			if re.match(sw + ' ', line): line = line[len(sw):].strip() # remove stopwords at the start of sentences
		for pm in PunctuationMarks: line = line.replace(pm, '')
		note[lid] = line
		Words = line.split()
		for w in Words:
			if re.search('\d\.$', w): Words.remove(w)
		WordsList.append(Words)
	Notes[nid] = note
	RawNoteWordsList.append(WordsList)

# combine sentences in notes
Corpus = []
for note in Notes: Corpus += note

tfidf_vectorizer = TfidfVectorizer()
TFIDFs = tfidf_vectorizer.fit_transform(Corpus).toarray()
NWordsList = RawNoteWordsList[0][:] # list of (union of words -> representaion of sentence)
start = 0 # the start index of the note in union
ComparedTFIDFs = TFIDFs[:len(Notes[0])]
print (len(ComparedTFIDFs), len(NWordsList))
threshold_cossim = 0.1
len_NWordsList = len(Notes[0])
NoteSenMatch = []
IsNoteSenMatched = []
for nid in range(len(Notes)):
	IsNoteSenMatched.append([])
	for sid in range(len(Notes[nid])):
		IsNoteSenMatched[nid].append(False)
		if nid == 0:
			NoteSenMatch.append([])
			NoteSenMatch[sid].append(sid)
for sid in range(len(NoteSenMatch)):
	for nid in range(1, len(Notes)): NoteSenMatch[sid].append(None)
# to match sentences (the sentences which are not matched will be insert to the list latter)
start = len(Notes[0])
for nid in range(1, len(Notes)):
	prevMatchedj = -1
	WordsList = RawNoteWordsList[nid]
	for i in range(start, start + len(Notes[nid])):
		for j in range(prevMatchedj + 1, len(Notes[0])):
			cos_sim = cosine_similarity(TFIDFs[i].reshape(1, -1), ComparedTFIDFs[j].reshape(1, -1))[0][0]
			if cos_sim >= threshold_cossim:
				IsNoteSenMatched[nid][i - start] = True
				NoteSenMatch[j][nid] = i - start
				prevMatchedj = j # assume that if si matches sj, then si+1 will not match to sj or sj-1
				IsNoteSenMatched[0][j] = True
				# combine the two sentences
				for w in WordsList[i - start]:
					if w not in NWordsList[j]: NWordsList[j].append(w)
				break # as soon as we find si matched, then continue to si+1 (assume that every sentence was matched once)
	start += len(Notes[nid])
# update ComparedTFIDFs
for msid in range(len(NoteSenMatch)):
	data = []
	for nid in range(len(Notes)):
		if nid == 0: start = 0
		if NoteSenMatch[msid][nid] != None:
			data.append(TFIDFs[msid + start][:])
			start += len(Notes[nid])
	ComparedTFIDFs[msid] = np.average(np.array(data), axis = 0)
# insert the sentences which were not matched
start = len(Notes[0])
for nid in range(1, len(Notes)):
	prevMatchedj = -1
	WordsList = RawNoteWordsList[nid][:]
	for sid in range(len(Notes[nid])):
		found = False
		if IsNoteSenMatched[nid][sid] == True: # find the next sentence to be matched
			for msid in range(len(NoteSenMatch)):
				if NoteSenMatch[msid][nid] == sid:
					found = True
					prevMatchedj = msid
			if found == False: print ('nid:', nid, 'sid:', sid)
			continue
		i = start + sid
		j = prevMatchedj + 1
		len_Compared = len(ComparedTFIDFs)
		while j < len_Compared:
			if NoteSenMatch[j][nid] == None:
				cos_sim = cosine_similarity(TFIDFs[i].reshape(1, -1), ComparedTFIDFs[j].reshape(1, -1))[0][0]
				if cos_sim >= threshold_cossim:
					IsNoteSenMatched[nid][sid] = True
					NoteSenMatch[j][nid] = sid
					prevMatchedj = j
					for w in WordsList[i - start]:
						if w not in NWordsList[j]: NWordsList.append(w)
					break
			if j == len(NWordsList) - 1 and cos_sim < threshold_cossim:
				NWordsList.insert(prevMatchedj + 1, WordsList[sid]) # insert to the prevMatchedj+1
				IsNoteSenMatched[nid][sid] = True
				NoteSenMatch.insert(prevMatchedj + 1, [])
				for n in Notes: NoteSenMatch[prevMatchedj + 1].append(None)
				NoteSenMatch[prevMatchedj + 1][nid] = sid
				ComparedTFIDFs = np.concatenate((ComparedTFIDFs[:prevMatchedj + 1], [TFIDFs[i]], ComparedTFIDFs[prevMatchedj + 1:]), axis = 0)
				prevMatchedj += 1
				break
			j += 1
			len_Compared = len(ComparedTFIDFs)
	start += len(Notes[nid])
NWordSeqlList = []
for nws in NWordsList:
	NWordSeqlList.append(' '.join(nws))
for match in NoteSenMatch:
	for nid in range(len(match)):
		if match[nid] != None: print (Notes[nid][match[nid]])
	print('\n')


''' segment the book contentes '''
# TSF
import nltk.data # split text on sentences
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy # average and standard deviation
from numpy import linalg # l2 norm
import math # check inf

def CosineSim (List_x, List_y):
	dotProduct = numpy.dot(List_x, List_y)
	norm_x = linalg.norm(List_x)
	norm_y = linalg.norm(List_y)
	if norm_x * norm_y > 0:
		return (numpy.dot(List_x, List_y) / (linalg.norm(List_x) * linalg.norm(List_y)))
	else: return 0

''' get content '''
with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]
Topics = []
with open ('Topics.csv', 'r', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})
with open ('book\\Supplement-A.txt', 'r', encoding = 'UTF-8') as inFile:
	RawParagraphList = inFile.readlines()
RawParagraphList = [s.replace('\n', '').strip().lower() for s in RawParagraphList]
#nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
RawSentenceList = [] # corpus
for para in RawParagraphList:
	RawSentenceList += senTokenizer.tokenize(para)
	for sid in range(len(RawSentenceList)):
		if re.match('(\d)+$', RawSentenceList[sid]): RawSentenceList[sid] = ''
	RawSentenceList = [s for s in RawSentenceList if (len(s) > 0)]
SentenceList = []
for s in RawSentenceList:
	for sw in StopWords:
		s = s.replace(' ' + sw + ' ', ' ').strip()
		if re.match(sw + ' ', s): s = s[len(sw):].strip() # remove stopwords at the start of sentences
	SentenceList.append(s)

''' TSF '''
# parameter setting
K = 10 # the number of sentences in a block

countVectorizer = CountVectorizer()
TFList = countVectorizer.fit_transform(SentenceList).toarray()
tfidfTransformer = TfidfTransformer()
TFIDFList = tfidfTransformer.fit_transform(TFList).toarray()
TermList = countVectorizer.get_feature_names()

InnerSimList = [] # [i, innerSim] for each element; i starts from 0
OuterSimList = [] # [i, outerSim] for each element
DissimList = [] # [i, dissimilarity] for each element

for i in range(K - 1, (len(TFList) - K + 1)):
	innerSim = 0
	outerSim = 0
	for a in range(i - K + 1, i + 1):
		for b in range(a + 1, i + 1):
			if a != b:
				innerSim = cosine_similarity(TFList[a].reshape(1, -1), TFList[b].reshape(1, -1))[0][0]
		for c in range(i + 1, i + K):
			outerSim += cosine_similarity(TFList[a].reshape(1, -1), TFList[c].reshape(1, -1))[0][0]
	if innerSim == 0:
		continue
	dissim = (innerSim - outerSim) / innerSim
	if math.isinf(dissim):
		print ('inner:', innerSim)
		print ('outer:', outerSim)
		continue
	InnerSimList.append([i, innerSim])
	OuterSimList.append([i, outerSim])
	DissimList.append({'i': i, 'dissim': dissim})

avg_dissim = numpy.mean([d['dissim'] for d in DissimList])
dev_dissim = numpy.std([d['dissim'] for d in DissimList])
# print ('Avg =', avg_dissim)
# print ('Dev =', dev_dissim)

THRESHOLD_DISSIM = avg_dissim + 0.4 * dev_dissim # the threshold of the dissimilarity

current_i = 0
ParagrahList = []
ParaSenList = []
for d in DissimList:
	if d['dissim'] > THRESHOLD_DISSIM:
		ParagrahList.append(' '.join(RawSentenceList[current_i:d['i'] + 1]))
		ParaSenList.append(RawSentenceList[current_i:d['i']])
		current_i = d['i'] + 1
ParagrahList.append(' '.join(RawSentenceList[current_i:]))
ParaSenList.append(RawSentenceList[current_i:])

for pid in range(len(ParagrahList)):
	ParagrahList[pid] = {'topic': [], 'content': ParagrahList[pid]}
	for term in Topics:
		if term['term_e'] in ParagrahList[pid]['content'] or (term['abbr'] != '' and term['abbr'] in ParagrahList[pid]['content']):
			ParagrahList[pid]['topic'].append(term['term_e'])


''' combine ppt slides '''
from pptx import Presentation
import re

Topics = []
with open ('Topics.csv', 'r', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})

FILE_NAME = 'ppt\\Supplement-A.pptx'
prs = Presentation(FILE_NAME)
slides = prs.slides
NoteList = []
Slides = []
text_runs = []
sid = 0
for slide in prs.slides:
	title = ''
	if slide.has_notes_slide:
		for shape in slide.notes_slide.shapes:
			if shape.text != '':
				NoteList.append(shape.text.lower())
	if slide.shapes.title:
		title = slide.shapes.title.text.lower()
	for shape in slide.shapes:
		content = ''
		if not shape.has_text_frame:
			continue
		for paragraph in shape.text_frame.paragraphs:
			text = ''
			for run in paragraph.runs:
				if len(run.text) > 0: text += run.text.lower()
			if len(text) > 0:
				content += text.replace('\n', ' ').replace('\t', ' ') + ' '
		content = re.sub(' +', ' ', content) # remove duplicate spaces
		if sid > 0 and title == Slides[sid - 1]['title']:
			Slides[sid - 1]['content'] = Slides[sid - 1]['content'] + ' ' + content.strip() # combine the slides which have a same title
		else:
			Slides.append({'title': title, 'content': content.strip()})
			sid += 1
for sid in range(len(Slides)):
	Slides[sid]['topic'] = []
	for term in Topics:
		if term['term_e'] in Slides[sid]['content'] or (term['abbr'] != '' and term['abbr'] in Slides[sid]['content']):
			Slides[sid]['topic'].append(term['term_e'])


''' match ppt slides and book paragraphs '''
import csv
# match by BTerms
BTerms = []
with open('book\\BTerms.csv', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		BTerms.append({'term': row['term'], 'abbr': row['abbr']})
IndexMatchDict = {}
for term in BTerms:
	IndexMatchDict[term['term']] = {'sid_list': [], 'pid_list': []}
	for sid in range(len(Slides)):
		if term['term'] in Slides[sid]['topic'] or (term['abbr'] != '' and term['abbr'] in Slides[sid]['topic']): IndexMatchDict[term['term']]['sid_list'].append(sid)
	for pid in range(len(ParagrahList)):
		if term['term'] in ParagrahList[pid]['topic'] or (term['abbr'] != '' and term['abbr'] in ParagrahList[pid]['topic']): IndexMatchDict[term['term']]['pid_list'].append(pid)
	if len(IndexMatchDict[term['term']]['sid_list']) == 0 and len(IndexMatchDict[term['term']]['pid_list']) == 0: IndexMatchDict.pop(term['term'], None)
SBIndexMatch = []
for sid in range(len(Slides)):
	SBIndexMatch.append([])
	for term in BTerms:
		if term['term'] in Slides[sid]['topic'] or (term['abbr'] != '' and term['abbr'] in Slides[sid]['topic']):
			for pid in IndexMatchDict[term['term']]['pid_list']:
				if pid not in SBIndexMatch[sid]: SBIndexMatch[sid].append(pid)

# match by cosine similarity
SBCossimMatch = []
Corpus = []
for s in Slides:
	Corpus.append(s['content'])
for p in ParagrahList:
	Corpus.append(p['content'])
tfidf_vectorizer = TfidfVectorizer()
TFIDFs = tfidf_vectorizer.fit_transform(Corpus).toarray()
THRESHOLD_COSSIM = 0.3 # avg = 0.066
sum_cossim = 0
count = 0
for i in range(len(Slides)):
	SBCossimMatch.append([])
	for j in range(len(Slides), len(Corpus)): # Corpus is composed of Slides and ParagraphList
		cos_sim = cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0]
		sum_cossim += cos_sim
		count += 1
		if cos_sim > THRESHOLD_COSSIM:
			SBCossimMatch[i].append(j - len(Slides))

SBMatch = []
for sid in range(len(Slides)):
	SBMatch.append([])
	for pid in range(len(ParagrahList)):
		if pid in SBIndexMatch[sid] and pid in SBCossimMatch[sid]:
			SBMatch[sid].append(pid)


''' match ppt slides and note paragraphs '''
# match by Topics
Topics = []
with open('Topics.csv', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		Topics.append({'term': row['term_e'], 'abbr': row['abbr']})
TopicMatchDict = {}
for term in Topics:
	TopicMatchDict[term['term']] = {'sid_list': [], 'msid_list': []}
	for sid in range(len(Slides)):
		if term['term'] in Slides[sid]['topic'] or (term['abbr'] != '' and term['abbr'] in Slides[sid]['topic']): TopicMatchDict[term['term']]['sid_list'].append(sid)
	for msid in range(len(NWordSeqlList)):
		if term['term'] in NWordSeqlList[msid] or (term['abbr'] != '' and term['abbr'] in NWordSeqlList[msid]): TopicMatchDict[term['term']]['msid_list'].append(msid)
	if len(TopicMatchDict[term['term']]['sid_list']) == 0 and len(TopicMatchDict[term['term']]['msid_list']) == 0: TopicMatchDict.pop(term['term'], None)
SNTopicMatch = []
for sid in range(len(Slides)):
	SNTopicMatch.append([])
	for term in Topics:
		if term['term'] in Slides[sid]['topic'] or (term['abbr'] != '' and term['abbr'] in Slides[sid]['topic']):
			for msid in TopicMatchDict[term['term']]['msid_list']:
				if msid not in SNTopicMatch[sid]: SNTopicMatch[sid].append(msid)

# match by cosine similarity
SNCossimMatch = []
Corpus = []
for nws in NWordSeqlList:
	Corpus.append(nws)
for s in Slides:
	Corpus.append(s['content'])
tfidf_vectorizer = TfidfVectorizer()
TFIDFs = tfidf_vectorizer.fit_transform(Corpus).toarray()
THRESHOLD_COSSIM = 0.03 # avg = 0.0239
sum_cossim = 0
count = 0
for i in range(len(Slides)):
	SNCossimMatch.append([])
	for j in range(len(Slides), len(Corpus)): # Corpus is composed of Slides and ParagraphList
		cos_sim = cosine_similarity(TFIDFs[i].reshape(1, -1), TFIDFs[j].reshape(1, -1))[0][0]
		sum_cossim += cos_sim
		count += 1
		if cos_sim > THRESHOLD_COSSIM:
			SNCossimMatch[i].append(j - len(Slides))
SNMatch = []
for sid in range(len(Slides)):
	SNMatch.append([])
	for msid in range(len(NWordSeqlList)):
		if msid in SNTopicMatch[sid] and msid in SNCossimMatch[sid]:
			SNMatch[sid].append(msid)
	SNMatch[sid].sort()
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile
from docx import *
import csv
from googletrans import Translator
import re
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

''' combine notes '''
NOTE_FOLDER = 'note\\'
NoteFileNames = [(NOTE_FOLDER + f) for f in listdir(NOTE_FOLDER) if '.docx' in f]
print (NoteFileNames)

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
		Topics.append({'c': row['c'], 'e': row['e']})

# translate into english
translator = Translator()
RawNNoteWordsList = []
for nid in range(len(Notes)):
	note = Notes[nid]
	WordsList = []
	for term in Topics:
		note = note.replace(term['c'], ' ' + term['e'] + ' ')
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
			if curr != prev:
				line += ' '
				prev = curr
			line += rawLine[i]
		line = ' '.join([translator.translate(w).text for w in line.split()]).replace(' 、 ', ', ').replace(' ， ', ', ')
		# print(line)
		note[lid] = line
		Words = line.split()
		for w in Words:
			if re.search('\d\.$', w): Words.remove(w)
		WordsList.append(Words)
	Notes[nid] = note
	RawNNoteWordsList.append(WordsList)
for n in RawNNoteWordsList:
	for wl in n: print (wl)

# combine sentences in notes
vectorizer = CountVectorizer()
Corpus = []
for note in Notes: Corpus += note
# TPs = vectorizer.fit_transform(Corpus).toarray() # 要先聯集所有筆記
# FeatureNames = vectorizer.get_feature_names()
# transformer = TfidfTransformer()
# TFIDFs = transformer.fit_transform(TPs).toarray()


# tfidf_vectorizer = TfidfVectorizer()
# TFIDFs = tfidf_vectorizer.fit_transform(Corpus).toarray()
# # print (TFIDFs)
# NWordsList = [] # list of (union of words -> representaion of sentence)
# start = 0 # the start index of the note in union
# ComparedTFIFDs = TFIDFs[:len(Notes[0])]
# threshold_cossim = 0.03
# for nid in range(len(Notes)):
# 	WordsList = RawNNoteWordsList[nid]
# 	if nid == 0:
# 		NWordsList = WordsList
# 		start = len(Notes[nid])
# 		continue
# 	for i in range(start, start + len(Notes[nid])):
# 		for j in range(len(Notes[0])):
# 			cos_sim = cosine_similarity(TFIDFs[i].reshape(1,-1), TFIDFs[j].reshape(1,-1))[0][0]
# 			if cos_sim >= threshold_cossim:
# 				for w in WordsList[i - start]:
# 					if w not in NWordsList[j]: NWordsList[j].append(w)
# 				break
# 			if j == len(NWordsList) - 1 and cos_sim < threshold_cossim:
# 				NWordsList.append(WordsList[i - start])
# 	start += len(Notes[nid])
# for Words in NWordsList:
# 	print (Words)
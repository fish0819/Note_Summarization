# -*- coding: UTF-8 -*-
import re
import nltk
# nltk.download('averaged_perceptron_tagger')

PunctuationMarks = [',', '!', '?', '“', '”', '–', '—', '…', '\'', '\"', '\\', '/', '(', ')', '<', '>', '[', ']', '{', '}']

with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]
StopWords += ['example', 'solved problem', 'figure', 'learning goals', 'chapter']

def ContainTopic (sen, Topics):
	for term in Topics:
		if term['term_e'] in sen or (term['abbr'] != '' and term['abbr'] in sen):
			return True
	return False

def NonTopicWordNum (sen, Topics):
	for p in PunctuationMarks:
		sen = sen.replace(p, '')
	for sw in StopWords:
		if re.match(sw + ' ', sen): sen = sen.replace(sw, '').strip()
		elif re.search(' ' + sw + ' ', sen): sen = sen.replace(' ' + sw + ' ', ' ')
	for term in Topics:
		if re.match(term['term_e'] + ' ', sen) or re.search(' ' + term['term_e'] + ' ', sen):
			sen = sen.replace(term['term_e'], '').strip()
		elif re.match(term['abbr'] + ' ', sen) or re.search(' ' + term['abbr'] + ' ', sen):
			sen = sen.replace(term['abbr'], '').strip()
	POSTag = nltk.pos_tag(nltk.word_tokenize(sen))
	for wid in range(len(POSTag)):
		if POSTag[wid][1] == 'CD': sen.replace(POSTag[wid][0], '')
	return (len(sen.split()))

def POSNum (sen):
	rawsen = sen
	for p in PunctuationMarks:
		sen = sen.replace(p, '')
	for sw in StopWords:
		if re.match(sw + ' ', sen): sen = sen.replace(sw, '').strip()
		elif re.search(' ' + sw + ' ', sen): sen = sen.replace(' ' + sw + ' ', ' ')
	text = nltk.word_tokenize(sen)
	ImportantTags = ['NN', 'VB', 'JJ', 'RB']
	NumList = [0, 0, 0, 0]
	for tag in nltk.pos_tag(text):
		for itid in range(len(ImportantTags)):
			if ImportantTags[itid] in tag[1]: NumList[itid] += 1
	return (NumList[0], NumList[1], NumList[2], NumList[3])

def CalSenScore (sen, alpha, beta, gamma, avg_n, max_n, min_n, Topics):
	NTWNum = NonTopicWordNum(sen, Topics)
	WN = 1 - abs(NTWNum - avg_n) / (max_n - min_n)
	POSNumTup = POSNum(sen)
	if NTWNum == 0: POSRatio = 0
	else: POSRatio = ((POSNumTup[0] + POSNumTup[1]) + (POSNumTup[2] + POSNumTup[3]) * 0.5) / avg_n
	return (alpha * ContainTopic(sen, Topics) + beta * WN + gamma * POSRatio)
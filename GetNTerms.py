# -*- coding: UTF-8 -*-
import os.path
from os import listdir
import csv
from docx import *
import jieba
import re # to check if a string contains chinese char
import requests
from bs4 import BeautifulSoup

class Paragraph:
	def __init__(self, content, KeyTerms):
		self.content = content
		self.KeyTerms = []

class Term:
	def __init__(self, cTerm, eTerm):
		self.cTerm = cTerm
		self.eTerm = eTerm

SUBJECT = 'OM'
CHAPTER = 'ch12'
NTERM_FOLDER = 'note/' + SUBJECT + '/'
NTERM_FILE_NAME = 'NTerms_' + CHAPTER + '.csv'
NOTE_FOLDER = 'note/' + SUBJECT + '/' + CHAPTER + '/'
NoteFileNames = [(NOTE_FOLDER + f) for f in listdir(NOTE_FOLDER) if '.docx' in f]

with open('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = inFile.readlines()

''' read docx '''
NTerms = []
for FILE_NAME in NoteFileNames:
	d = Document(FILE_NAME)
	NoteParagraphs = []
	pid = 0
	for p in d.paragraphs:
		if len(p.text) == 0:
			if len(NoteParagraphs) == pid + 1:
				pid += 1
			continue
		if pid == len(NoteParagraphs):
			NoteParagraphs.append(Paragraph(p.text, []))
		else:
			NoteParagraphs[pid].content += ' ' + p.text

	''' segmentation '''
	# checking paragraphs may need '\t'
	PunctuationList = ['\t', '\n', '，', '。', '！', '？', '：', '（', '）', '、', ',', '.', '!', '?', ':', '(', ')', '…', '+', '=', '*', '/', '<', '>']
	for pid in range(len(NoteParagraphs)):
		prev = '' # 'c' or 'e'
		Sequences = [] # [sequence, language]
		PTerms = []
		# split chinese and english sequences
		for i in range(len(NoteParagraphs[pid].content)):
			if NoteParagraphs[pid].content[i] in PunctuationList: # remove punctuation
				if len(Sequences) > 0:
					if len(Sequences[-1]) > 0: Sequences[-1][0] += ' '
				continue
			if (NoteParagraphs[pid].content[i] >= u'\u4e00' and NoteParagraphs[pid].content[i] <= u'\u9fff'): # determine if the char is chinese
				if prev != 'c':
					prev = 'c'
					Sequences.append([NoteParagraphs[pid].content[i], prev])
				else: Sequences[len(Sequences) - 1][0] += NoteParagraphs[pid].content[i]
			else:
				if prev != 'e':
					prev = 'e'
					Sequences.append([NoteParagraphs[pid].content[i], prev])
				else: Sequences[len(Sequences) - 1][0] += NoteParagraphs[pid].content[i]
		for sequence in Sequences:
			if sequence[1] == 'c': # for chinese
				Terms = jieba.cut(sequence[0], cut_all = False)
				for term in Terms:
					t = term.replace(' ', '')
					if len(t) > 0:
						PTerms.append([t, 'c'])
			else: # for english
				Terms = sequence[0].split()
				for term in Terms:
					PTerms.append([term, 'e'])
		# print (PTerms)
		''' ngram to get key terms '''
		prev_i = 0
		prev_j = 0
		isPrevTerm = False
		pervLan = ''
		for i in range(len(PTerms)):
			if isPrevTerm and i <= prev_i + prev_j:
				continue
			hasGottenTerm = False
			candidate_term = PTerms[i][0].lower()
			# english keywords
			if PTerms[i][1] == 'e':
				for j in range(5): # max: 5 terms (1 + 4)
					if (i + j > len(PTerms) - 1) or (j > 2 and isPrevTerm == False):
						break
					if j > 0:
						if PTerms[i + j][1] == 'c':
							break
						candidate_term += PTerms[i + j][0].lower()
					if candidate_term in StopWords: continue
					NAER_URL = 'http://terms.naer.edu.tw/search/?q=' + candidate_term + '&field=ti&op=AND&group=&num=10'
					Wiki_URL = 'https://en.wikipedia.org/wiki/' + '_'.join(candidate_term.lower().split())
					try:
						request = requests.get(Wiki_URL)
						resultSoup = BeautifulSoup(request.text, 'lxml')
						if 'Wikipedia does not have an article with this exact name' not in resultSoup.select('div#content')[0].text:
							isPrevTerm = True
							term_e = candidate_term.lower()
							term_c = ''
							plang = resultSoup.select('div#p-lang')[0]
							if len(plang) > 0:
								interwikizh = plang.select('li.interlanguage-link.interwiki-zh')
								if len(interwikizh) > 0:
									chineselink = interwikizh[0].select('a.interlanguage-link-target')[0]
									if len(chineselink) > 0:
										term_sc = chineselink.attrs.get('title').split()[0]
										Wiki_URL = 'https://zh.wikipedia.org/zh-tw/' + term_sc
										request = requests.get(Wiki_URL)
										resultSoup = BeautifulSoup(request.text, 'lxml')
										term_c = resultSoup.select('h1#firstHeading')[0].text
										for w in term_c:
											if NoteParagraphs[pid].content[i] < u'\u4e00' and NoteParagraphs[pid].content[i] > u'\u9fff':
												term_c = ''
												break
							if '{' in term_c: term_c = term_c[:term_c.index(' {')]
							if '(' in term_c: term_c = term_c[:term_c.index(' (')]
							if len(NTerms) == 0:
								NTerms.append({'c': candidate_term, 'e': term_e})
							elif not any(d['e'] == term_e for d in NTerms):
								NTerms.append({'c': term_c, 'e': term_e})
						else:
							isPrevTerm = False
					except:
						print ('except:', candidate_term)
			# chinese keywords to english
			else:
				if any(d['c'] == candidate_term for d in NTerms):
					continue
				for j in range(5): # max: 5 terms (1 + 4)
					if (i + j > len(PTerms) - 1) or (j > 2 and isPrevTerm == False):
						break
					if j > 0:
						if PTerms[i + j][1] == 'e':
							break
						candidate_term += PTerms[i + j][0]
					# National Academy for Educational Research
					NAER_URL = 'http://terms.naer.edu.tw/search/?q=' + candidate_term + '&field=ti&op=AND&group=&num=10'
					try:
						request = requests.get(NAER_URL)
						resultSoup = BeautifulSoup(request.text, 'lxml')
						if '抱歉，目前查無相關資料' not in resultSoup.select('div.leftcolumn')[0].text and resultSoup.select('tr.dash')[0].select('td.zhtwnameW')[0].select('a')[0].text == candidate_term: # if term exists in NAER
							isPrevTerm = True
							prev_i = i
							prev_j = j
							term_e = resultSoup.select('tr.dash')[0].select('td.ennameW')[0].select('a')[0].text.lower()
					# if 1 == 2: pass # if NAER shock down
					except:
						# Wiki
						Wiki_URL = 'https://zh.wikipedia.org/wiki/' + candidate_term
						try:
							request = requests.get(Wiki_URL)
							resultSoup = BeautifulSoup(request.text, 'lxml')
							if '维基百科目前还没有与上述标题相同的条目' not in resultSoup.select('div#content')[0].text and len(resultSoup.select('span.LangWithName')) > 0:
								isPrevTerm = True
								prev_i = i
								prev_j = j
								term_e = ''
							
								plang = resultSoup.select('div#p-lang')[0]
								if len(plang) > 0:
									interwikien = plang.select('li.interlanguage-link.interwiki-en')
									if len(interwikien) > 0:
										englishlink = interwikizh[0].select('a.interlanguage-link-target')[0]
										if len(englishlink) > 0:
											term_e = englishlink.attrs.get('title').split()[0]
							else:
								isPrevTerm = False
						except: print ('except:', candidate_term)
					if term_e == '':
						isPrevTerm = False
						continue
					if '{' in term_e: term_e = term_e[:term_e.index('{')].strip()
					if '(' in term_e: term_e = term_e[:term_e.index('(')].strip()
					if len(NTerms) == 0:
						NTerms.append({'c': candidate_term, 'e': term_e})
					elif not any(d['e'] == term_e for d in NTerms):
						NTerms.append({'c': candidate_term, 'e': term_e})

FIELD_NAME = ['c', 'e']
with open(NTERM_FOLDER + NTERM_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as termFile:
	writer = csv.DictWriter(termFile, fieldnames = FIELD_NAME)
	writer.writeheader()
	for t in NTerms:
		writer.writerow(t)

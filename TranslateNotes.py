# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile
from docx import *
import csv
from langdetect import detect
from googletrans import Translator
import re
import sys

# translate into english and remove stop words
# print (sys.argv)
NOTE_FOLDER = 'note/OM/ch15/'
NOTE_NAME = '生管_ch10_黃慈方'

UselessList = ['Summarization\\', '.docx']
NOTE_FOLDER = sys.argv[1]
NOTE_NAME = sys.argv[3]
for w in UselessList: NOTE_NAME = NOTE_NAME.replace(w, '')
print (NOTE_NAME)
CHNOTE_FILE_NAME = NOTE_NAME + '.docx'
ENNOTE_FILE_NAME = NOTE_NAME + '_en.txt'
TOPIC_FOLDER = 'result/OM/'
TOPIC_FILE_NAME = 'Topics_supplementA.csv'

note = ''
d = Document(NOTE_FOLDER + CHNOTE_FILE_NAME)
for p in d.paragraphs:
	text = p.text.strip()
	if len(text) > 0:
		note += text + '\n'

Topics = []
with open (TOPIC_FOLDER + TOPIC_FILE_NAME, 'r', encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})

# translate into english and remove stop words
with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]
translator = Translator()
RawNoteWordsList = []
ChEnPuctuation = [{'c': '，', 'e': ', '}, {'c': '、', 'e': ', '}, {'c': '。', 'e': '. '}, {'c': '！', 'e': '! '}, {'c': '？', 'e': '? '}, {'c': '：', 'e': ': '}, {'c': '；', 'e': '; '}, {'c': '「', 'e': '‘'}, {'c': '」', 'e': '’'}, {'c': '『', 'e': '“'}, {'c': '』', 'e': '”'}, {'c': '（', 'e': '('}, {'c': '）', 'e': ')'}]
PunctuationMarks = ['.', '!', '?', ':', ';', '\'', '\"', ',', '※', '○', '●', '→', '←', '↓', '↑', '->', '◎', '§', '…']
SpecialMarks = ['+', '-', '*', '/', '=', '\\', '<', '>', '~', '@', '#', '(', ')', '[', ']', '{', '}', '|', '^', '–', '—']

with open(NOTE_FOLDER + ENNOTE_FILE_NAME, 'w', encoding = 'utf-8') as outFile:
	WordsList = []
	for term in Topics:
		if len(term['term_c']) > 0: note = note.replace(term['term_c'], ' ' + term['term_e'] + ' ')

	for p in ChEnPuctuation:
		note = note.replace(p['c'], p['e'])
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
			# if rawLine[i] == '?': print (rawLine[i-1], prev + '\t' + rawLine[i], curr )
			if (curr == 'o' and rawLine[i] != '-') or (curr != prev and (prev != 'd' and curr != 'd') and (rawLine[i] != '-' and rawLine[i - 1] != '-')):
				line += ' '
				prev = curr
			line += rawLine[i]
		Words = line.split()
		for wid in range(len(Words)):
			if re.match('(\d)+\.$', Words[wid]) or re.match('\((\d)+\)$', Words[wid]): 
				Words[wid] = ''
				continue
			if Words[wid] in SpecialMarks or Words[wid] in PunctuationMarks or re.match('(\d)+-?(\d)?$', Words[wid]): continue
			try:
				wordLan = detect(Words[wid])
				if wordLan == 'zh-tw' or wordLan == 'zh-cn' or wordLan == 'ja' or wordLan == 'ko':
					Words[wid] = translator.translate(Words[wid]).text.lower()
			except: pass
				# print (Words[wid], wordLan)
		line = ' '.join(Words).replace('  ', ' ').strip().lower()
		# print (line + '\n\n')
		for sw in StopWords:
			line = line.replace(' ' + sw + ' ', ' ')
			if re.match(sw + ' ', line): line = line[len(sw):].strip() # remove stopwords at the start of sentences
		for pm in PunctuationMarks: line = line.replace(pm, '')
		note[lid] = line
		outFile.write(line + '\n')		
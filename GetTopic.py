# -*- coding: UTF-8 -*-
import sys
import csv
import codecs

SUBJECT = 'OM'
CHAPTER = 'ch1'

SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
print (SUBJECT, CHAPTER)

NTERM_FOLDER = 'note/' + SUBJECT + '/'
BOOK_FOLDER = 'book/' + SUBJECT + '/'
TOPIC_FOLDER = 'topic/' + SUBJECT + '/'
NTERM_FILE_NAME = 'NTerms_' + CHAPTER + '.csv'
BTERM_FILE_NAME = 'BTerms.csv'
TOPIC_FILE_NAME = 'Topics_' + CHAPTER + '.csv'

NTerms = []
with open(NTERM_FOLDER + NTERM_FILE_NAME, encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		NTerms.append({'c': row['c'], 'e': row['e']})
		for i in range(len(NTerms[-1]['c'])):
			if NTerms[-1]['c'][i] >= u'\u4e00' and NTerms[-1]['c'][i] <= u'\u9fff':
				break
			if i == len(NTerms[-1]['c']) - 1 and (NTerms[-1]['c'][i] < u'\u4e00' or NTerms[-1]['c'][i] > u'\u9fff'):
				NTerms[-1]['c'] = ''

BTerms = []
with open(BOOK_FOLDER + BTERM_FILE_NAME, encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		BTerms.append({'term': row['term'], 'abbr': row['abbr'], 'pages': row['pages']})

Topics = []
BT = [bt['term'] for bt in BTerms]
BA = [bt['abbr'] for bt in BTerms]
nid = 0
l = len(NTerms)
while nid < l:
	if NTerms[nid]['e'] in BT:
		Topics.append({'term_e': NTerms[nid]['e'], 'abbr': BTerms[BT.index(NTerms[nid]['e'])]['abbr'], 'term_c': NTerms[nid]['c']})
	elif NTerms[nid]['e'] in BA:
		Topics.append({'term_e': BTerms[BA.index(NTerms[nid]['e'])]['term'], 'abbr': NTerms[nid]['e'], 'term_c': NTerms[nid]['c']})
	nid += 1

# for t in Topics:
# 	print (t)

with open(TOPIC_FOLDER + TOPIC_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as termFile:
	writer = csv.DictWriter(termFile, fieldnames = ['term_e', 'abbr', 'term_c'])
	writer.writeheader()
	for t in Topics:
		writer.writerow(t)
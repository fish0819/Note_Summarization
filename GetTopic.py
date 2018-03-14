# -*- coding: UTF-8 -*-
import csv
import codecs

NTerms = []
FILE_NAME = 'note\\NTerms_w3.csv'
with open(FILE_NAME, encoding = 'utf-8') as termFile:
	reader = csv.DictReader(termFile)
	for row in reader:
		NTerms.append({'c': row['c'], 'e': row['e']})

BTerms = []
FILE_NAME = 'book\\BTerms.csv'
with open(FILE_NAME, encoding = 'utf-8') as termFile:
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

for t in Topics:
	print (t)

with open('Topics.csv', 'w', newline = '', encoding = 'utf-8') as termFile:
	writer = csv.DictWriter(termFile, fieldnames = ['term_e', 'abbr', 'term_c'])
	writer.writeheader()
	for t in Topics:
		writer.writerow(t)
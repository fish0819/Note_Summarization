# -*- coding: UTF-8 -*-
import csv
import codecs

NTerms = []
FILE_NAME = 'note\\NTerms_w3.csv'
with codecs.open(FILE_NAME, encoding = 'utf-8', errors='ignore') as termFile:
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
for bt in BTerms:
	if bt['term'] in Topics or bt['abbr'] in Topics: continue
	if bt['term'] in [nt['e'] for nt in NTerms]: Topics.append(bt['term'])
	if bt['abbr'] in [nt['e'] for nt in NTerms]: Topics.append(bt['abbr'])

for t in Topics:
	print (t)
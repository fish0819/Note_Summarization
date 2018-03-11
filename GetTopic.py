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
	if NTerms[nid]['e'] not in BT and NTerms[nid]['e'] not in BA:
		nid += 1
		continue
	Topics.append(NTerms[nid])
	nid += 1

for t in Topics:
	print (t)

with open('Topics.csv', 'w', newline = '', encoding = 'utf-8') as termFile:
	writer = csv.DictWriter(termFile, fieldnames = ['c', 'e'])
	writer.writeheader()
	for t in Topics:
		writer.writerow(t)
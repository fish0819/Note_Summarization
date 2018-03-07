# -*- coding: UTF-8 -*-
import io
import re # for regular expression
import csv

FILE_NAME = 'book\\SubjectIndex.txt'

with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
	Lines = inFile.readlines()

for lid in range(len(Lines)):
	Lines[lid] = Lines[lid].replace('\n', '').strip()

lid = 0
Lines = [l for l in Lines if len(l) > 0]

FIELD_NAME = ['term', 'abbr', 'pages']
Indexes = []
StopWords = ['definition of', 'introduction to', 'assumptions of', 'calculation of']
Prepositions = ['at', 'in', 'on', 'of', 'across']
for line in Lines:
	line = line.lower()
	isSubentry = False
	abbr = ''
	subterm = []
	Pages = []
	rawPage = ''
	pattern = re.compile(', \D')
	if 'see also' in line: continue
	# remove stop words
	for w in StopWords:
		if ', ' + w in line: line = line.replace(', ' + w, '')
		elif re.match(w, line): continue
	# remove tags of specific fields
	for w in Prepositions:
		if ', ' + w in line: line = line[:re.search(', ' + w, line).start()] + line[re.search(', ' + w, line).end():]
		elif re.match(w, line): continue
	if re.search('\([^(]*\)', line): # (abbr)
		if line.index('(') > (line.index(')') - line.index('(') - 1):
			abbr = line[line.index('(') + 1:line.index(')')] + line[line.index(')') + 1:(re.search(', \d', line)).start()]
			line = line[:line.index(' (')] + line[line.index(')') + 1:]
		else:
			abbr = line[:line.index(' (')]
			if re.search(', \d', line): abbr += line[line.index(')') + 1:(re.search(', \d', line)).start()]
			line = line[line.index('(') + 1:line.index(')')] + line[line.index(')') + 1:]
	if re.search(', \d', line):
		rawPage = line[(re.search(', \d', line)).start() + 2:]
		line = line[:(re.search(', \d', line)).start()]
		RawPages = rawPage.split(', ')
		for pid in range(len(RawPages)):
			if 'f' in RawPages[pid] or 't' in RawPages[pid]:
				RawPages[pid] = RawPages[pid][:-1]
			if '–' in RawPages[pid]:
				for p in range(int(RawPages[pid][:RawPages[pid].index('–')].strip()), int(RawPages[pid][RawPages[pid].index('–') + 1:].strip()) + 1): Pages.append(p)
			else: Pages.append(int(RawPages[pid]))
	term = line
	#print ('term:', term + ',\t', 'abbr:', abbr + ',\t', 'page:', Pages)
	Indexes.append({'term': term, 'abbr': abbr, 'pages': Pages})


TERM_FILE_NAME = 'book\\BTerms.csv'
with open(TERM_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as termFile:
	writer = csv.DictWriter(termFile, fieldnames = FIELD_NAME)
	writer.writeheader()
	for index in Indexes:
		writer.writerow(index)
# -*- coding: UTF-8 -*-
import io
import re # for regular expression
import csv
import sys

SUBJECT = 'OM'
SUBJECT = sys.argv[1]
print (SUBJECT)

BOOK_FOLDER = 'book/' + SUBJECT + '/'
FILE_NAME = 'Index.txt'
TERM_FILE_NAME = 'BTerms.csv'

with open (BOOK_FOLDER + FILE_NAME, 'r', encoding = 'utf-8') as inFile:
	Lines = inFile.readlines()

for lid in range(len(Lines)):
	Lines[lid] = Lines[lid].replace('\n', '').strip()

lid = 0
Lines = [l for l in Lines if len(l) > 0]

FIELD_NAME = ['term', 'abbr', 'pages']
Indexes = []
StopWords = ['assumptions of', 'calculation of', 'definition of', 'introduction to', 'definition']
Prepositions = ['across', 'at', 'in', 'of', 'on']

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
		elif ' ' + w in line: line = line.replace(' ' + w, '')
		elif re.match(w, line): line = ''
	# remove tags of specific fields
	for w in Prepositions:
		if ', ' + w in line:
			tmpline = line[:re.search(', ' + w, line).start()]
			if re.search(', \d', line): line = tmpline + line[re.search(', \d', line).start():]
		elif w != 'of' and ' ' + w in line:
			tmpline = line[:re.search(' ' + w, line).start()]
			if re.search(', \d', line): line = tmpline + line[re.search(', \d', line).start():]
		elif re.match(w, line): line = ''
	if line == '': continue
	if re.search('\([^(]*\)', line): # (abbr)
		if line.index('(') > (line.index(')') - line.index('(') - 1):
			abbr = line[line.index('(') + 1:line.index(')')] + line[line.index(')') + 1:(re.search(', \d', line)).start()]
			line = line[:line.index(' (')] + line[line.index(')') + 1:]
		else:
			abbr = line[:line.index(' (')]
			if re.search(', \d', line): abbr += line[line.index(')') + 1:(re.search(', \d', line)).start()]
			line = line[line.index('(') + 1:line.index(')')] + line[line.index(')') + 1:]
	Words = [w.strip() for w in re.split(',|\.', line) if w != '' and w != None] # use ',' and '.' to split a string
	term = ''
	for w in Words:
		# page no.
		if re.match('(\d)+[ft]?$', w): # eg. 123f, 26, 33t
			Pages.append(int(w.replace('f', '').replace('t', '')))
		elif re.match('(\d)+[ft]?-(\d)+[ft]?$', w) or re.match('(\d)+[ft]?–(\d)+[ft]?$', w): # eg. 111-120
			start = int(w[:re.search('[-–]', w).start()].replace('f', '').replace('t', ''))
			end = int(w[re.search('[-–]', w).start() + 1:].replace('f', '').replace('t', ''))
			if start <= end:
				for p in range(start, end + 1): Pages.append(p)
			else:
				Pages.append(start)
				Pages.append(end)
		# term
		else:
			term += w + ' '
	Pages = sorted(list(set(Pages)))
	Indexes.append({'term': term.strip(), 'abbr': abbr, 'pages': Pages})
	# print ('term:', term + ',\t', 'abbr:', abbr + ',\t', 'page:', Pages)

with open(BOOK_FOLDER + TERM_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as termFile:
	writer = csv.DictWriter(termFile, fieldnames = FIELD_NAME)
	writer.writeheader()
	for index in Indexes:
		writer.writerow(index)

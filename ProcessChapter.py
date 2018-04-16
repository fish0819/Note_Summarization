import io
import re # for regular expression
import sys

SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
# SUBJECT = 'OM'
# CHAPTER = 'ch1'

# get content
BOOK_FOLDER = 'book/' + SUBJECT + '/'
BOOK_FILE_NAME = CHAPTER + '.txt'

with open (BOOK_FOLDER + BOOK_FILE_NAME, 'r', encoding = 'utf-8') as inFile:
	Lines = inFile.readlines()

pattern1 = '.+[\.:]$' # end with '.' or ':'
pattern2 = '[^A-Z].*$' # not start with capital letter
pattern3 = '[^a-z\d]+$' # all capital letter (maybe title)

Symbols = ['', '', '', '', '', '', '', '•', '○', '●', '◎', '↑', '↓', '←', '→', '->', '<-', '`']
for lid in range(len(Lines)):
	Lines[lid] = Lines[lid].replace('\n', '').strip()
	for s in Symbols:
		Lines[lid] = Lines[lid].replace(s, '').strip()

lid = 0
while lid < len(Lines):
	if len(Lines[lid]) == 0:
		del Lines[lid]
		continue
	if not re.match(pattern1, Lines[lid - 1]):# not end with '.' or ':'
		if re.match(pattern2, Lines[lid]): # start with lowercase letter
			Lines[lid - 1] += ' ' + Lines[lid]
			del Lines[lid]
			continue
		elif re.match(pattern3, Lines[lid]) and re.match(pattern1, Lines[lid - 1]):
			Lines[lid - 1] += ' ' + Lines[lid]
			del Lines[lid]
			continue
		elif (re.match(pattern3, Lines[lid]) and re.match(pattern3, Lines[lid - 1])) or re.match('.+,$', Lines[lid - 1]) or re.match('[A-Z][a-z]+.*\.', Lines[lid - 1]):
			Lines[lid - 1] += ' ' + Lines[lid]
			del Lines[lid]
			continue
	lid += 1

# for line in Lines:
	# print (line)

with open (BOOK_FOLDER + BOOK_FILE_NAME, 'w', encoding = 'utf-8') as outFile:
	for line in Lines:
		outFile.write(line + '\n')

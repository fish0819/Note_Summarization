import io
import re # for regular expression

FILE_NAME = 'book\\SubjectIndex.txt'

with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
	Lines = inFile.readlines()

pattern1 = '^\D+.*[^\dft]{1}$'
pattern2 = '^(\d)+[ft]?$' # start with page number
pattern3 = '.*(\d)[ft]?$' # page numbers followed by f have figures; followed by t have tables

for lid in range(len(Lines)):
	Lines[lid] = Lines[lid].replace('\n', '').strip()

lid = 0
while lid < len(Lines):
	if len(Lines[lid]) == 0:
		del Lines[lid]
		continue
	if re.match(pattern2, Lines[lid]):
		if Lines[lid - 1][-1] != ',':
			Lines[lid - 1] += ','
		Lines[lid - 1] += ' ' + Lines[lid]
		del Lines[lid]
		continue
	m = re.match(pattern1, Lines[lid])
	while m:
		# print ('Old:', Lines[lid])
		if lid == len(Lines): continue
		if len(Lines[lid + 1]) == 0: break
		Lines[lid] += ' ' + Lines[lid + 1]
		# print ('New:', Lines[lid])
		del Lines[lid + 1]
		m = re.match(pattern1, Lines[lid])
	if '. See' in Lines[lid]:
		print (Lines[lid])
		Lines.insert(lid + 1, Lines[lid][Lines[lid].index('See'):])
		Lines[lid] = Lines[lid][:Lines[lid].index('. See')]
		lid += 1
	lid += 1

# for line in Lines:
# 	print (line)

with open (FILE_NAME, 'w', encoding = 'utf-8') as outFile:
	for line in Lines:
		outFile.write(line + '\n')
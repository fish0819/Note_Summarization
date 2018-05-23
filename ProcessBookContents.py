import io
import re # for regular expression

FILE_NAME = 'book\\Contents.txt'

with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
	Lines = inFile.readlines()

pattern1 = '.*\D$'
pattern2 = '^(\d)+$'

for lid in range(len(Lines)):
	Lines[lid] = Lines[lid].replace('\n', '').strip()

lid = 0
while lid < len(Lines):
	if len(Lines[lid]) == 0:
		del Lines[lid]
		continue
	if re.match(pattern2, Lines[lid]):
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
	lid += 1

with open (FILE_NAME, 'w', encoding = 'utf-8') as outFile:
	for line in Lines:
		outFile.write(line + '\n')

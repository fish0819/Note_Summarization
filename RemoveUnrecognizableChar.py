UnrecogCharList = ['', '', '', '', '', '', '']

rawText = ''
FILE_NAME = 'book\\Supplement-A'
with open (FILE_NAME + '_raw.txt', 'r', encoding = 'UTF-8') as inFile:
	while True:
		try:
			char = inFile.read(1)
		except Exception as e:
			print ('Error:', e)
			continue
		if not char:
			break
		if char in UnrecogCharList: char = ''
		rawText += char
LineList = [s.strip() for s in rawText.splitlines()]
text = ''
for i in range(len(LineList)):
	if LineList[i] == '': text += '\n'
	elif LineList[i][-1] == '-': text += LineList[i][:len(LineList[i])]
	else: text += (LineList[i] + ' ')

with open (FILE_NAME + '.txt', 'w', encoding = 'UTF-8') as outFile:
	outFile.write(text)

# with open ('Supplement-A.txt', 'r', encoding = 'UTF-8') as inFile:
# 	with open ('Supplement-A-1.txt', 'w', encoding = 'UTF-8') as outFile:
# 		while True:
# 			try:
# 				char = inFile.read(1)
# 			except Exception as e:
# 				print ('Error:', e)
# 				continue
# 			if not char:
# 				break
# 			if char in UnrecogCharList: char = ''
# 			outFile.write(char)

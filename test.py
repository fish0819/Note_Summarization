import numpy

SentenceList = []
with open ('Supplement-A.txt', 'r', encoding = 'UTF-8') as inFile:
	SentenceList = inFile.readlines()
SentenceList = [s.replace('\n', '').strip() for s in SentenceList]
print (SentenceList)

# text = '      Hello world!\n  \n     What a good day.   '
# print (text)
# print ([s.strip() for s in text.splitlines()])
# text = text.strip()
# print (text)


# with open ('Supplement-A.txt', 'r') as inFile:
# 	LineList = inFile.readlines()
# text = ''
# for i in range(len(LineList)):
# 	if LineList[i] == '': text += '\n'
# 	elif LineList[i][-1] == '-': text += LineList[i][:len(LineList[i])]
# 	else: text += (LineList[i] + ' ')
# print (text)



# import re # for regular expression
# 
# text = 'gfgfdAAA1234ZZZuijjkAAAA123333ZZZZZ'

# m = re.search('AAA(.+?)ZZZ', text)
# print (m)
# if m:
# 	print (m.group(0))
# 	print (m.group(1))


# pattern = re.compile('\.[A-Z]')
# text = 'A good day.Hi!'
# print (pattern.match(text))
# result = re.search('\.[A-Z]', text)
# if result:
# 	print (result)
# 	print (result.group(0))

# from sklearn.metrics.pairwise import cosine_similarity

# print (cosine_similarity([1, 2, 0], [2, 2, 1]))
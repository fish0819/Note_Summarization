from docx import *
import jieba
import re # to check if a string contains chinese char
import requests
from bs4 import BeautifulSoup

class Paragraph:
    def __init__(self, content, KeyTerms):
        self.content = content
        self.KeyTerms = []

''' read docx '''
FILE_NAME = 'test.docx'

d = Document(FILE_NAME)
ParagraphList = []
pid = 0
for p in d.paragraphs:
	if len(p.text) == 0:
		if len(ParagraphList) == pid + 1:
			pid += 1
		continue
	if pid == len(ParagraphList):
		ParagraphList.append(Paragraph(p.text, []))
	else:
		ParagraphList[pid].content += ' ' + p.text

''' segmentation '''
# 之後要判斷 paragraph 時可能會用到 '\t'
PunctuationList = ['\t', '\n', '，', '。', '！', '？', '：', '（', '）', '、', ',', '.', '!', '?', ':', '(', ')', '…']
for pid in range(len(ParagraphList)):
	prev = '' # 'c' or 'e'
	Sequences = [] # [sequence, lanuage]
	PTerms = []
	# split chinese and english sequences
	for i in range(len(ParagraphList[pid].content)):
		if ParagraphList[pid].content[i] in PunctuationList: # remove punctuation
			Sequences[len(Sequences) - 1][0]  += ' '
			continue
		if (ParagraphList[pid].content[i] > u'\u4e00' and ParagraphList[pid].content[i] < u'\u9fff'): # determine if the char is chinese
			if prev != 'c':
				prev = 'c'
				Sequences.append([ParagraphList[pid].content[i], prev])
			else: Sequences[len(Sequences) - 1][0] += ParagraphList[pid].content[i]
		else:
			if prev != 'e':
				prev = 'e'
				Sequences.append([ParagraphList[pid].content[i], prev])
			else: Sequences[len(Sequences) - 1][0] += ParagraphList[pid].content[i]
	for sequence in Sequences:
		if sequence[1] == 'c': # for chinese
			Terms = jieba.cut(sequence[0], cut_all = False)
			for term in Terms:
				t = term.replace(' ', '')
				if len(t) > 0:
					PTerms.append([t, 'c'])
		else: # for english
			Terms = sequence[0].split()
			for term in Terms:
				PTerms.append([term, 'e'])
	print (PTerms)
	''' ngram to get key terms '''
	prev_i = 0
	prev_j = 0
	isPrevTerm = False
	pervLan = ''
	for i in range(len(PTerms)):
		if isPrevTerm and i <= prev_i + prev_j:
			continue
		hasGottenTerm = False
		if PTerms[i][1] == 'e':
			continue
		candidate_term = PTerms[i][0]
		for j in range(5): # max: 5 terms (1 + 4)
			if (i + j > len(PTerms) - 1) or (j > 2 and isPrevTerm == False):
				break
			if j > 0:
				if PTerms[i + j][1] == 'e':
					break
				candidate_term += PTerms[i + j][0]
			print (candidate_term)
			# National Academy for Educational Research
			NAER_URL = 'http://terms.naer.edu.tw/search/?q=' + candidate_term + '&field=ti&op=AND&group=&num=10'
			request = requests.get(NAER_URL)
			resultSoup = BeautifulSoup(request.text, 'lxml')
			if '抱歉，目前查無相關資料' not in resultSoup.select('div.leftcolumn')[0].text and resultSoup.select('tr.dash')[0].select('td.zhtwnameW')[0].select('a')[0].text == candidate_term: # if term exists in NAER
				isPrevTerm = True
				prev_i = i
				prev_j = j
				print (resultSoup.select('tr.dash')[0].select('td.ennameW')[0].select('a')[0].text, '(from 學術名詞計辭書資訊網)\n')
			else:
				# Wiki
				Wiki_URL = 'https://zh.wikipedia.org/wiki/' + candidate_term
				request = requests.get(Wiki_URL)
				resultSoup = BeautifulSoup(request.text, 'lxml')
				if '维基百科目前还没有与上述标题相同的条目' not in resultSoup.select('div#bodyContent')[0].text and len(resultSoup.select('span.LangWithName')) > 0:
					isPrevTerm = True
					prev_i = i
					prev_j = j
					print (resultSoup.select('span.LangWithName')[0].select('span')[0].text, '(from 維基百科)\n')
				else:
					isPrevTerm = False
					print ('no result\n')
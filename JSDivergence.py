''' Jensen-Shannon Divergence '''
import re
from sklearn.feature_extraction.text import CountVectorizer
import dit

with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
	StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]

for sid in range(len(SelectedSenList)):
	for sw in StopWords:
		if re.match(sw + ' ', SelectedSenList[sid]): SelectedSenList[sid] = SelectedSenList[sid].replace(sw + ' ', '')
		if re.search(' ' + sw + ' ', SelectedSenList[sid]): SelectedSenList[sid] = SelectedSenList[sid].replace(' ' + sw + ' ', ' ')

with open ('book\\Supplement-A.txt', 'r', encoding = 'UTF-8') as inFile:
	ParagraphList = [s.replace('\n', '').strip().lower() for s in inFile.readlines()]
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
BookCorpus = []
for para in ParagraphList:
	BookCorpus += senTokenizer.tokenize(para)
	for sid in range(len(BookCorpus)):
		if re.match('(\d)+$', BookCorpus[sid]): BookCorpus[sid] = ''
BookCorpus = [s for s in BookCorpus if (len(s) > 0)]
for sid in range(len(BookCorpus)):
	for sw in StopWords:
		if re.match(sw + ' ', BookCorpus[sid]): BookCorpus[sid] = BookCorpus[sid].replace(sw + ' ', '')
		if re.search(' ' + sw + ' ', BookCorpus[sid]): BookCorpus[sid] = BookCorpus[sid].replace(' ' + sw + ' ', ' ')
BCountVectorizer = CountVectorizer()
BWordSenCount = np.array(BCountVectorizer.fit_transform(BookCorpus).toarray())
BWords = BCountVectorizer.get_feature_names()
BWordCount = np.sum(BWordSenCount, axis = 0)
BWordProb = [(c / np.sum(BWordCount)) for c in BWordCount]

with open ('result\\Summary_OM_w3.txt', 'r', encoding = 'utf-8') as inFile:
	SummaryCorpus = [s.replace('\n', '') for s in inFile.readlines()]
for sid in range(len(SummaryCorpus)):
	for sw in StopWords:
		if re.match(sw + ' ', SummaryCorpus[sid]): SummaryCorpus[sid] = SummaryCorpus[sid].replace(sw + ' ', '')
		if re.search(' ' + sw + ' ', SummaryCorpus[sid]): SummaryCorpus[sid] = SummaryCorpus[sid].replace(' ' + sw + ' ', ' ')
SCountVectorizer = CountVectorizer()
SWordSenCount = np.array(SCountVectorizer.fit_transform(SummaryCorpus).toarray())
SWords = SCountVectorizer.get_feature_names()
SWordCount = np.sum(SWordSenCount, axis = 0)
SWordProb = [(c / np.sum(SWordCount)) for c in SWordCount]

P = dit.ScalarDistribution(BWords, BWordProb)
Q = dit.ScalarDistribution(SWords, SWordProb)
print (jensen_shannon_divergence([P, Q]))
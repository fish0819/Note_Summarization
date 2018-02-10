import nltk.data # split text on sentences
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy # average and standard deviation
from numpy import linalg # l2 norm
import math # check inf

def CosineSim (List_x, List_y):
	dotProduct = numpy.dot(List_x, List_y)
	norm_x = linalg.norm(List_x)
	norm_y = linalg.norm(List_y)
	if norm_x * norm_y > 0:
		return (numpy.dot(List_x, List_y) / (linalg.norm(List_x) * linalg.norm(List_y)))
	else: return 0

''' get content '''
with open ('book\\Supplement-A.txt', 'r', encoding = 'UTF-8') as inFile:
	RawParagraphList = inFile.readlines()
RawParagraphList = [s.replace('\n', '').strip() for s in RawParagraphList]
#nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
SentenceList = [] # corpus
for para in RawParagraphList:
	SentenceList += senTokenizer.tokenize(para)

''' TSF '''
# parameter setting
K = 10 # the number of sentences in a block

countVectorizer = CountVectorizer()
TFList = countVectorizer.fit_transform(SentenceList).toarray()
tfidfTransformer = TfidfTransformer()
TFIDFList = tfidfTransformer.fit_transform(TFList).toarray()
TermList = countVectorizer.get_feature_names()

InnerSimList = [] # [i, innerSim] for each element; i starts from 0
OuterSimList = [] # [i, outerSim] for each element
DissimList = [] # [i, dissimilarity] for each element

for i in range(K - 1, (len(TFList) - K + 1)):
	innerSim = 0
	outerSim = 0
	for a in range(i - K + 1, i + 1):
		for b in range(a + 1, i + 1):
			if a != b:
				innerSim += CosineSim(TFList[a], TFList[b])
		for c in range(i + 1, i + K):
			outerSim += CosineSim(TFList[a], TFList[c])
	if innerSim == 0:
		continue
	dissim = (innerSim - outerSim) / innerSim
	if math.isinf(dissim):
		print ('inner:', innerSim)
		print ('outer:', outerSim)
		continue
	InnerSimList.append([i, innerSim])
	OuterSimList.append([i, outerSim])
	DissimList.append({'i': i, 'dissim': dissim})

avg_dissim = numpy.mean([d['dissim'] for d in DissimList])
dev_dissim = numpy.std([d['dissim'] for d in DissimList])
print ('Avg =', avg_dissim)
print ('Dev =', dev_dissim)

DISSIM_THRESHOLD = avg_dissim + 0.35 * dev_dissim # the threshold of the dissimilarity

current_i = 0
ParagrahList = []
for d in DissimList:
	if d['dissim'] > DISSIM_THRESHOLD:
		ParagrahList.append(' '.join(SentenceList[current_i:d['i'] + 1]))
		current_i = d['i'] + 1
ParagrahList.append(' '.join(SentenceList[current_i:]))

print (len(ParagrahList))
for p in ParagrahList:
	print (p + '\n\n')
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import nltk.data # split text on sentences
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy # average and standard deviation

''' get content '''
rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec = 'UTF-8', laparams = laparams)
fp = open('Chapter 1.pdf', 'rb')
interpreter = PDFPageInterpreter(rsrcmgr, device)
maxpages = 0
pagenos = set()

PageContentList = []
for page in PDFPage.get_pages(fp, pagenos, maxpages = maxpages, password = '', caching = True, check_extractable = True):
	# read_position = retstr.tell() # it will be 0 on the first page
	interpreter.process_page(page)
	# retstr.seek(read_position, 0)
	# PageContentList.append(retstr.read())
text = retstr.getvalue()
fp.close()
device.close()
retstr.close()
print (text)

''' TSF '''
# parameter setting
K = 5 # the number of sentences in a block
DISSIM_THRESHOLD = 0.5 # the threshold of the dissimilarity

SentenceList = []
# nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
SentenceList = senTokenizer.tokenize(text) #corpus
print (SentenceList)

"""
countVectorizer = CountVectorizer()
TFList = countVectorizer.fit_transform(SentenceList).toarray()
tfidfTransformer = TfidfTransformer()
TFIDFList = tfidfTransformer.fit_transform(TFList).toarray()
TermList = countVectorizer.get_feature_names()

InnerSimList = [] # [i, innerSim] for each element; i starts from 0
OuterSimList = [] # [i, outerSim] for each element
DissimList = [] # [i, dissimilarity] for each element

for i in range(K - 1, len(TFList)):
	innerSim = 0
	outerSim = 0
	for a in range(i - K + 1, i + 1):
		for b in range(a + 1, i + 1):
			if a != b:
				print ('Sa:', TFList[a])
				print ('Sb:', TFList[b])
				innerSim += cosine_similarity(numpy.reshape(TFList[a], (-1, 1)), numpy.reshape(TFList[b], (-1, 1)))[0][0]
				# cosine_similarity needs 2d arrays for input, and will output a 2d array
		for c in range(i + 1, i + K):
			outerSim += cosine_similarity(numpy.reshape(TFList[a], (-1, 1)), numpy.reshape(TFList[c], (-1, 1)))[0][0]
	InnerSimList.append([i, innerSim])
	OuterSimList.append([i, outerSim])
	if innerSim == 0:
		print ('Error:', 'i =', i, 'innerSim == 0')
		continue
	DissimList.append([i, (innerSim - outerSim) / outerSim])

print ('Avg =', numpy.mean(DissimList))
print ('Dev =', numpy.std(DissimList))
"""

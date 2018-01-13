from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import nltk.data # split text on sentences
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

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
	read_position = retstr.tell() # it will be 0 on the first page
	interpreter.process_page(page)
	retstr.seek(read_position, 0)
	PageContentList.append(retstr.read())
text = retstr.getvalue()
fp.close()
device.close()
retstr.close()

''' TSF '''
# parameter setting
K = 5 # the number of sentences in a block
DISSIM_THRESHOLD = 0.5 # the threshold of the dissimilarity

SentenceList = []
# nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
SentenceList = senTokenizer.tokenize(text) #corpus
countVectorizer = CountVectorizer()
TFList = countVectorizer.fit_transform(corpus).toarray()



InnerSimList = [] # [i, innerSim] for each element
OuterSimList = [] # [i, outerSim] for each element
DissimList = [] # [i, dissimilarity] for each element

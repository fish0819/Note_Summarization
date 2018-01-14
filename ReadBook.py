from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io

rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec = 'UTF-8', laparams = laparams)
# fp = open('Subject Index.pdf', 'rb')
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
# with open ('Book.txt', 'w', encoding = 'UTF-8') as outFile:
# 	for text in PageContentList:
# 		try:
# 			if text[0] == ' ':
# 				text = text.replace(' ', '')
# 			text = text.replace('', '\n')
# 			outFile.write (text)
# 		except Exception as e:
# 			print (e)
		# print (text)


# from docx import *

# ''' read docx '''
# FILE_NAME = 'Subject Index.docx'

# d = Document(FILE_NAME)
# for p in d.paragraphs:
# 	print (p.text)

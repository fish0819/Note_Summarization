import PyPDF2
# pdf_file = open('content & index_OM.pdf', 'rb+')
pdf_file = open('Subject Index.pdf', 'rb+')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
print (number_of_pages)
if read_pdf.isEncrypted:
	read_pdf.decrypt('') # the pdf's password
	print (read_pdf.getNumPages())
for i in range(number_of_pages):
	page = read_pdf.getPage(i)
	page_content = page.extractText()
	print (page_content)
pdf_file.close()


# import textract
# text = textract.process('Subject Index.pdf')
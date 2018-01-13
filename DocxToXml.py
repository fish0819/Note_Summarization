from docx import *
from lxml import etree

import os
import sys

FILE_NAME = '生管_張朝華_w2.docx'

try:
	import pypandoc
	from tidylib import tidy_document
	output = pypandoc.convert_file(FILE_NAME, 'rst', format = 'md', encoding = 'utf-8')
	print (output)
except ImportError:
	print("\n\nRequires pypandoc and pytidylib. See requirements.txt\n\n")



# d = opendocx(FILE_NAME)
# words = d.xpath('//w:r', namespaces=d.nsmap)

# WPML_URI = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
# tag_rPr = WPML_URI + 'rPr'
# tag_highlight = WPML_URI + 'highlight'
# tag_val = WPML_URI + 'val'

# for word in words:
#     for rPr in word.findall(tag_rPr):
#         if rPr.find(tag_highlight).attrib[tag_val] == 'yellow':
#             print (word.find(tag_t).text)
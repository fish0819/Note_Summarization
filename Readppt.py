#import pptx
from pptx import Presentation
import PyPDF2

FILE_NAME = '01_Array.pptx'
prs = Presentation(FILE_NAME)
slides = prs.slides
ContentList = []
NoteList = []
for slide in prs.slides:
	if slide.has_notes_slide:
		# print (slides.index(slide) + 1)
		# noteSlide = slide.notes_slide
		for shape in slide.notes_slide.shapes:
			if shape.text != '':
				NoteList.append(shape.text)
			# print ('\nname:', shape.name, '\ntext:', shape.text)
	for shape in slide.shapes:
		if not shape.has_text_frame:
			continue
		for paragraph in shape.text_frame.paragraphs:
			content = ''
			for run in paragraph.runs:
				content += run.text
			if len(content) > 0:
				ContentList.append(content)
			# for run in paragraph.runs:
			# 	ContentList.append(run.text)
print (ContentList)
print (NoteList)
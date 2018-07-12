# -*- coding: UTF-8 -*-
import csv

def GetTopics (FILE_NAME):
    Topics = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as termFile:
        reader = csv.DictReader(termFile)
        for row in reader:
            Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})
    return Topics

def GetStopWords (FILE_NAME):
    with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
        StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]
    return StopWords

def GetBookPara (FILE_NAME, Topics):
    ParaSenList = []
    Para = []
    ParagraphList = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
        while True:
            sen = inFile.readline()
            if not sen: break
            sen = sen.replace('\n', '')
            if len(sen) == 0:
                if len(Para) > 0:
                    ParaSenList.append(Para)
                    Para = []
            else: Para.append(sen)
    for para in ParaSenList:
        ParagraphList.append(' '.join(para))
    for pid in range(len(ParagraphList)):
        ParagraphList[pid] = {'topic': [], 'content': ParagraphList[pid]}
        for term in Topics:
            if term['term_e'] in ParagraphList[pid]['content'] or (term['abbr'] != '' and (' ' + term['abbr'] + ' ' in ParagraphList[pid]['content'] or  '(' + term['abbr'] + ')' in ParagraphList[pid]['content'])):
                ParagraphList[pid]['topic'].append(term['term_e'])
    return ParagraphList

def GetNotePara (FILE_NAME):
    MixedNoteParaList = []
    with open (FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            MixedNoteParaList.append({'content': row['content'], 'topic': row['topic'].replace('[\'', '').replace('\']', '').split('\', \''), 'sid': int(row['sid'])})
    return MixedNoteParaList

def GetSlides (FILE_NAME):
    Slides = []
    with open (FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            s = {'title': row['title'], 'content': row['content'], 'topic': row['topic'].replace('[\'', '').replace('\']', '').split('\', \'')}
            Slides.append(s)
    return Slides

def GetBookParaText (FILE_NAME):
    Para = []
    BookParaList = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
        while True:
            sen = inFile.readline()
            if not sen: break
            sen = sen.replace('\n', '')
            if len(sen) == 0:
                if len(Para) > 0:
                    BookParaList.append(Para)
                    Para = []
            else: Para.append(sen)
    return BookParaList

def GetNoteParaText (FILE_NAME):
    NoteParaList = []
    with open (FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            NoteParaList.append(row['content'].splitlines())
    return NoteParaList

def GetSlideText (FILE_NAME):
    SlideTextList = []
    with open (FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            SlideTextList.append(row['content'].splitlines())
    return SlideTextList

def GetExamText (FILE_NAME):
    ExamSenList = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as inFile:
        while True:
            sen = inFile.readline()
            if not sen: break
            sen = sen.replace('\n', '').strip()
            if len(sen) > 0:
                ExamSenList.append(sen)
    return ExamSenList

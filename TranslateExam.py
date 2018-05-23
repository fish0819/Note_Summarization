# -*- coding: UTF-8 -*-
''' translate into english and remove stop words '''
from os import listdir
from os.path import isfile
from docx import *
import csv
from langdetect import detect
from googletrans import Translator
import re
import sys
import GetDocuments

ExamChapters = {
    'OM': [['ch1', 'supplementA', 'ch3', 'ch6', 'ch7', 'ch8'], ['ch9', 'ch15', 'ch16'], ['ch10', 'ch12', 'ch13']], 
    'DS': [['ch2', 'ch3'], ['ch4', 'ch5', 'ch6'], ['ch6', 'ch7']] 
}

SUBJECT = 'DS'
EXAM = 3

# SUBJECT = sys.argv[1]
# EXAM = int(sys.argv[2])

EXAM_NAME = 'exam' + str(EXAM)
print (SUBJECT, EXAM_NAME)

EXAM_FOLDER = 'exam/' + SUBJECT + '/'
CHEXAM_FILE_NAME = EXAM_NAME + '.docx'
ENEXAM_FILE_NAME = EXAM_NAME + '.txt'
TOPIC_FOLDER = 'topic/' + SUBJECT + '/'

Topics = []
for c in ExamChapters[SUBJECT][EXAM - 1]:
    TOPIC_FILE_NAME = 'Topics_' + c + '.csv'
    with open (TOPIC_FOLDER + TOPIC_FILE_NAME, 'r', encoding = 'utf-8') as termFile:
        reader = csv.DictReader(termFile)
        for row in reader:
            if row['term_e'] not in [t['term_e'] for t in Topics]:
                Topics.append({'term_e': row['term_e'], 'abbr': row['abbr'], 'term_c': row['term_c']})

exam_content = ''
d = Document(EXAM_FOLDER + CHEXAM_FILE_NAME)
for p in d.paragraphs:
    text = p.text.strip()
    if len(text) > 0:
        exam_content += text + '\n'

# translate into english and remove stop words
with open ('stopwords.txt', 'r', encoding = 'utf-8') as inFile:
    StopWords = [sw.replace('\n', '') for sw in inFile.readlines()]
translator = Translator()
RawNoteWordsList = []
ChEnPuctuation = [{'c': '，', 'e': ', '}, {'c': '、', 'e': ', '}, {'c': '。', 'e': '. '}, {'c': '！', 'e': '! '}, {'c': '？', 'e': '? '}, {'c': '：', 'e': ': '}, {'c': '；', 'e': '; '}, {'c': '「', 'e': '‘'}, {'c': '」', 'e': '’'}, {'c': '『', 'e': '“'}, {'c': '』', 'e': '”'}, {'c': '（', 'e': '('}, {'c': '）', 'e': ')'}]
PunctuationMarks = ['.', '!', '?', ':', ';', '\'', '\"', ',', '※', '○', '●', '→', '←', '↓', '↑', '->', '◎', '§', '…']
SpecialMarks = ['+', '-', '*', '/', '=', '\\', '<', '>', '~', '@', '#', '(', ')', '[', ']', '{', '}', '|', '^', '–', '—']

with open(EXAM_FOLDER + ENEXAM_FILE_NAME, 'w', encoding = 'utf-8') as outFile:
    WordsList = []
    for term in Topics:
        if len(term['term_c']) > 0: exam_content = exam_content.replace(term['term_c'], ' ' + term['term_e'] + ' ')

    for p in ChEnPuctuation:
        exam_content = exam_content.replace(p['c'], p['e'])
    exam_content = exam_content.splitlines()
    for lid in range(len(exam_content)):
        rawLine = exam_content[lid]
        line = ''
        prev = '' # 'c', 'e', 'd' or 'o' (other)
        curr = ''
        if re.search('(\d)+\.\D', rawLine):
            rawLine = rawLine[:]
        for i in range(len(rawLine)):
            if rawLine[i] >= u'\u4e00' and rawLine[i] <= u'\u9fff': curr = 'c'
            elif (rawLine[i] >= u'\u0041' and rawLine[i] <= u'\u005a') or (rawLine[i] >= u'\u0061' and rawLine[i] <= u'\u007a'): curr = 'e'
            elif rawLine[i] >= u'\u0030' and rawLine[i] <= u'\u0039': curr = 'd'
            else: curr = 'o'
            if i == 0:
                prev = curr
                line = rawLine[i]
                continue
            # if rawLine[i] == '?': print (rawLine[i-1], prev + '\t' + rawLine[i], curr )
            if (curr == 'o' and rawLine[i] != '-') or (curr != prev and (prev != 'd' and curr != 'd') and (rawLine[i] != '-' and rawLine[i - 1] != '-')):
                line += ' '
                prev = curr
            line += rawLine[i]
        Words = line.split()
        for wid in range(len(Words)):
            if re.match('(\d)+\.$', Words[wid]) or re.match('\((\d)+\)$', Words[wid]): 
                Words[wid] = ''
                continue
            if Words[wid] in SpecialMarks or Words[wid] in PunctuationMarks or re.match('(\d)+-?(\d)?$', Words[wid]): continue
            try:
                wordLan = detect(Words[wid])
                if wordLan == 'zh-tw' or wordLan == 'zh-cn' or wordLan == 'ja' or wordLan == 'ko':
                    Words[wid] = translator.translate(Words[wid]).text.lower()
            except: pass
                # print (Words[wid], wordLan)
        line = ' '.join(Words).replace('  ', ' ').strip().lower()
        # print (line + '\n\n')
        for sw in StopWords:
            line = line.replace(' ' + sw + ' ', ' ')
            if re.match(sw + ' ', line): line = line[len(sw):].strip() # remove stopwords at the start of sentences
        for pm in PunctuationMarks: line = line.replace(pm, '')
        exam_content[lid] = line
        outFile.write(line + '\n')      
# -*- coding: utf-8 -*-
import sys
import os
import GetDocuments
import nltk.data # split text on sentences
import re
import numpy as np
import itertools
import time
import pyfpgrowth
import FPGrowth
from sklearn.feature_extraction.text import CountVectorizer

SUBJECT = 'OM'
CHAPTER = 'ch8'
SELECTEDRATIO = 0.1
THRESHOLD_SUPPORT = 10

# SUBJECT = sys.argv[1]
# CHAPTER = sys.argv[2]
# SELECTEDRATIO = abs(round(float(sys.argv[3]), 1))
# THRESHOLD_SUPPORT = int(sys.argv[4])
print (SUBJECT, CHAPTER, SELECTEDRATIO, THRESHOLD_SUPPORT)

start_time = time.time()

BOOK_FOLDER = 'book/' + SUBJECT + '/'
SUMMARY_FOLDER = 'result/' + SUBJECT + '/others/'
BOOKPARA_FILE_NAME = CHAPTER + '_TSF.txt'
SUMMARY_FILE_NAME = 'Summary_PatSum_' + CHAPTER + '.txt'

if not os.path.isdir(SUMMARY_FOLDER):
    os.makedirs(SUMMARY_FOLDER)

# preprocessing
StopWords = GetDocuments.GetStopWords('stopwords.txt')
PunctuationMarks = ['!', '?', ':', ';', '\'', '\"', ',']
BookParaList = GetDocuments.GetBookParaText(BOOK_FOLDER + BOOKPARA_FILE_NAME)
TOTALSENNUM = 0
RawBookSenList = []
BookSenList = []
#nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for p in BookParaList:
    TOTALSENNUM += len(p)
    RawBookSenList += p
sid = 0
while sid < len(RawBookSenList):
    s = RawBookSenList[sid]
    if re.match('^(\d)+\.$', s) or re.match('^[^A-Za-z]+$', s) or re.match('^[A-Za-z]\.$', s) or re.match('^\((\d)+\)$', s):
        del RawBookSenList[sid]
        continue
    for sw in StopWords:
        if re.match(sw + ' ', s): s = s.replace(sw, '').strip()
        elif re.search(' ' + sw + ' ', s): s = s.replace(' ' + sw + ' ', ' ')
    for m in re.finditer('\((\d)+\)', s):
        s = s.replace(m.group(0), '')
    for m in re.finditer('(\d)+\.\D', s):
        s = s.replace(m.group(0), '')
    for m in re.finditer('\([A-Za-z]+\)', s):
        s = s.replace(m.group(0), '')
    for m in re.finditer('[A-Za-z]+\. ', s):
        s = s.replace(m.group(0), '')
    for pun in PunctuationMarks: s = s.replace(pun, '').replace('  ', ' ').strip()
    if re.search('[A-Za-z]\.', s): s = s[:-1]
    BookSenList.append(s)
    sid += 1

# define class of pattern
class Pattern:
    def __init__(self, WordTuple, sid):
        self.WordTuple = WordTuple
        self.termNum = len(WordTuple)
        self.isFrequent = True
        self.isClosed = True
        self.CoverSenList = [sid]
    def add_sen(self, sid):
        self.CoverSenList.append(sid)
    def cal_freq(self):
        if len(self.CoverSenList) < THRESHOLD_SUPPORT: self.isFrequent = False
        return self.isFrequent
    def cal_supp(self):
        return (len(self.CoverSenList))

# find freqent itemsets
BSenWordsList = []
Operators = ['+', '-', '±', '×', '÷', '⊕', '⊗', '*', '/', '^', '<', '>', '(', ')', '[', ']', '{', '}']
for sid in range(len(BookSenList)):
    BSenWordsList.append(BookSenList[sid].split())
    wid = 0
    while wid < len(BSenWordsList[sid]):
        if BSenWordsList[sid][wid] in Operators: del BSenWordsList[sid][wid]
        elif re.match('^(\d)+(\.(\d)+)*$', BSenWordsList[sid][wid]): del BSenWordsList[sid][wid]
        else: wid += 1
# Itemsets = pyfpgrowth.find_frequent_patterns(BSenWordsList, THRESHOLD_SUPPORT).keys()
Itemsets = FPGrowth.find_frequent_patterns(BSenWordsList, THRESHOLD_SUPPORT).keys()
Itemsets = [set(items) for items in Itemsets]
i = 0
while i < len(Itemsets):
    count = 0
    for item in Itemsets[i]:
        if re.match('^[^A-Za-z]+$', item):
            count += 1
    if count >= 0.5 * len(Itemsets[i]): del Itemsets[i]
    else: i += 1
print (len(Itemsets))

# find patterns and their cover sentences
Patterns = []
PatternWords = []
for sid in range(len(BookSenList)):
    SenWords = BookSenList[sid].split()
    SenWordSet = set(SenWords)
    # tmpPatWords = []
    for items in Itemsets:
        pw = []
        if items.issubset(SenWordSet):
            for w in SenWords:
                if w in items: pw.append(w)
            if tuple(pw) not in PatternWords:
                PatternWords.append(tuple(pw))
                Patterns.append(Pattern(tuple(pw), sid))
            else:
                Patterns[PatternWords.index(tuple(pw))].add_sen(sid)
# find freqent patterns
pid = 0
while pid < len(Patterns):
    if not Patterns[pid].cal_freq():
        del Patterns[pid]
        del PatternWords[pid]
        continue
    pid += 1
print (len(Patterns))

# find closed patterns
ClosedPatterns = []
ClosedPatWords = []
for pid in range(len(Patterns)):
    if len(ClosedPatterns) == 0:
        ClosedPatWords.append(PatternWords[pid])
        ClosedPatterns.append(Patterns[pid])
        continue
    SubPatList = [] # cpid list
    for cpid in range(len(ClosedPatWords)):
        prev_i = prev_j = -1
        for i in range(len(ClosedPatWords[cpid])):
            if prev_i < i - 1: break
            for j in range(prev_j + 1, len(PatternWords[pid])):
                if ClosedPatWords[cpid][i] == PatternWords[pid][j]:
                    prev_i = i
                    prev_j = j
                    if i == len(ClosedPatWords[cpid]) - 1: SubPatList.append(cpid)
                    break
    allSubClosed = True
    if len(SubPatList) == 0: allSubClosed = False
    for i in range(len(SubPatList)):
        scpid = SubPatList[i] - i
        if ClosedPatterns[scpid].cal_supp() == Patterns[pid].cal_supp(): # subpattern is not closed
            ClosedPatterns[scpid].isClosed = False
            allSubClosed = False
            del ClosedPatWords[scpid]
            del ClosedPatterns[scpid]
    if not allSubClosed:
        ClosedPatWords.append(PatternWords[pid])
        ClosedPatterns.append(Patterns[pid])
print (len(ClosedPatterns))
# for cp in ClosedPatterns:
#     print (cp.WordTuple, len(cp.CoverSenList))

# calculate weight of closed patterns, weight of terms and tw of sentences
ClosedPatWeight = []
for cp in ClosedPatterns:
    ClosedPatWeight.append(len(cp.CoverSenList))
countVectorizer = CountVectorizer()
TermWeightList = countVectorizer.fit_transform(BookSenList).toarray().tolist()
TermWeights = np.sum(TermWeightList, axis = 0)
Terms = countVectorizer.get_feature_names()
# for t in Terms:
#     print (t)
SenTWList = []
SenPatList = [] # a list of lists of cpid
for sid in range(len(BSenWordsList)):
    sw = 0
    twdict = {}
    SenPat = []
    for cpid in range(len(ClosedPatterns)):
        if sid in ClosedPatterns[cpid].CoverSenList:
            SenPat.append(cpid)
            for w in ClosedPatterns[cpid].WordTuple:
                tmp_w = w.replace('-', '')
                if tmp_w not in Terms:
                    continue
                if len(twdict) == 0: twdict[w] = TermWeights[Terms.index(tmp_w)]
                elif w not in twdict.keys(): twdict[w] = TermWeights[Terms.index(tmp_w)]
                else: twdict[w] += TermWeights[Terms.index(tmp_w)]
    SenTWList.append(twdict)
    SenPatList.append(SenPat)

# find adjacency matrix R
R = []
for i in range(len(BSenWordsList)):
    R_i = []
    for j in range(len(BSenWordsList)):
        rij = 0
        if i == j:
            for cpid in SenPatList[i]: rij += len(ClosedPatterns[cpid].WordTuple) * len(ClosedPatterns[cpid].CoverSenList)
        else:
            for cpid in SenPatList[i]:
                if cpid in SenPatList[j]: rij += len(ClosedPatterns[cpid].WordTuple) * len(ClosedPatterns[cpid].CoverSenList)
        R_i.append(rij)
    R.append(R_i)

# calculate weight of sentence
SenWeights = []
l = 0.5 # lambda set in the paper
for sid in range(len(BookSenList)):
    twsum = 0
    for t, w in SenTWList[sid].items():
        twsum += w
    SenWeights.append(l * twsum + (1 - l) * np.max(R[sid]))
    # print (SenWeights[sid])
SortedSenWeights, SortedBookSenList = zip(*sorted(zip(SenWeights, RawBookSenList)))
print (len(SortedSenWeights), len(SortedBookSenList))

# select sentences
SELECTEDSENNUM = int(round(TOTALSENNUM * SELECTEDRATIO))
with open(SUMMARY_FOLDER + SUMMARY_FILE_NAME, 'w', encoding = 'utf-8') as outFile:
    sid = 0
    while sid < SELECTEDSENNUM:
        outFile.write(SortedBookSenList[sid] + '\n')
        sid += 1

end_time = time.time()
print ('cost time:', end_time - start_time)
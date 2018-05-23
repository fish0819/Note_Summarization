# -*- coding: UTF-8 -*-
''' search relative web '''
import re
import sys
import GetDocuments
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
import nltk.data # split text on sentences
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import TSF

SUBJECT = 'OM'
CHAPTER = 'ch10'
THRESHOLD_COSSIM = 0.2
THRESHOLD_DISSIM = 0.3

SUBJECT = sys.argv[1]
CHAPTER = sys.argv[2]
THRESHOLD_COSSIM = float(sys.argv[3])
THRESHOLD_DISSIM = float(sys.argv[4])
print (SUBJECT, CHAPTER, THRESHOLD_COSSIM, THRESHOLD_DISSIM)

K = 5

SLIDE_FOLDER = 'ppt/' + SUBJECT + '/'
MATCH_FOLDER = 'match/' + SUBJECT + '_' + str(THRESHOLD_COSSIM) + '/'
WEB_FOLDER = 'web/' + SUBJECT + '/'
COMBINEDSLIDE_FILE_NAME = CHAPTER + '_slides.csv'
BSMATCH_FILE_NAME = 'BSMatch_' + CHAPTER + '.csv'
WEB_FILE_NAME = 'WebSupp_' + CHAPTER + '.csv'

# nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

Slides = GetDocuments.GetSlides(SLIDE_FOLDER + COMBINEDSLIDE_FILE_NAME)
BMatchSList = []
SuppDocList = []
with open (MATCH_FOLDER + BSMATCH_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
    reader = csv.DictReader(inFile)
    for row in reader:
        sid = int(row['sid'])
        if row['pid'] == '':
            SuppDocList.append({'sid': sid, 'WebContent': []})
            query = '+'.join(Slides[sid]['title'].split()).lower()
            google_url = 'https://www.google.com/search?source=hp&hl=en&q=' + query # hl=interface_lan
            try:
                UrlList = []
                request = requests.get(google_url)
                resultSoup = BeautifulSoup(request.text, 'lxml')
                div_res = resultSoup.select('div#res')[0]
                h3 = div_res.select('h3')
                for i in range(3):
                    div_g = div_res.select('div.g')[i]
                    div_rc = div_res.select('div_rc')
                    h3_r = h3[i]
                    cite = div_g.select('cite')[0].text
                    url = cite
                    if '...' in url:
                        a = h3_r.select('a')[0]
                        href = a.attrs['href'].replace('/url?q=', '')
                        href = href[:re.search('&sa=', href).start()]
                        url = href
                    url = url.replace(' ', '')
                    if not re.match('http://', url) and not re.match('https://', url): url = 'http://' + url
                    UrlList.append(url)
            except Exception as err:
                print ('except:', err)
            for url in UrlList:
                WSenList = []
                try:
                    request = requests.get(url)
                    resultSoup = BeautifulSoup(request.text, 'lxml')
                    title_tag = resultSoup.title # 網頁標題標籤
                    for p in resultSoup.select('p'):
                        if len(p.text.strip()) > 0:
                            WSenList += senTokenizer.tokenize(re.sub('\s+', ' ', ' '.join(p.text.strip().replace('\t', ' ').split('\n'))).strip())
                except Exception as err:
                    print ('except:', err)
                if len(WSenList) > 2.5 * K:
                    WParaSenList = TSF.SegementPara(WSenList, K, THRESHOLD_DISSIM)
                else:
                    WParaSenList = [WSenList]
                for para in WParaSenList:
                    Corpus = [(' '.join(Slides[sid]['content'].splitlines())).lower(), (' '.join(para)).lower()]
                    countVectorizer = CountVectorizer()
                    TFList = countVectorizer.fit_transform(Corpus).toarray()
                    tfidfTransformer = TfidfTransformer()
                    TFIDFList = tfidfTransformer.fit_transform(TFList).toarray()
                    cos_sim = cosine_similarity(TFList[0].reshape(1, -1), TFList[1].reshape(1, -1))[0][0]
                    if cos_sim >= THRESHOLD_COSSIM:
                        SuppDocList[-1]['WebContent'].append('\n'.join(para))
with open (WEB_FOLDER + WEB_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as outFile:
    writer = csv.DictWriter(outFile, fieldnames = ['sid', 'WebContent'])
    writer.writeheader()
    for sd in SuppDocList:
        if len(sd['WebContent']) > 0:
            writer.writerow(sd)

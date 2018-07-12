from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import GetDocuments
import numpy as np # average and standard deviation
from numpy import linalg # l2 norm
import re

def SegementPara (SentenceList, K, THRESHOLD_DISSIM):
    StopWords = GetDocuments.GetStopWords('stopwords.txt')
    Corpus = []
    for s in SentenceList:
        for sw in StopWords:
            if re.match(sw + ' ', s): s = s.replace(sw, '').strip()
            elif re.search(' ' + sw + ' ', s): s = s.replace(' ' + sw + ' ', ' ')
        Corpus.append(s.lower())

    countVectorizer = CountVectorizer()
    TFList = countVectorizer.fit_transform(Corpus).toarray()
    tfidfTransformer = TfidfTransformer()
    TFIDFList = tfidfTransformer.fit_transform(TFList).toarray()
    TermList = countVectorizer.get_feature_names()

    InnerSimList = [] # [i, innerSim] for each element; i starts from 0
    OuterSimList = [] # [i, outerSim] for each element
    DissimList = [] # [i, dissimilarity] for each element

    for i in range(K - 1, (len(TFList) - K)):
        preSim = postSim = innerSim = outerSim = preCount = postCount = outerCount = 0
        for a in range(i - K + 1, i + 1):
            for b in range(a + 1, i + 1):
                if a != b:
                    preCount += 1
                    preSim += cosine_similarity(TFList[a].reshape(1, -1), TFList[b].reshape(1, -1))[0][0]
            for c in range(i + 1, i + K + 1):
                outerCount += 1
                outerSim += cosine_similarity(TFList[a].reshape(1, -1), TFList[c].reshape(1, -1))[0][0]
        for a in range(i + 1, i + K):
            for b in range(a + 1, i + K + 1):
                if a != b:
                    postCount += 1
                    postSim += cosine_similarity(TFList[a].reshape(1, -1), TFList[b].reshape(1, -1))[0][0]
        innerSim = (preSim / preCount + postSim / postCount) / 2
        outerSim /= outerCount
        if innerSim == 0:
            continue
        dissim = (innerSim - outerSim) / innerSim
        InnerSimList.append([i, innerSim])
        OuterSimList.append([i, outerSim])
        DissimList.append({'i': i, 'dissim': dissim})

    avg_dissim = np.mean([d['dissim'] for d in DissimList])
    dev_dissim = np.std([d['dissim'] for d in DissimList])
    print ('Avg =', avg_dissim)
    print ('Dev =', dev_dissim)

    current_i = 0
    ParaSenList = []
    for did in range(len(DissimList)):
        if DissimList[did]['dissim'] >= THRESHOLD_DISSIM:
            if did < len(DissimList) - 1:
                if DissimList[did]['i'] + 1 == DissimList[did + 1]['i'] and DissimList[did]['dissim'] < DissimList[did + 1]['dissim']: continue
            ParaSenList.append(SentenceList[current_i:DissimList[did]['i'] + 1])
            current_i = DissimList[did]['i'] + 1
    ParaSenList.append(SentenceList[current_i:])
    return ParaSenList
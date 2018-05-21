# -*- coding: UTF-8 -*-
import numpy as np
import csv
import sys

SUBJECT = 'DS'

JSD_FOLDER = 'result/'
JSD_FILE_NAME = SUBJECT + '.csv'
AVG_FILE_NAME = SUBJECT + '_avg.csv'

ResultList = []
with open (JSD_FOLDER + JSD_FILE_NAME, 'r', newline = '', encoding = 'utf-8') as inFile:
	reader = csv.reader(inFile, delimiter = ',')
	ResultList = list(reader)
del ResultList[0]
for rid in range(len(ResultList)):
	ResultList[rid] = [float(x) for x in ResultList[rid][2:]]

a = b = r = 0
AvgJSDList = []
JSD_NS = []
JSD_BS = []
for Result in ResultList:
	if Result[0] == a and Result[1] == b and Result[2] == r:
		JSD_NS.append(Result[3])
		JSD_BS.append(Result[4])
	else:
		if len(JSD_NS) > 0:
			AvgJSDList.append([a, b, r, np.average(JSD_NS), np.average(JSD_BS)])
		a = Result[0]
		b = Result[1]
		r = Result[2]
		JSD_NS = [Result[3]]
		JSD_BS = [Result[4]]
AvgJSDList.append([a, b, r, np.average(JSD_NS), np.average(JSD_BS)])

with open (JSD_FOLDER + AVG_FILE_NAME, 'w', newline = '', encoding = 'utf-8') as outFile:
	writer = csv.writer(outFile, delimiter = ',')
	writer.writerow(['Alpha','Beta','Gamma','JS(N,S)','JS(B,S)'])
	writer.writerows(AvgJSDList)

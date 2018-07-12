# -*- coding: UTF-8 -*-
import csv

def get_slides (FILE_NAME):
    slides = []
    with open (FILE_NAME, 'r', newline = '', encoding = 'utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            s = {'title': row['title'], 'content': row['content'], 'topic': row['topic'].replace('[\'', '').replace('\']', '').split('\', \'')}
            slides.append(s)
    return slides

def get_matches (FILE_NAME):
    matches = []
    with open (FILE_NAME, 'r', newline = '', encoding = 'utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row['sid'] == '': sid = -1
            else: sid = int(row['sid'])
            if row['pid'] == '': pid = -1
            else: pid = int(row['pid'])
            m = {'npid': int(row['npid']), 'sid': sid, 'pid': pid}
            matches.append(m)
    return matches

def get_bookparas (FILE_NAME):
    para = []
    bookpara_list = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as infile:
        while True:
            sen = infile.readline()
            if not sen: break
            sen = sen.replace('\n', '')
            if len(sen) == 0:
                if len(para) > 0:
                    bookpara_list.append(para)
                    para = []
            else: para.append(sen)
    return bookpara_list

def get_noteparas (FILE_NAME):
    notepara_list = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            notepara_list.append(row['ch_content'].splitlines())
    return notepara_list

def get_summaries (FILE_NAME):
    summary_list = []
    with open (FILE_NAME, 'r', encoding = 'utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            pid = int(row['pid'])
            if len(summary_list) == 0: summary_list.append({'pid': pid, 'content': ('\n'.join(row['sentence'].replace('[\'', '').replace('\']', '').split('\', \''))).replace('[]', '')})
            elif pid not in [s['pid'] for s in summary_list]: summary_list.append({'pid': pid, 'content': ('\n'.join(row['sentence'].replace('[\'', '').replace('\']', '').split('\', \''))).replace('[]', '')})
    return summary_list
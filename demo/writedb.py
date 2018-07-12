# -*- coding:utf-8 -*-
import os
import sys
import load_file as lf
import pymysql

subject_list = [{'subject': 'OM', 'chapters': ['ch1', 'ch3', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch15', 'ch16', 'supplementA']}, {'subject': 'DS', 'chapters': ['ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch9']}]

for s in subject_list:
    subject = s['subject']
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', db = 'notesum_' + subject.lower(), charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            for chapter in s['chapters']:
                sql = 'INSERT INTO `chp` (`chapter`) VALUES (%s)'
                cursor.execute(sql, (chapter))

                slides = lf.get_slides('ppt/' + subject + '/' + chapter + '_slides.csv')
                noteparas = lf.get_noteparas('note/' + subject + '/' + chapter + '/Mixed_' + chapter + '.csv')
                bookparas = lf.get_bookparas('book/' + subject + '/' + chapter + '_TSF.txt')
                summaries = lf.get_summaries('summary/' + subject + '/Summary_' + chapter + '.csv')
                matches = lf.get_matches('match/' + subject + '/NSBMatch_' + chapter + '.csv')
                
                for sid in range(len(slides)):
                    sql = 'INSERT INTO `ppt` (`chapter`, `sid`, `title`, `content`) VALUES (%s, %s, %s, %s)'
                    cursor.execute(sql, (chapter, sid, slides[sid]['title'], slides[sid]['content']))
                for npid in range(len(noteparas)):
                    sql = 'INSERT INTO `note` (`chapter`, `npid`, `content`) VALUES (%s, %s, %s)'
                    cursor.execute(sql, (chapter, npid, '\n'.join(noteparas[npid])))
                for bpid in range(len(bookparas)):
                    sql = 'INSERT INTO `book` (`chapter`, `bpid`, `content`) VALUES (%s, %s, %s)'
                    cursor.execute(sql, (chapter, bpid, '\n'.join(bookparas[bpid])))
                for summary in summaries:
                    sql = 'INSERT INTO `summary` (`chapter`, `bpid`, `sentences`) VALUES (%s, %s, %s)'
                    cursor.execute(sql, (chapter, summary['pid'], summary['content']))
                for match in matches:
                    sql = 'INSERT INTO `tuple` (`chapter`, `npid`, `sid`, `bpid`) VALUES (%s, %s, %s, %s)'
                    cursor.execute(sql, (chapter, match['npid'], match['sid'], match['pid']))
        connection.commit()
    except Exception as e:
        raise e
        print (e)
    finally:
        connection.close()
# # OM
# connection = pymysql.connect(host = 'localhost', user = 'root', password = '', db = 'notesum_om', charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
# try:
#     with connection.cursor() as cursor:
#         sql = 'INSERT INTO `book` (`chapter`, `bpid`, `content`) VALUES (%s, %s, %s)'
#         cursor.execute(sql, ('ch1', int('0'), 'Test!!! Haha~'))
#     connection.commit()
# finally:
#     connection.close()
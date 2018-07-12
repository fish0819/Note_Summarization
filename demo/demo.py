# -*- coding:utf-8 -*-
import os
import sys
import load_file as lf
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

subject_list = [{'subject': 'Operating Management', 'chapters': ['ch1', 'ch3', 'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12', 'ch15', 'ch16', 'supplementA']}, {'subject': 'Data Structure', 'chapters': ['ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch9']}]

class main_window(QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.subject_button_list = []
        self.chapter = self.topic = ''
        self.content_lable_list = [QLabel(), QLabel(), QLabel()] # slide, note, summary
        self.content_name_list = ['Slide', 'Note', 'Summary']
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setGeometry(300, 100, 1200, 900)
        self.setWindowTitle('Note Summary Demo')
        self.setWindowIcon(QIcon('pencil.png'))
        self.setup_subject_ui()
        self.win_layout = QVBoxLayout()
        self.win_layout.addWidget(self.subject_gb)
        self.setLayout(self.win_layout)

    def setup_subject_ui(self):
        self.subject_gb = QGroupBox('Subject')
        self.subject_gb.setFont(QFont('Georgia', 12))
        layout = QHBoxLayout()
        for sid in range(len(subject_list)):
            self.subject_button_list.append(QPushButton(subject_list[sid]['subject'], self))
            self.subject_button_list[sid].setMaximumWidth(300)
            self.subject_button_list[sid].setCheckable(True)
            self.subject_button_list[sid].setFont(QFont('微軟正黑體', 16))
            self.subject_button_list[sid].clicked.connect(self.onclick_subject)
            layout.addWidget(self.subject_button_list[sid])
        self.subject_gb.setLayout(layout)

    @pyqtSlot()
    def onclick_subject(self):
        for bid in range(len(self.subject_button_list)):
            if self.subject_button_list[bid].isChecked():
                self.subject = self.subject_button_list[bid].text()
                self.subject_abbr = ''.join([w[0] for w in self.subject.split()])
        self.subject_gb.deleteLater()
        self.subject_gb = None
        self.setup_note_ui()

    @pyqtSlot()
    def onclick_turnslide(self, button):
        tid = self.topic_cbbox.currentIndex()
        print ('tid:', tid, button.text())
        if tid == -1:
            QMessageBox.about(self, '!', 'Please choose the chapter first.')
        elif button.text() == 'Previous Slide':
            if tid == 0:
                QMessageBox.about(self, '!', 'No previous slide.')
            else:
                tid -= 1
                self.topic_cbbox.setCurrentIndex(tid)
        else:
            if tid == len(self.topics) - 1:
                QMessageBox.about(self, '!', 'No next slide.')
            else:
                tid += 1
                self.topic_cbbox.setCurrentIndex(tid)
        print ('tid:', tid)
        print (str(self.topic_cbbox.currentText()))
        self.display_content(str(self.topic_cbbox.currentText()))


    def setup_note_ui(self):
        for sid in range(len(subject_list)):
            if self.subject == subject_list[sid]['subject']:
                chapters = subject_list[sid]['chapters']
                break
        self.topic_gb = QGroupBox('Topic — ' + self.subject)
        self.topic_gb.setFont(QFont('Georgia', 12))
        topic_layout = QHBoxLayout()
        self.chapter_cbbox = QComboBox()
        self.chapter_cbbox.setFont(QFont('Calibri', 14))
        self.chapter_cbbox.addItems(chapters)
        self.chapter_cbbox.setCurrentIndex(-1)
        self.chapter_cbbox.activated[str].connect(self.select_chapter)

        self.topic_cbbox = QComboBox()
        self.topic_cbbox.setFont(QFont('Calibri', 14))
        self.topic_cbbox.activated[str].connect(self.select_topic)

        self.prev_button = QPushButton('Previous Slide')
        self.prev_button.setFont(QFont('Calibri', 14))
        self.prev_button.clicked.connect(lambda: self.onclick_turnslide(self.prev_button))
        self.next_button = QPushButton('Next Slide')
        self.next_button.setFont(QFont('Calibri', 14))
        self.next_button.clicked.connect(lambda: self.onclick_turnslide(self.next_button))

        topic_layout.addWidget(self.chapter_cbbox)
        topic_layout.addWidget(self.topic_cbbox)
        topic_layout.addWidget(self.prev_button)
        topic_layout.addWidget(self.next_button)
        self.topic_gb.setLayout(topic_layout)

        self.content_gb = QGroupBox()
        content_layout = QHBoxLayout()

        for i in range(len(self.content_lable_list)):
            gb = QGroupBox(self.content_name_list[i])
            gb.setFont(QFont('Georgia', 12))
            l = QVBoxLayout()
            self.content_lable_list[i].setMargin(10)
            self.content_lable_list[i].setFont(QFont('Candara', 14))
            self.content_lable_list[i].setAlignment(Qt.AlignTop)
            self.content_lable_list[i].setWordWrap(True)
            self.content_lable_list[i].setMaximumWidth(350)
            scroll_area = QScrollArea()
            scroll_area.setAutoFillBackground(True)
            p = scroll_area.palette()
            p.setColor(self.backgroundRole(), Qt.white)
            scroll_area.setPalette(p)
            scroll_area.setWidgetResizable(True)
            scroll_bar = scroll_area.verticalScrollBar()
            scroll_area.setWidget(self.content_lable_list[i])
            scroll_area.setMinimumSize(QSize(350, 750))
            l.addWidget(scroll_area)
            gb.setLayout(l)
            gb.setMinimumWidth(400)
            content_layout.addWidget(gb)
        self.content_gb.setLayout(content_layout)

        self.win_layout.addWidget(self.topic_gb)
        self.win_layout.addStretch(1)
        self.win_layout.addWidget(self.content_gb)
        self.win_layout.addStretch(19)
        self.setLayout(self.win_layout)

    def select_chapter(self, selected_text):
        self.chapter = selected_text
        print (self.subject_abbr, self.chapter)
        self.slides = lf.get_slides('ppt/' + self.subject_abbr + '/' + self.chapter + '_slides.csv')
        self.topics = [s['title'] for s in self.slides if s['title'] != '']
        self.topic_cbbox.clear()
        self.topic_cbbox.addItems(self.topics)
        self.topic_cbbox.setCurrentIndex(-1)
        self.matches = lf.get_matches('match/' + self.subject_abbr + '/NSBMatch_' + self.chapter + '.csv')
        self.summaries = lf.get_summaries('summary/' + self.subject_abbr + '/Summary_' + self.chapter + '.csv')
        self.spid_list = [s['pid'] for s in self.summaries]
        print (self.spid_list)
        print (len(self.spid_list), len(self.summaries))
        self.noteparas = lf.get_noteparas('note/' + self.subject_abbr + '/' + self.chapter + '/Mixed_' + self.chapter + '.csv')

    def select_topic(self, selected_text):
        self.display_content(selected_text)

    def display_content(self, selected_text):
        self.topic = selected_text
        sid = [s['title'] for s in self.slides].index(selected_text)
        npid_list = []
        pid_list = []
        for m in self.matches:
            if sid == m['sid']:
                npid_list.append(m['npid'])
                if m['pid'] != -1:
                    pid_list.append(m['pid'])
        npid_list = list(set(npid_list))
        pid_list = list(set(pid_list))
        self.content_lable_list[0].setText(self.slides[sid]['content'])
        note_text = ''
        for npid in npid_list:
            note_text += '\n'.join(self.noteparas[npid]) + '\n'
        note_text = note_text.strip('\n')
        self.content_lable_list[1].setText(note_text)
        summary_text = ''
        print (pid_list)
        if len(pid_list) > 0:
            for pid in pid_list:
                print (self.spid_list.index(pid))
                summary_text += self.summaries[self.spid_list.index(pid)]['content'] + '\n'
            summary_text = summary_text.strip('\n')
        self.content_lable_list[2].setText(summary_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    sys.exit(app.exec_())

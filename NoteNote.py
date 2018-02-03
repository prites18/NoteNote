#!/usr/bin/env python3
"""
Sticky Note app in python3 with PyQt5 GUI
Author: Pritesh Ranjan < pranjan341@gmail.com >
github: https://github.com/prites18/NoteNote
"""
import sys
import os
import random
import getpass

from PyQt5.QtWidgets import (QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint


class NoteNote(QWidget):
    """Sticky notes class containg all methods and attributes"""

    def __init__(self, notes_file, x, y) -> None:
        super(NoteNote, self).__init__()
        self.notes_file = notes_file
        self.color = self.bg_color()
        self.x = x
        self.y = y
        self.layout = QVBoxLayout()
        self.dmp_btn = QPushButton()
        self.title = QLabel("NoteNote")
        self.lck_btn = QPushButton()
        self.stk_btn = QPushButton()
        self.text = QTextEdit(self)
        self.init_ui()
        self.start = QPoint(0, 0)
        self.pressing = False
        self.stk_flag=False

    def init_ui(self):
        """sets the different UI elements"""
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        self.dmp_btn = QPushButton()
        self.dmp_btn.setFixedSize(30, 30)
        self.dmp_btn.setToolTip("Delete all notes")
        self.dmp_btn.setIcon(QIcon("icons/garbage.png"))
        self.dmp_btn.setStyleSheet("background-color: {}".format(self.color))
        self.dmp_btn.clicked.connect(self.dmp_act)
        self.title.setFixedHeight(30)
        self.title.setAlignment(Qt.AlignCenter)
        self.lck_btn = QPushButton()
        self.lck_btn.setFixedSize(30, 30)
        self.lck_btn.setToolTip("Protection off")
        self.lck_btn.setStyleSheet("background-color: {}".format(self.color))
        self.lck_btn.setIcon(QIcon("icons/unlock.png"))
        self.lck_btn.clicked.connect(lambda: self.lck_act(self.text.isReadOnly()))
        self.stk_btn = QPushButton()
        self.stk_btn.setFixedSize(30, 30)
        self.stk_btn.setToolTip("stick notes")
        self.stk_btn.setStyleSheet("background-color: {}".format(self.color))
        self.stk_btn.setIcon(QIcon("icons/pin.png"))
        self.stk_btn.clicked.connect(self.stk_act)
        h_layout.addWidget(self.dmp_btn)
        h_layout.addWidget(self.title)
        h_layout.addWidget(self.lck_btn)
        h_layout.addWidget(self.stk_btn)
        self.title.setStyleSheet("background-color: {}; color: black".format(self.color))
        self.layout.addLayout(h_layout)
        self.text.setContentsMargins(0, 0, 0, 0)
        self.text.setFont(QFont("Comic Sans MS", 13))
        self.text.setStyleSheet("background-color: {}".format(self.color))
        self.text.setText(self.saved_data)
        self.text.textChanged.connect(self.auto_save)
        self.layout.addWidget(self.text)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.setMinimumSize(100, 100)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(300, 300)

    def mousePressEvent(self, event):
        """detects if and when the title bar is held by mouse"""
        if self.stk_flag is False:
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True

    def mouseMoveEvent(self, event):
        """sets the window coordinates according to the mouse movement"""
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.width(),
                                self.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        """detects if the mose press is released"""
        self.pressing = False

    @property
    def saved_data(self) -> str:
        """ fetches the already stored notes and displays
        it in the text area"""
        if os.path.isfile(self.notes_file):
            with open(self.notes_file, "rb") as nf:
                data = nf.read()
                old_notes = data.decode("utf-8")
                return old_notes
        else:
            return " "

    def dmp_act(self) -> None:
        """reset sticky notes app"""
        open(self.notes_file, "wb").close
        self.text.setText("")
        sys.exit()

    def lck_act(self, text_disabled: bool) -> None:
        """toggle read only mode for textbox"""
        if text_disabled is True:
            self.text.setReadOnly(False)
            self.lck_btn.setIcon(QIcon("icons/unlock.png"))
            self.lck_btn.setToolTip("Protection off")
        else:
            self.text.setReadOnly(True)
            self.lck_btn.setIcon(QIcon("icons/lock.png"))
            self.lck_btn.setToolTip("Protection on")

    def auto_save(self) -> None:
        """ auto saves the text in the text area to a file as
        soon any data is inserted/deleted"""
        with open(self.notes_file, "wb") as nf:
            notes = self.text.toPlainText()
            nf.write(notes.encode("utf-8"))

    def stk_act(self) -> None:
        """stick notes"""
        self.stk_flag = not self.stk_flag
        if self.stk_flag:
            self.stk_btn.setIcon(QIcon("icons/unpin.png"))
            self.stk_btn.setToolTip("release")
        else:
           self.stk_btn.setIcon(QIcon("icons/pin.png"))
           self.stk_btn.setToolTip("stick notes")
               
    
    @staticmethod
    def bg_color() -> str:
        """ Returns a random colour from a list of intelligently choosen beautiful colours"""
        #list_of_colours = ["#F0F8FF", "#F0FFFF", "#F5F5DC", "#FFFAF0", "#F8F8FF",
         #                  "#DCDCDC", "#FFFFF0", "#F0E68C", "#E6E6FA", "#FFF0F5",
          #                 "#FFFACD", "#E0FFFF", "#FAFAD2", "#FFFFE0", "#FAF0E6",
           #                "#F5FFFA", "#FFE4E1", "#FFE4B5", "#FFEFD5", "#00ffbf"]
        #my_color = random.choice(list_of_colours)
        r1 = lambda: random.randint(200,255)
        r2 = lambda: random.randint(200,255)
        r3 = lambda: random.randint(150,255)
        return '#%02X%02X%02X' % (r1(),r2(),r3())
        #return my_color
       
    def main(self) -> None:
        """sets window properties and displays the gui"""
        self.setGeometry(self.x, self.y, 300, 300)
        self.setWindowIcon(QIcon("icons/letter-0.png"))
        self.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = getpass.getuser()
    path = "/home/"+user+"/.NoteNote/"
    if not os.path.exists(path):
            os.makedirs(path)
    NoteNote(path+"notes.bin", 1070, 0).main()
    sys.exit(app.exec_())

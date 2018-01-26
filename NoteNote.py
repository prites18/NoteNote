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
import glob

from PyQt5.QtWidgets import (QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt5.QtGui import QIcon, QFont
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
        self.new_btn = QPushButton()
        self.text = QTextEdit(self)
        self.init_ui()
        self.start = QPoint(0, 0)
        self.pressing = False

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
        self.lck_btn.setToolTip("Turn on Protection")
        self.lck_btn.setStyleSheet("background-color: {}".format(self.color))
        self.lck_btn.setIcon(QIcon("icons/lock.png"))
        self.lck_btn.clicked.connect(lambda: self.lck_act(self.text.isReadOnly()))
        self.new_btn = QPushButton()
        self.new_btn.setFixedSize(30, 30)
        self.new_btn.setToolTip("New notes")
        self.new_btn.setStyleSheet("background-color: {}".format(self.color))
        self.new_btn.setIcon(QIcon("icons/plus.png"))
        self.new_btn.clicked.connect(self.new_act)
        h_layout.addWidget(self.dmp_btn)
        h_layout.addWidget(self.title)
        h_layout.addWidget(self.lck_btn)
        h_layout.addWidget(self.new_btn)
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
        self.close()
        return True

    def lck_act(self, text_disabled: bool) -> None:
        """toggle read only mode for textbox"""
        if text_disabled is True:
            self.text.setReadOnly(False)
            self.lck_btn.setIcon(QIcon("icons/lock.png"))
            self.lck_btn.setToolTip("Turn on Protection")
        else:
            self.text.setReadOnly(True)
            self.lck_btn.setIcon(QIcon("icons/unlock.png"))
            self.lck_btn.setToolTip("Turn off Protection")

    def auto_save(self) -> None:
        """ auto saves the text in the text area to a file as
        soon any data is inserted/deleted"""
        with open(self.notes_file, "wb") as nf:
            notes = self.text.toPlainText()
            nf.write(notes.encode("utf-8"))

    def new_act(self) -> None:
        """open a new window"""
        AppManager().new_window(self.notes_file, self.x, self.y)

    
    @staticmethod
    def bg_color() -> str:
        """ Returns a random colour from a list of intelligently choosen beautiful colours"""
        list_of_colours = ["#F0F8FF", "#F0FFFF", "#F5F5DC", "#FFFAF0", "#F8F8FF",
                           "#DCDCDC", "#FFFFF0", "#F0E68C", "#E6E6FA", "#FFF0F5",
                           "#FFFACD", "#E0FFFF", "#FAFAD2", "#FFFFE0", "#FAF0E6",
                           "#F5FFFA", "#FFE4E1", "#FFE4B5", "#FFEFD5", "#00ffbf"]
        my_color = random.choice(list_of_colours)
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
        return True


class AppManager:
    """ Manages the window instances and loads the required data and programs at startup"""
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.req_wind = len(glob.glob1("./", "*.bin"))
        self.notes_files = glob.glob("*.bin")
        self.user = getpass.getuser()
        self.path = "/home/"+self.user+"/.NoteNote/"
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def startup(self) -> None:
        """ called when the app is restarted or opened for the first time"""
        if self.req_wind != 0:
            for file in self.notes_files:
                NoteNote(self.path+file, 1070, 0).main()
        else:
            NoteNote(self.path+"1.bin", 1070, 0).main()
        sys.exit(self.app.exec_())


    def new_window(self, notes_file, x, y) -> None:
        """ to initialize a new window"""
        seq_range = "0123456789"
        seq = int(''.join([inte for inte in notes_file if inte in seq_range]))
        seq += 1
        new_file = "{}.bin".format(seq)
        NoteNote(self.path+new_file, x, y+310).main()



if __name__ == "__main__":
    AppManager().startup()


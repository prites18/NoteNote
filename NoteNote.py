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
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class NoteNote(QWidget):
    """Sticky notes class containg all methods and attributes"""

    def __init__(self, notes_file) -> None:
        super(NoteNote, self).__init__()
        self.notes_file = notes_file
        self.title = QLabel()
        self.title.setText("NoteNote")
        self.text = QTextEdit(self)
        self.text.setFont(QFont("Comic Sans MS", 13))
        self.text.setStyleSheet("background-color: {}".format(self.bg_color()))
        self.text.textChanged.connect(self.auto_save)
        self.dmp_btn = QPushButton()
        self.dmp_btn.setToolTip("Delete all notes")
        self.dmp_btn.setIcon(QIcon("icons/garbage.png"))
        self.lck_btn = QPushButton()
        self.lck_btn.setToolTip("Turn on Protection")
        self.lck_btn.setIcon(QIcon("icons/lock.png"))
        #self.pin_btn = QPushButton("PIN")
        self.gen_ui()

    def gen_ui(self) -> None:
        """generates the GUI design; adds buttons and other
           other widgets to the layout """
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.dmp_btn)
        h_layout.addSpacing(50)
        h_layout.addWidget(self.title)
        h_layout.addSpacing(50)
        h_layout.addWidget(self.lck_btn)
        #h_layout.addWidget(self.pin_btn)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.text)
        self.dmp_btn.clicked.connect(self.dmp_act)
        self.lck_btn.clicked.connect(lambda: self.lck_act(self.text.isReadOnly()))
        #self.pin_btn.clicked.connect(self.pin_act)
        self.setLayout(v_layout)
        self.text.setText(self.saved_data)

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
        sys.exit(0)

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

    def pin_act(self) -> None:
        """yet to be implemented"""
        pass

    @staticmethod
    def bg_color() -> str:
        """ Returns a random colour from a list of intelligently choosen beautiful colours"""
        list_of_colours = ["#F0F8FF", "#F0FFFF", "#F5F5DC", "#FFFAF0", "#F8F8FF",
                           "#DCDCDC", "#FFFFF0", "#F0E68C", "#E6E6FA", "#FFF0F5",
                           "#FFFACD", "#E0FFFF", "#FAFAD2", "#FFFFE0", "#FAF0E6",
                           "#F5FFFA", "#FFE4E1", "#FFE4B5", "#FFEFD5", "#00ffbf"]
        my_color = random.choice(list_of_colours)
        return my_color

    def main(self) -> None:
        """sets window properties and displays the gui"""
        self.setGeometry(1070, 0, 300, 300)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(300, 300)
        self.setWindowIcon(QIcon("icons/letter-0.png"))
        self.show()

if __name__ == "__main__":
    USER = getpass.getuser()
    PATH = "/home/"+USER+"/.NoteNote/"
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    APP = QApplication(sys.argv)
    NOTES_APP = NoteNote(PATH+"notes.bin").main()
    sys.exit(APP.exec_())

"""
Sticky Note app in python3 with PyQt5 GUI
Author: Pritesh Ranjan < pranjan341@gmail.com >
github: https://github.com/prites18/NoteNote
"""
import sys
import os
import random
import datetime

from PyQt5.QtWidgets import (QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QIcon, QFont

class NoteNote(QWidget):
    """Sticky notes class containg all methods and attributes"""

    def __init__(self, notes_file="notes.bin") -> None:
        super(NoteNote, self).__init__()
        self.notes_file = notes_file
        self.text = QTextEdit(self)
        self.text.setFont(QFont("Comic Sans MS", 13))
        self.text.setStyleSheet("background-color: {}".format(self.bg_color()))
        self.text.textChanged.connect(self.auto_save)
        self.dmp_btn = QPushButton()
        self.dmp_btn.setIcon(QIcon("icons/garbage.png"))
        self.lck_btn = QPushButton()
        self.lck_btn.setIcon(QIcon("icons/lock.png"))
        #self.pin_btn = QPushButton("PIN")
        self.gen_ui()

    def gen_ui(self) -> None:
        """generates the GUI design; adds buttons and other
           other widgets to the layout """
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.dmp_btn)
        h_layout.addSpacing(200)
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
        else:
            self.text.setReadOnly(True)
            self.lck_btn.setIcon(QIcon("icons/unlock.png"))

    def auto_save(self) -> None:
        """ auto saves the text in the text area to a file as
        soon any data is inserted/deleted"""
        with open(self.notes_file, "wb") as nf:
            notes = self.text.toPlainText()
            nf.write(notes.encode("utf-8"))

    def pin_act(self) -> None:
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

    @staticmethod
    def curr_date() -> str:
        """ Returns current data in dd-mm-yyyy format"""
        date_data = datetime.datetime.today().strftime("%d-%m-%Y")
        return date_data

    def main(self) -> None:
        """sets window properties and display the gui"""
        self.setGeometry(1070, 0, 300, 300)
        self.setFixedSize(300, 300)
        self.setWindowTitle("Sticky Notes {}".format(self.curr_date()))
        self.setWindowIcon(QIcon("icons/letter-0.png"))
        self.show()


my_app = QApplication(sys.argv)
note_app = NoteNote().main()
sys.exit(my_app.exec_())

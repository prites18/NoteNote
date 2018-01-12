""" coding=UTF8
NoteNote sticky note app in python3 with Tk GUI
Author: Pritesh Ranjan <pranjan341@gmail.com> """

import os
import datetime
from tkinter import *

class NoteNote:
    """NoteNote app is designed and implemented in this class"""
    def __init__(self):
        HEIGHT = 400
        WIDTH = 300
        self.notes = ""
        self.notes_file = "notes.bin"
        self.app = Tk()
        self.app.title("NoteNote:  {}".format(self.curr_date()))
        self.app.resizable(False, False)
        frame = Frame(self.app)
        frame.pack()
        frame.config(height=HEIGHT, width=WIDTH)
        self.text_area = Text(frame, height=23, width=45, bg="yellow")
        self.text_area.pack()
        self.text_area.insert(INSERT, self.get_data())
        self.app.bind("<Key>", self.autosave)
        self.app.mainloop()

    def autosave(self, event):
        """ auto saves the text in the text area to a file as
        soon any data is inserted"""
        with open("notes.bin", "wb") as my_file:
            self.notes = self.text_area.get(0.0, END)
            my_file.write(self.notes.encode("utf-8"))

    def get_data(self):
        """ fetches the already stored notes and displays
        it in the text area at boot"""
        if os.path.isfile(self.notes_file):
            with open(self.notes_file, "rb") as my_file:
                data = my_file.read()
                old_notes = data.decode('utf-8')
                return old_notes
        else:
            return " "

    @staticmethod
    def curr_date():
        date_data = datetime.datetime.today().strftime('%Y-%m-%d')
        return date_data+"\n"


NoteNote()

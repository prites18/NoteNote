""" 
coding=UTF8
NoteNote sticky note app in python3 with Tk GUI
Author: Pritesh Ranjan < pranjan341@gmail.com >
github: https://github.com/prites18/NoteNote
"""

import os
import datetime
import random
import glob
from tkinter import END, Tk, Frame, Text, INSERT, PhotoImage, WORD

class NoteNote:
    """NoteNote app is designed and implemented in this class"""

    def __init__(self, notes_file="notes.bin", app_title="NoteNote") -> None:
        self.notes = ""
        self.notes_file = notes_file
        self.app = Tk()
        img = PhotoImage(file="letter-n.gif")
        self.app.tk.call("wm", "iconphoto", self.app._w, img)
        self.app.font = "Comic Sans MS"
        self.app.title(app_title + ": {}".format(self.curr_date()))
        self.app.resizable(False, False)
        frame = Frame(self.app)
        frame.pack()
        frame.config(height=400, width=300)
        self.text_area = Text(frame, height=18, width=30, bg=self.bg_color, wrap=WORD, font=45)
        self.text_area.pack()
        self.text_area.insert(INSERT, self.get_data())
        self.app.bind("<Key>", self.autosave)

    def autosave(self, event) -> None:
        """ auto saves the text in the text area to a file as
        soon any data is inserted"""

        with open("notes.bin", "wb") as my_file:
            self.notes = self.text_area.get(0.0, END)
            my_file.write(self.notes.encode("utf-8"))

    def get_data(self) -> str:
        """ fetches the already stored notes and displays
        it in the text area at boot"""
        if os.path.isfile(self.notes_file):
            with open(self.notes_file, "rb") as my_file:
                data = my_file.read()
                old_notes = data.decode("utf-8")
                return old_notes
        else:
            return " "

    @property
    def bg_color(self) -> str:
        """ Returns a random colour from a list of intelligently choosen beautiful colours"""

        list_of_colours = ["#F0F8FF", "#F0FFFF", "#F5F5DC", "#FFFAF0", "#F8F8FF",
                           "#DCDCDC", "#FFFFF0", "#F0E68C", "#E6E6FA", "#FFF0F5",
                           "#FFFACD", "#E0FFFF", "#FAFAD2", "#FFFFE0", "#FAF0E6",
                           "#F5FFFA", "#FFE4E1", "#FFE4B5", "#FFEFD5", "#00ffbf"]
        my_color = random.choice(list_of_colours)
        return my_color

    @staticmethod
    def curr_date() -> str:
        """ Returns current data in yyyy-mm-dd format"""

        date_data = datetime.datetime.today().strftime("%Y-%m-%d")
        return date_data

    def main(self) -> None:
        """display the gui"""

        self.app.mainloop()



class AppManager:
    """ Manages the window instances and loads the required data and programs at startup"""
    def __init__(self) -> None:
        self.req_wind = len(glob.glob1("./", "*.bin"))
        self.note_files = glob.glob("*.bin")

    def startup(self) -> None:
        """ called when the app is restarted or opened for the first time"""
        for file in self.note_files:
            NoteNote(notes_file=file).main()

    def new_window(self) -> None:
        """ to initialize a new window"""
        pass

if __name__ == "__main__":
    AppManager().startup()

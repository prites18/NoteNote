#!/bin/bash
echo "installing dependencies via apt package manager"
sudo apt-get install python3-pyqt5
chmod u+x NoteNote.py
sudo install NoteNote.py /usr/local/bin/NoteNote
mkdir ~/.NoteNote
cp icons/ ~/.NoteNote
cd ~/.NoteNote
echo "[Desktop Entry]" > NoteNote.desktop
echo "Version=1.0" >> NoteNote.desktop
echo "Name=NoteNote" >> NoteNote.desktop
echo "Comment="NoteNote Sticky Notes"" >> NoteNote.desktop
echo "Exec=NoteNote" >> NoteNote.desktop
echo "Path=/home/prites/projects/NoteNote/" >> NoteNote.desktop
echo "Icon=/home/prites/projects/NoteNote/icons/letter-2.gif" >> NoteNote.desktop
echo "Terminal=false" >> NoteNote.desktop
echo "Type=Application" >> NoteNote.desktop
echo "Categories=Utility;" >> NoteNote.desktop
cp NoteNote.desktop ~/.local/share/applications
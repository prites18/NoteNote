#!/bin/bash


#make sure this script wasn't started as 'sh install.sh' or similar.
if [ "x$BASH" = "x" ]; then
    echo "\033[0;31m Should be started as 'bash install.sh'"
    exit 1;
fi

# error function called when ever something important fails to execute.
error()
{
	echo -e "\033[0;31m Oops! ERROR: " ${1}
	echo ""
	echo ""
	echo -e '\033[0;31m Please check if you have a working internet connection and you are  authorised  to install programs in this system \e[0m'

	kill "$!"
	exit 1
}

# to check for a stable internet connection
chk_internet_connection() 
{
	ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` 2> /dev/null && echo "Internet is working" || error "No internet"
}

# spinner animation while something runs in the background
spinner()
{
	local i sp n
    echo ' '
    sp='  /-\|'
    n=${#sp}
    printf ' '
    while sleep 0.1; do
        printf "%s\b" "${sp:i++%n:1}"
    done
}

chk_internet_connection || error "NO Internet connection; cannot download dependencies"
echo "installing dependencies via apt package manager"
sudo apt-get install python3-pyqt5
spinner &
mkdir -p ~/.NoteNote
cp ./* ~/.NoteNote
cd ~/.NoteNote

chmod u+x NoteNote.py
chmod u+x NoteNote
sudo install NoteNote /usr/local/bin/NoteNote
sudo cp NoteNote /etc/init.d/

echo "[Desktop Entry]" > NoteNote.desktop
echo "Version=1.0" >> NoteNote.desktop
echo "Name=NoteNote" >> NoteNote.desktop
echo "Comment="NoteNote Sticky Notes"" >> NoteNote.desktop
echo "Exec=NoteNote" >> NoteNote.desktop
echo "Path=/home/${USER}/.NoteNote/" >> NoteNote.desktop
echo "Icon=/home/${USER}/.NoteNote/icons/letter-2.gif" >> NoteNote.desktop
echo "Terminal=false" >> NoteNote.desktop
echo "Type=Application" >> NoteNote.desktop
echo "Categories=Utility;" >> NoteNote.desktop
cp NoteNote.desktop ~/.local/share/applications
kill "$!"
clear
echo "NoteNote installed successfully"
notify-send "NoteNote installed successfully"

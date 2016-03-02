![SoundRain Logo](resources/soundrainlogo.jpg)


# Soundrain
---

### What is it ?

SoundRain is a OS X (for now) app letting you to download Soundcloud music.
You just have to give it the URL !

### Why does SoundRain ask me at the beginning about a 'client ID' ?

SoundRain will ask only once about your client ID, you have to provide it to him
so it can DL your music :)

##### How do i find my 'client ID' ?

* Go at this [page](http://soundcloud.com/you/apps).
* Click on **Register a new application**.
* Enter a name (type anything, it won't matter).
* Copy/Paste your **Client ID** into the SoundRain app.

---

### How to download music ?

* Copy/Paste the URL of your music
* Click on **Search**
* (Optional): Edit music tags
* Make it rain baby !

---

### README

If you like the music, support the artist ! Buy its music !:)

---

### How to use it

You'll need module from requirements.txt plus pyqt5 and sip.
* `pip install -r requirements.txt`

if using OSX and Homebrew:
* `brew install sip`
* `brew install pyqt5`
Else use your favorite package manager (as pyqt and sip aren't available on pip):

To launch it in CLI:
`python3 SoundRain.py`

---

### TODO List

- [X] GUI.
- [X] Can download single music.
- [X] Ask at first start for the 'client ID'.
- [ ] InApp tutorial | Web tutorial.
- [X] Can download playlist.
- [X] Can download likes.
- [ ] Add shortcut.
- [ ] Split code for GUI and Downloader into two different files (I'm laaazy).
- [ ] Add a link to place where you can buy artist's music.

---

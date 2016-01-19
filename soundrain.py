"""
    This python script create a GUI allowing to download a Soundcloud music
    Made by BoBibelo
"""

# Native import
import sys
import os
import re
# PyQt5 imports
from PyQt5.QtWidgets    import (QApplication,  QWidget,        QDesktopWidget,
                                QMainWindow,   QAction,        qApp,
                                QTextEdit,     QHBoxLayout,    QVBoxLayout,
                                QLabel,        QLineEdit,      QPushButton,
                                QFrame,        QFileDialog,    QMessageBox,
                                QInputDialog,  QErrorMessage,  QDialog)
from PyQt5.QtGui        import  QPixmap,       QIcon
from PyQt5.QtCore       import (QSettings,     QObject,        pyqtSignal,
                                pyqtSlot,      Qt)
#import module for soundcloud, music handling, and file downloading
import soundcloud
import urllib
import httplib2
import requests
from mutagen.mp3        import  MP3,           EasyMP3
from mutagen.id3        import  ID3,           APIC

class WindowSR(QMainWindow):
    """Main window of SoundRain"""

    bad_id = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initWin()
        self.init_client_id()

    def initWin(self):
        """Create main parts of the window"""

        # Main Window
        self.setFixedSize(900, 500)
        self.center()
        self.setWindowTitle("SoundRain")
        self.setWindowIcon(QIcon('resources/soundrainlogo.jpg'))

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # QVBox stocking every row
        self.vertical_grid = QVBoxLayout()

        # First row: URL request
        row_url   = QHBoxLayout()
        label_url = QLabel("URL:", self)
        self.text_url  = QLineEdit(self)
        self.but_url   = QPushButton("Search", self)
        self.but_url.clicked.connect(self.check_url)
        row_url.addWidget(label_url)
        row_url.addWidget(self.text_url)
        row_url.addWidget(self.but_url)

        # Row of separation 1
        row_sep1 = QHBoxLayout()
        line_sep = QFrame()
        line_sep.setFrameShape(QFrame.HLine)
        row_sep1.addWidget(line_sep)

        # Second row (splitted screen between cover image and music info): 
        row_split  = QHBoxLayout()
        # Cover image
        column_image = QVBoxLayout()
        self.label_image  = QLabel(self)
        self.label_image.setMaximumHeight(280)
        self.label_image.setMinimumHeight(280)
        self.label_image.setMaximumWidth(280)
        self.label_image.setMinimumHeight(280)
        self.cover = QPixmap(280, 280)
        self.cover.load("resources/unknownperson.jpg")
        self.label_image.setPixmap(self.cover)
        column_image.addWidget(self.label_image)
        # music info
        column_info  = QVBoxLayout()
        label_name   = QLabel("Name", self)
        self.name    = QLineEdit(self)
        label_artist = QLabel("Artist", self)
        self.artist  = QLineEdit(self)
        label_album  = QLabel("Album", self)
        self.album   = QLineEdit(self)
        label_genre  = QLabel("Genre", self)
        self.genre   = QLineEdit(self)
        # --
        column_info.addWidget(label_name)
        column_info.addWidget(self.name)
        column_info.addWidget(label_artist)
        column_info.addWidget(self.artist)
        column_info.addWidget(label_album)
        column_info.addWidget(self.album)
        column_info.addWidget(label_genre)
        column_info.addWidget(self.genre)
        # --
        row_split.addLayout(column_image)
        row_split.addLayout(column_info)

        # Row of separation 2
        row_sep2  = QHBoxLayout()
        line_sep2 = QFrame()
        line_sep2.setFrameShape(QFrame.HLine)
        row_sep2.addWidget(line_sep2)

        # Add the file location selection row
        row_file       = QHBoxLayout()
        self.but_file  = QPushButton("Save location", self)
        self.but_file.clicked.connect(self.open_f)
        self.text_file = QLineEdit(self.default_path(), self)
        row_file.addWidget(self.but_file)
        row_file.addWidget(self.text_file)

        # Row of separation 3
        row_sep3  = QHBoxLayout()
        line_sep3 = QFrame()
        line_sep3.setFrameShape(QFrame.HLine)
        row_sep3.addWidget(line_sep3)

        # Download button row
        row_dl      = QHBoxLayout()
        row_dl.addStretch(1)
        self.but_dl = QPushButton("Make it rain !", self)
        self.but_dl.clicked.connect(self.manage_download)
        row_dl.addWidget(self.but_dl)

        # Add every row to the vertical grid
        self.vertical_grid.addLayout(row_url)
        self.vertical_grid.addLayout(row_sep1)
        self.vertical_grid.addLayout(row_split)
        self.vertical_grid.addLayout(row_sep2)
        self.vertical_grid.addLayout(row_file)
        self.vertical_grid.addLayout(row_sep3)
        self.vertical_grid.addLayout(row_dl)

        # Set layout of the vertical grid to the central widget
        self.central_widget.setLayout(self.vertical_grid)

        self.show()

    def init_client_id(self):
        """Ask for client id if it as never been entered, else load it from
        register with QSettings"""

        self.client_id = None
        self.setting   = QSettings(QSettings.UserScope, "BoBibelo",
                                   "SoundRain", self)
        if not self.setting.value("SR_bool"): # Setting never set
            self.client_id_box()
            self.setting.setValue("SR_bool", True)
            self.setting.setValue("SR_id", self.client_id)
        else:
            self.client_id = self.setting.value("SR_id")
        self.client = soundcloud.Client(client_id=self.client_id)

    def client_id_box(self):
        """Generate the client id box"""

        self.client_id_bo = QDialog(self)
        self.client_id_bo.setFixedSize(400, 200)
        self.client_id_bo.setModal(True)

        client_id_grid = QVBoxLayout()
        label_request  = QLabel("Enter your Soundcloud Client ID:", self.client_id_bo)
        self.input_id  = QLineEdit(self.client_id_bo)
        label_help     = QLabel("<a href=\"http://bobibelo.github.io/soundrain/help.html\">Need help ?</a>",
                                self.client_id_bo)
        label_help.setTextFormat(Qt.RichText);
        label_help.setTextInteractionFlags(Qt.TextBrowserInteraction);
        label_help.setOpenExternalLinks(True);

        self.got_id = False
        button_cancel = QPushButton("Cancel", self.client_id_bo)
        button_cancel.clicked.connect(self.reject_id)
        button_accept = QPushButton("Ok", self.client_id_bo)
        button_accept.clicked.connect(self.get_id)
        button_grid   = QHBoxLayout()
        button_grid.addStretch(1)
        button_grid.addWidget(button_cancel)
        button_grid.addWidget(button_accept)

        client_id_grid.addWidget(label_request)
        client_id_grid.addWidget(self.input_id)
        client_id_grid.addWidget(label_help)
        client_id_grid.addLayout(button_grid)
        self.client_id_bo.setLayout(client_id_grid)

        self.client_id_bo.rejected.connect(self.reject_id)
        self.client_id_bo.exec_()

    def get_id(self):
        """Get client id from the qdialog"""

        self.client_id = self.input_id.text().strip()
        if len(self.client_id) != 0:
            self.got_id = True
            self.client_id_bo.close()

    def reject_id(self):
        """Quit app after user not giving client id"""

        if not self.got_id:
            self.close()
            sys.exit(1)

    def open_f(self):
        """Choose the directory where to save music"""

        self.dirname = QFileDialog.getExistingDirectory()
        if self.dirname and len(self.dirname) > 0:
            self.text_file.setText(self.dirname)

    def center(self):
        """Places window in the screen's center"""

        center_geo = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        center_geo.moveCenter(center_pos)
        self.move(center_geo.topLeft())

    def check_url(self):
        """Test if the music url is correct and if so fill info"""

        url_pattern = "^https?://(www\.)?soundcloud\.com"
        if not re.match(url_pattern, self.text_url.text()):
            QMessageBox.about(self, "Invalid URL",
                              "The requested URL is invalid: %s" % self.text_url.text())
        else:
            if "/sets/" in self.text_url.text(): # Is playlist
                self.artist.setText("Not available for playlist.")
                self.name.setText("Not available for playlist.")
                self.disable_input()
            else:
                self.enable_input()
            self.get_music_info()

    def disable_input(self):
        """Disable artist, and name in case of playlist"""

        self.is_playlist = True
        self.artist.setDisabled(True)
        self.name.setDisabled(True)

    def enable_input(self):
        """Enable artist, and name after a playlist"""

        self.is_playlist = False
        self.artist.setDisabled(False)
        self.name.setDisabled(False)

    def get_track(self):
        """Returns track"""
       
        http_page = httplib2.Http()
        resp = http_page.request(self.url_str, "HEAD")
        if int(resp[0]["status"]) >= 400:
            QMessageBox.about(self,
                              "Error URL",
                              "URL doesn't exist.")
            return False

        try:
            self.track = self.client.get("/resolve", url=self.url_str)
        except:
            self.setting.setValue("SR_bool", False)
            self.init_client_id()
            self.get_track()

        return True

    def get_music_info(self):
        """Get music info, which will be stocked in self.track, and fill info"""

        self.url_str = self.text_url.text()
        if not self.get_track():
            return

        if not self.is_playlist:
            self.artist.setText(self.track.user['username'])
            self.name.setText(self.track.title)
            self.image = requests.get(self.modifiy_image_size()).content
            self.cover.loadFromData(self.image)
            self.cover = self.cover.scaledToWidth(280)
            self.label_image.setPixmap(self.cover)
        else:
            # Get the last part of URL ( == to playlist name)
            self.album.setText(self.text_url.text().rsplit('/', 1)[-1])
        self.genre.setText(self.track.genre)

    def modifiy_image_size(self):
        """Change artwork_url so the image can (potentially) look better"""

        artwork_url = self.track.artwork_url
        if "large" in artwork_url:
            return artwork_url.replace("large", "t500x500")
        else:
            return artwork_url

    def manage_download(self):
        """Manage download in case of playlist"""

        if self.is_playlist:
            playlist = self.client.get('/playlists/%s' % (self.track.id))
            for song_url in playlist.tracks:
                self.url_str = song_url["permalink_url"]
                self.get_track()
                self.image = requests.get(self.modifiy_image_size()).content
                self.download()
            self.success_box() # Success box for playlist
            self.enable_input()
        else:
            self.download()
            self.success_box() # Succes box for single song

    def download(self):
        """Try to download a single song"""
        try:
            self.fi_mp3, headers = urllib.request.urlretrieve(self.create_url(),
                                                              self.create_filename())
        except:
            QMessageBox.about(self, "Error Download",
                              "Download failed for song: %s" % self.track.title)
            return False

        self.add_tags()
        return True

    def add_tags(self):
        """Add artists name, music name, album, genre, and cover"""

        # Set artist name, music name, album, and genre
        audio_file = EasyMP3(self.fi_mp3)
        audio_file.tags = None
        if self.is_playlist:
            audio_file["artist"] = self.track.user["username"]
            audio_file["title"]  = self.track.title
        else:
            audio_file["artist"] = self.artist.text()
            audio_file["title"]  = self.name.text()
        audio_file["genre"]  = self.genre.text()
        audio_file["album"]  = self.album.text()
        audio_file.save()

        # Determine the mime
        artwork_url = self.modifiy_image_size()
        mime = "image/jpeg"
        if ".png" in artwork_url:
            mime = "image/png"

        # Set cover
        audio_file = MP3(self.fi_mp3, ID3=ID3)
        audio_file.tags.add(
                APIC(
                    encoding=3,
                    mime=mime,
                    type=3,
                    desc="Cover",
                    data=self.image
                )
        )
        audio_file.save()

    def success_box(self):
        """Display a sucess box"""

        if self.is_playlist:
            QMessageBox.about(self, "Success",
                              "%s playlist have just been download right into %s"
                              % (self.text_url.text().rsplit('/', 1)[-1], self.text_file.text()))
        else:
            QMessageBox.about(self, "Success",
                              "%s have just been download right into %s"
                              % (self.name.text(), self.text_file.text()))

    def create_url(self):
        url_str = "http://api.soundcloud.com/tracks/%s/stream?client_id=%s" % (self.track.id, self.client_id)
        return url_str

    def create_filename(self):
        path = self.text_file.text()
        name = self.track.title + ".mp3"
        fi_str  = os.path.join(path, name)
        return fi_str

    def default_path(self):
        """Set the default path"""

        list_user = os.listdir("/Users")
        for user in list_user:
            if user != "Shared" and user != ".localized":
                break
        else:
            user = "Shared"

        path = "/Users/" + user + "/Music"
        return path

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = WindowSR()
    sys.exit(app.exec_())

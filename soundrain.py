import sys
import re
from PyQt5.QtWidgets    import (QApplication,  QWidget,        QDesktopWidget,
                                QMainWindow,   QAction,        qApp,
                                QTextEdit,     QHBoxLayout,    QVBoxLayout,
                                QLabel,        QLineEdit,      QPushButton,
                                QFrame,        QFileDialog,    QMessageBox)
from PyQt5.QtGui        import (QPixmap)

class WindowSR(QMainWindow):
    """Main window of SoundRain"""

    def __init__(self):
        super().__init__()
        self.initWin()

    def initWin(self):
        """Create main parts of the window"""

        # Main Window
        self.resize(400, 500)
        self.center()
        self.setWindowTitle("SoundRain")
       
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
        label_image  = QLabel(self)
        self.cover = QPixmap(200, 200)
        label_image.setPixmap(self.cover)
        column_image.addWidget(label_image)
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
        self.text_file = QLineEdit("~/", self)
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

    def open_f(self):
        self.dirname = QFileDialog.getExistingDirectory()
        print (self.dirname)
        self.text_file.setText(self.dirname)

    def center(self):
        """Places window in the screen's center"""

        center_geo = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        center_geo.moveCenter(center_pos)
        self.move(center_geo.topLeft())

    def check_url(self):
        url_pattern = "^https?://(www\.)?soundcloud\.com"
        if re.match(url_pattern, self.text_url.text()):
            print ("cool")
        else:
            QMessageBox.about(self, "Invalid URL",
                              "The requested URL is invalid: %s" % self.text_url.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex  = WindowSR()
    sys.exit(app.exec_())



from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys


def pushed_my_button():
    print("Pressed it")


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        button = QPushButton("Hello")
        button.pressed.connect(pushed_my_button)

        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()



app.exec_()



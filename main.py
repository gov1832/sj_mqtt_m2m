import logging
import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from funtion_class import funtion_class
from drawclass_file import drawclass
import ssl

class mainClass(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("mqtt_hbrain_m2m.ui", self)

        self.hbrain_logo = QPixmap("icon/hbrain_logo.png")
        self.hbrain_logo = self.hbrain_logo.scaled(220, 50)
        self.ui.logo_image.setPixmap(self.hbrain_logo)
        self.setWindowIcon(QIcon("icon/hbrain.png"))

        self.uc = funtion_class(self.ui)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    myWindow = mainClass()

    myWindow.show()

    app.exec_()

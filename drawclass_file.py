from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget

class drawclass(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        global ev_y, robot_x, robot_y, door_open
        self.setGeometry(1470, 30, 950, 970)
        self.ev_x = 650
        self.ev_w = 100
        self.ev_h = 100
        self.robot_w = 60
        self.robot_h = 30
        ev_y = 800
        robot_x = 300
        robot_y = 850
        door_open = False

    def paintEvent(self, event):
        global ev_y, robot_x, robot_y, door_open
        qp = QPainter()
        qp.begin(self)
        self.drawOther(qp)
        self.drawEV(qp, self.ev_x, ev_y, self.ev_w, self.ev_h)
        self.drawRobot(qp, robot_x, robot_y, self.robot_w, self.robot_h)

        if door_open:
            self.drawEVdoor(qp, self.ev_x - 50, ev_y, self.ev_w / 2, self.ev_h)
            self.drawEVdoor(qp, self.ev_x + 100, ev_y, self.ev_w / 2, self.ev_h)
        else:
            self.drawEVdoor(qp, self.ev_x, ev_y, self.ev_w / 2, self.ev_h)
            self.drawEVdoor(qp, self.ev_x + 50, ev_y, self.ev_w / 2, self.ev_h)

        qp.end()
        self.update()

    def drawEV(self, qp, x, y, w, h):
        qp.setPen(QPen(Qt.black, 5))
        qp.drawRect(x, y, w, h)

    def drawEVdoor(self, qp, x, y, w, h):
        qp.setPen(QPen(QColor(254, 196, 0)))
        qp.setBrush(Qt.Dense6Pattern)
        qp.drawRect(x, y, w, h)
        qp.fillRect(x, y, w, h, QBrush(QColor(254, 196, 0), Qt.BDiagPattern))

    def drawRobot(self, qp, x, y, w, h):
        # body
        qp.setPen(QPen(QColor(0, 208, 255), 2))
        qp.drawRect(x, y, w, h)
        qp.fillRect(x, y, w, h, QBrush(QColor(0, 208, 255), Qt.Dense2Pattern))
        qp.setPen(QPen(Qt.white, 2))
        qp.drawRect(x, y+h, w, h/2)
        qp.fillRect(x, y+h, w, h/2, QBrush(Qt.white, Qt.Dense2Pattern))
        # ellipse
        qp.setPen(QPen(Qt.black, 2))
        qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        qp.drawEllipse(x + w/8, y + (h*1.5) - w/8, w/4, w/4)
        qp.drawEllipse(x+ (w/8)*5, y + (h*1.5) - w/8, w/4, w/4)

    def drawOther(self, qp):
        qp.setPen(QPen(Qt.gray, 3, Qt.DashLine))
        qp.drawLine(100, 0, 800, 0)
        qp.drawLine(100, 100, 800, 100)
        qp.drawLine(100, 200, 800, 200)
        qp.drawLine(100, 300, 800, 300)
        qp.drawLine(100, 400, 800, 400)
        qp.drawLine(100, 500, 800, 500)
        qp.drawLine(100, 600, 800, 600)
        qp.drawLine(100, 700, 800, 700)
        qp.drawLine(100, 800, 800, 800)
        qp.drawLine(100, 900, 800, 900)

        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.drawLine(600, 0, 800, 0)
        qp.drawLine(600, 100, 800, 100)
        qp.drawLine(600, 200, 800, 200)
        qp.drawLine(600, 300, 800, 300)
        qp.drawLine(600, 400, 800, 400)
        qp.drawLine(600, 500, 800, 500)
        qp.drawLine(600, 600, 800, 600)
        qp.drawLine(600, 700, 800, 700)
        qp.drawLine(600, 800, 800, 800)
        qp.drawLine(600, 900, 800, 900)

        qp.setFont(QFont('Arial', 16))
        qp.drawText(820, 30, '9F')
        qp.drawText(820, 130, '8F')
        qp.drawText(820, 230, '7F')
        qp.drawText(820, 330, '6F')
        qp.drawText(820, 430, '5F')
        qp.drawText(820, 530, '4F')
        qp.drawText(820, 630, '3F')
        qp.drawText(820, 730, '2F')
        qp.drawText(820, 830, '1F')

    def get_EVData(self, now_floor, now_door, now_arrival):
        global ev_y, door_open
        ev_y = 900 - 100 * now_floor
        if now_door == "open":
            door_open = True
        elif now_door == "opening":
            door_open = True
        elif now_door == "close":
            door_open = False
        elif now_door == "closing":
            door_open = False

    def get_RobotData(self, now_state, now_floor):
        global robot_x, robot_y
        if now_state == 1:
            robot_x = 675
            robot_y = 950 - 100 * now_floor
        elif now_state == 4:
            robot_x = 300




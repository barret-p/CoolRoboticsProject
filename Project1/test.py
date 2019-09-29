# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import math

class Link:
    def __init__(self, length, origin, theta, xdir, ydir):
        self.length = length
        self.origin = origin
        self.theta = theta
        self.xdir = xdir
        self.ydir = ydir
        self.endpoint = self.get_endpoint()

    def vectorLength(self, vector):
        return math.sqrt(sum([v*v for v in vector]))
    
    def get_endpoint(self):
        x = self.origin[0] 
        y = self.origin[1]
        cos_frame_angle = np.dot(self.xdir, [1,0]) / (self.vectorLength(self.xdir)*(self.vectorLength([1,0])))
        frame_angle_diff = math.acos(cos_frame_angle)
        
        theta = self.theta - (frame_angle_diff * 180 / math.pi)
        x += self.length * math.cos(theta / 180 * math.pi)
        y += self.length * math.sin(theta / 180 * math.pi)

        return (x, y)

    


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))
        self.pen.setWidth(3)
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        self.link1 = QtCore.QRectF(100,200,11.2,15)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(853, 619)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 601, 601))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.link1CWButton = QtWidgets.QPushButton(Dialog)
        self.link1CWButton.setGeometry(QtCore.QRect(740, 40, 75, 23))
        self.link1CWButton.setObjectName("link1CWButton")
        self.link2CCWButton = QtWidgets.QPushButton(Dialog)
        self.link2CCWButton.setGeometry(QtCore.QRect(640, 110, 75, 23))
        self.link2CCWButton.setObjectName("link2CCWButton")
        self.link2CWButton = QtWidgets.QPushButton(Dialog)
        self.link2CWButton.setGeometry(QtCore.QRect(740, 110, 75, 23))
        self.link2CWButton.setObjectName("link2CWButton")
        self.link3CCWButton = QtWidgets.QPushButton(Dialog)
        self.link3CCWButton.setGeometry(QtCore.QRect(640, 180, 75, 23))
        self.link3CCWButton.setObjectName("link3CCWButton")
        self.link3CWButton = QtWidgets.QPushButton(Dialog)
        self.link3CWButton.setGeometry(QtCore.QRect(740, 180, 75, 23))
        self.link3CWButton.setObjectName("link3CWButton")
        self.drawOffButton = QtWidgets.QPushButton(Dialog)
        self.drawOffButton.setGeometry(QtCore.QRect(640, 250, 75, 23))
        self.drawOffButton.setObjectName("drawOffButton")
        self.drawOnButton = QtWidgets.QPushButton(Dialog)
        self.drawOnButton.setGeometry(QtCore.QRect(740, 250, 75, 23))
        self.drawOnButton.setObjectName("drawOnButton")
        self.link1CCWButton = QtWidgets.QPushButton(Dialog)
        self.link1CCWButton.setGeometry(QtCore.QRect(640, 40, 75, 23))
        self.link1CCWButton.setObjectName("link1CCWButton")


        self.link1origin = (300,0)
        #self.link1 = Link(150, (300, 0), 90, [1,0], [0,1])
        #self.link2origin = self.link1.get_endpoint()
        #self.link2 = Link(100, self.link2origin, 90, [1,0], [0,1])









        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def createLine(self, link):
        line = QtGui.Q



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.link1CWButton.setText(_translate("Dialog", "Link 1 CW"))
        self.link2CCWButton.setText(_translate("Dialog", "Link 2 CCW"))
        self.link2CWButton.setText(_translate("Dialog", "Link 2 CW"))
        self.link3CCWButton.setText(_translate("Dialog", "Link 3 CCW"))
        self.link3CWButton.setText(_translate("Dialog", "Link 3 CW"))
        self.drawOffButton.setText(_translate("Dialog", "Draw Off"))
        self.drawOnButton.setText(_translate("Dialog", "Draw On"))
        self.link1CCWButton.setText(_translate("Dialog", "Link 1 CCW"))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black,  5, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255,255,255)))
        painter.drawRect(self.link1)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MyWidget()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

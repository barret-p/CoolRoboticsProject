import sys, math
from PyQt5 import QtGui, uic, QtCore, QtWidgets
import numpy as np
import scipy as sp
import scipy.optimize as opt

class MyWindow(QtWidgets.QMainWindow):

    # array of tuples for light positions
    lights = []

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Project3.ui', self)
        self.initUI()
    
    def initUI(self):

        # override window click event
        self.centralWidget.mouseReleaseEvent = self.addLight
        self.clearLights.clicked.connect(self.clearAllLights)

        self.setWindowTitle('Project 3: Braitenberg Vehicles')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        global t
        qp.setPen(pen)
        yellow = QtGui.QColor(255,255,0)

        # paint lights
        qp.setBrush(yellow)
        for light in self.lights:
            qp.drawEllipse(light[0], light[1], 10, 10)

    # function to add lights to the canvas
    def addLight(self, event):
        # only call if the box is checked
        if self.addLightOnClick.isChecked():
            x = event.pos().x()
            y = event.pos().y()
            self.lights.append((x, y))
            self.update()

    def clearAllLights(self):
        self.lights = []
        self.update()

def main():

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
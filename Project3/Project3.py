import sys
import math
from PyQt5 import QtGui, uic, QtCore, QtWidgets
import numpy as np
import scipy as sp
import scipy.optimize as opt


class Vehicle:
    """ A representation of a vehicle. """
    x = 0
    y = 0
    K = []

    def update(self):
        """ This function should take in sensor or light values and update the
        position and K values
        """
        pass

    def fromString(self, s):
        """Sets the vehicle's variables from an input string.

        Input:
            string s: formatted as x, y, k11, k12, k21, k22
        """
        vars = s.replace(',', '').split()
        self.x = vars[0]
        self.y = vars[1]
        self.K = [vars[2], vars[3], vars[4], vars[5]]

    def __repr__(self):
        """ Sets the printing format to use print(Vehicle). """
        return f'x: {self.x}, y: {self.y}, K: {self.K}'


class Database():
    vehicles = []

    def __init__(self, filename):
        """ Takes a filename and reads in every line as a vehicle. Every line
        should be formatted as 'x, y, k11, k12, k21, k22'.
        """
        with open(filename, 'r') as fp:
            line = fp.readline()
            while line:
                v = Vehicle()
                v.fromString(line)
                self.vehicles.append(v)
                line = fp.readline()

    def getVehicles(self):
        """ Returns the list of vehicles in the database """
        return self.vehicles


class MyWindow(QtWidgets.QMainWindow):
    # array of vehicles
    db = Database('vehicles.txt')
    vehicles = db.getVehicles()

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
        yellow = QtGui.QColor(255, 255, 0)

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
    # v = Vehicle()
    # v.fromString("1, 2, 300, 3, 0, 300")
    # print(v)
    # db = Database('vehicles.txt')

    main()

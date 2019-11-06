import sys
import math
from PyQt5 import QtGui, uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
import numpy as np
import scipy as sp
import scipy.optimize as opt


class Vehicle:
    """ A representation of a vehicle. """
    def __init__(self, line):
        self.position = [0,0]
        self.d = 5
        self.l = 4 * self.d
        self.angle = 90
        self.K = np.array([])
        self.W = np.array([])
        self.fromString(line)
        self.w1_pos = self.getLeftWheelPosition()
        self.w2_pos = self.getRightWheelPosition()
        self.leftSensor = self.getLeftSensor()
        self.rightSensor = self.getRightSensor()
        self.omega = 0
        self.R = 0
        self.timestep = 16.666 / 1000

    def update(self, lights):
        """ This function should take in sensor or light values and update the
        position and K values
        
        Input:
            np.array([[S1].  The sensor values
                      [S2]])
        """
        leftSensorDistances = []
        rightSensorDistances = []
        
        # calculate sensor values
        for light in lights:
            leftSensorDistances.append(self.getDistance(self.leftSensor, light))
            rightSensorDistances.append(self.getDistance(self.rightSensor, light))
        leftSensorValue = sum([100/max(d, 1e-5) for d in leftSensorDistances])
        rightSensorValue = sum([100/max(d, 1e-5) for d in rightSensorDistances])

        # calculate wheel velocities
        self.W = np.matmul(self.K, np.array([[leftSensorValue], 
                                             [rightSensorValue]]))
        
        # calculate angular velocity (omega)
        diff = self.W[0] - self.W[1]
        self.omega = diff/(2*self.d)
        if diff == 0:
            self.R = self.d*sum(self.W)/0.000000001
        else:
            self.R = self.d*sum(self.W)/diff

        V = (self.W[0] + self.W[1]) / 2

        # integration
        self.angle += self.omega * self.timestep
        self.position[0] += V * math.sin(math.radians(self.angle))
        self.position[1] += V * math.cos(math.radians(self.angle))

        self.w1_pos = self.getLeftWheelPosition()
        self.w2_pos = self.getRightWheelPosition()
        self.leftSensor = self.getLeftSensor()
        self.rightSensor = self.getRightSensor()
        QApplication.activeWindow().update()


    def fromString(self, s):
        """Sets the vehicle's variables from an input string.

        Input:
            string s: formatted as x, y, k11, k12, k21, k22
        """
        vars = s.replace(',', '').split()
        self.position = [int(vars[0]), int(vars[1])]
        print(self.position)
        self.K = np.array([[int(vars[2]), int(vars[3])], 
                           [int(vars[4]), int(vars[5])]])
        
    def getDistance(self, sensor, lightSource):
        horizontal = (lightSource[0] - sensor[0])**2
        vertical = (lightSource[1] - sensor[1])**2
        
        return math.sqrt(horizontal + vertical)

    def getLeftWheelPosition(self):
        x =  self.d * math.cos(math.radians(self.angle)) + self.position[0]
        y = -self.d * math.sin(math.radians(self.angle)) + self.position[1]
        return [x,y]
    
    def getRightWheelPosition(self):
        x = -self.d * math.cos(math.radians(self.angle)) + self.position[0]
        y =  self.d * math.sin(math.radians(self.angle)) + self.position[1]
        return [x,y]

    def getLeftSensor(self):
        x = self.l * math.sin(math.radians(self.angle)) + self.w1_pos[0]
        y = self.l * math.cos(math.radians(self.angle)) + self.w1_pos[1]
        return [x,y]
    
    def getRightSensor(self):
        x = self.l * math.sin(math.radians(self.angle)) + self.w2_pos[0]
        y = self.l * math.cos(math.radians(self.angle)) + self.w2_pos[1]
        return [x,y]

    def paint(self, qp):
        w1_pos = [int(w) for w in self.w1_pos]
        w2_pos = [int(w) for w in self.w2_pos]
        rightSensor = [int(w) for w in self.rightSensor]
        leftSensor = [int(w) for w in self.leftSensor]

        # draw rectangle
        qp.drawLine(w1_pos[0], w1_pos[1], w2_pos[0], w2_pos[1])
        qp.drawLine(w2_pos[0], w2_pos[1], rightSensor[0], rightSensor[1])
        qp.drawLine(rightSensor[0], rightSensor[1], leftSensor[0], leftSensor[1])
        qp.drawLine(leftSensor[0], leftSensor[1], w1_pos[0], w1_pos[1])


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
            for line in fp:
                v = Vehicle(line)
                self.vehicles.append(v)                

    def getVehicles(self):
        """ Returns the list of vehicles in the database """
        return self.vehicles


class MyWindow(QtWidgets.QMainWindow):
    # array of vehicles
    db = Database('vehicles.txt')
    

    # array of tuples for light positions
    lights = []

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Project3.ui', self)
        self.initUI()
        self.vehicles = self.db.getVehicles()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

    def timerEvent(self):
        for vehicle in self.vehicles:
            vehicle.update(self.lights)

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

        # paint vehicles
        qp.setBrush(QtGui.QColor(255,255,255))
        for vehicle in self.vehicles:
            vehicle.paint(qp)

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
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # v = Vehicle()
    # v.fromString("1, 2, 300, 3, 0, 300")
    # print(v)
    #db = Database('vehicles.txt')

    main()

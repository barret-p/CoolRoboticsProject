import sys, math
from PyQt5 import QtGui, uic, QtCore, QtWidgets
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import fmin_slsqp
#from scipy.optimize import *

# fixed origin
originX = 380
originY = 350
# angle of three joints
theta1 = 180 
theta2 = 120
theta3 = 180
t = [theta1, theta2, theta3]
q0 = np.array([np.pi/4, np.pi/4, np.pi/4])
# length of three joints
l1len= 150
l2len = 100
l3len = 75
L = [l1len, l2len, l3len]
# radius of joint and brush
joint_rad = 20
brush_rad = 10
# position of paint brush
brush_x = 0
brush_y = 0
brush_org_x = 0
brush_org_y = 0
# change in angle (degrees)
delta_theta = 1

# slider values
slider_start =  [-3, -3, -3]
slider_end = [363, 363, 363]
slider1_start = -3
slider1_end = 363
slider2_start = -3
slider2_end = 363
slider3_start = -3
slider3_end = 363


point_list = []

def equations(thetas, x, y):
    t1, t2, t3 = thetas
    #print(thetas)
    t1 = t1 % 360
    t2 = t2 % 360
    t3 = t3 % 360
    t1 = math.radians(t1)
    t2 = math.radians(t2)
    t3 = math.radians(t3)
    x_ = originX + l1len*math.sin(t1) + l2len*math.sin(t2) + l3len*math.sin(t3)
    y_ = originY + l1len*math.cos(t1) + l2len*math.cos(t2) + l3len*math.cos(t3)
    
    e1 = x - x_
    e2 = y - y_
    e3 = t1 - t2
    return (e1,e2,e3)

def distance_to_default(q, *args):
    """Objective function to minimize
    Calculates the euclidean distance through joint space to the
    default arm configuration. The weight list allows the penalty of
    each joint being away from the resting position to be scaled
    differently, such that the arm tries to stay closer to resting
    state more for higher weighted joints than those with a lower
    weight.
    q : np.array
        the list of current joint angles
    returns : scalar
        euclidean distance to the default arm position
    """
    # weights found with trial and error,
    # get some wrist bend, but not much
    weight = [1, 1, 1.3]
    return np.sqrt(np.sum([(qi - q0i)**2 * wi
                   for qi, q0i, wi in zip(q, q0, weight)]))

def x_constraint(q, xy):
    """Returns the corresponding hand xy coordinates for
    a given set of joint angle values [shoulder, elbow, wrist],
    and the above defined arm segment lengths, L
    q : np.array
        the list of current joint angles
    xy : np.array
        current xy position (not used)
    returns : np.array
        the difference between current and desired x position
    """
    x = (L[0]*np.sin(q[0]) + L[1]*np.sin(q[1]) +
         L[2]*np.sin(q[2])) - xy[0]
    return x

def y_constraint(q, xy):
    """Returns the corresponding hand xy coordinates for
    a given set of joint angle values [shoulder, elbow, wrist],
    and the above defined arm segment lengths, L
    q : np.array
        the list of current joint angles
    xy : np.array
        current xy position (not used)
    returns : np.array
        the difference between current and desired y position
    """
    y = (L[0]*np.cos(q[0]) + L[1]*np.cos(q[1]) +
         L[2]*np.cos(q[2])) - xy[1]
    return y


class MyWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('project2.ui', self)
        self.initUI()
        self.brushColor = QtGui.QColor(255,255,255)
        
    def initUI(self):

        #Go to functions when buttons are pressed
        self.pushButtonCCW1.clicked.connect(self.Joint1CCW)
        self.pushButtonCW1.clicked.connect(self.Joint1CW)
        self.pushButtonCCW2.clicked.connect(self.Joint2CCW)
        self.pushButtonCW2.clicked.connect(self.Joint2CW)
        self.pushButtonCCW3.clicked.connect(self.Joint3CCW)
        self.pushButtonCW3.clicked.connect(self.Joint3CW)
        self.pushButtonPaint.clicked.connect(self.Paint)
        self.pushButtonClear.clicked.connect(self.Clear)
        self.pushButtonUndo.clicked.connect(self.Undo)

        self.pushButtonIncrX.clicked.connect(self.IncrX)
        self.pushButtonDecrX.clicked.connect(self.DecrX)
        self.pushButtonIncrY.clicked.connect(self.IncrY)
        self.pushButtonDecrY.clicked.connect(self.DecrY)

        self.redButton.clicked.connect(self.redPressed)
        self.greenButton.clicked.connect(self.greenPressed)
        self.blueButton.clicked.connect(self.bluePressed)
        self.customButton.clicked.connect(self.customPressed)

        intValidator = QtGui.QIntValidator(0,255)
        self.redEdit.setValidator(intValidator)
        self.greenEdit.setValidator(intValidator)
        self.blueEdit.setValidator(intValidator)

        self.horizontalSlider.setRange(slider_start[0], slider_end[0])
        self.horizontalSlider_2.setRange(slider_start[1], slider_end[1])
        self.horizontalSlider_3.setRange(slider_start[2], slider_end[2])
        
        self.horizontalSlider.setValue(theta1)
        self.horizontalSlider_2.setValue(theta2)
        self.horizontalSlider_3.setValue(theta3)
        
        self.horizontalSlider.setTickInterval(0.1)
        self.horizontalSlider_2.setTickInterval(0.1)
        self.horizontalSlider_3.setTickInterval(0.1)
        
        self.horizontalSlider.sliderMoved.connect(self.Joint1Slilder)
        self.horizontalSlider_2.sliderMoved.connect(self.Joint2Slilder)
        self.horizontalSlider_3.sliderMoved.connect(self.Joint3Slilder)
        
        self.horizontalSlider.sliderReleased.connect(self.updateSliderValues)
        self.horizontalSlider_2.sliderReleased.connect(self.updateSliderValues)
        self.horizontalSlider_3.sliderReleased.connect(self.updateSliderValues)
        
        self.setWindowTitle('Project 1: Forward Kinematics')    
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)

        join1_x = originX - joint_rad / 2
        join1_y = originY - joint_rad / 2
        qp.drawEllipse(join1_x, join1_y, joint_rad, joint_rad)

        #Draw first link
        link1_startx = originX
        link1_starty = originY
        link1_endx = originX + l1len*math.sin(math.radians(theta1))
        link1_endy = originY + l1len*math.cos(math.radians(theta1))
        link1 = qp.drawLine(link1_startx, link1_starty, link1_endx, link1_endy)

        #Draw second R joint
        joint2_x = link1_endx - joint_rad / 2
        joint2_y = link1_endy - joint_rad / 2
        qp.drawEllipse(joint2_x, joint2_y, joint_rad, joint_rad)

        #Draw second link
        link2_startx = link1_endx
        link2_starty = link1_endy
        link2_endx = link2_startx + l2len*math.sin(math.radians(theta2))
        link2_endy = link2_starty + l2len*math.cos(math.radians(theta2))
        link2 = qp.drawLine(link2_startx, link2_starty, link2_endx, link2_endy)

        #Draw third R joint
        joint3_x = link2_endx - joint_rad / 2
        joint3_y = link2_endy - joint_rad / 2
        qp.drawEllipse(joint3_x, joint3_y, joint_rad, joint_rad)

        #Draw third link
        link3_startx = link2_endx
        link3_starty = link2_endy
        link3_endx = link3_startx + l3len*math.sin(math.radians(theta3))
        link3_endy = link3_starty + l3len*math.cos(math.radians(theta3))
        link3 = qp.drawLine(link3_startx, link3_starty, link3_endx, link3_endy)
        global brush_org_x, brush_org_y
        brush_org_x = link3_endx
        brush_org_y = link3_endy
        #print((theta1, theta2, theta3))
        #print((brush_org_x, brush_org_y))

        #Draw paint brush
        global brush_x, brush_y
        brush_x = link3_endx - brush_rad / 2
        brush_y = link3_endy - brush_rad / 2
        qp.setBrush(self.brushColor)
        qp.drawEllipse(brush_x, brush_y, brush_rad, brush_rad)

        global t
        t = [theta1, theta2, theta3]

        #Draw paint
        for i in range(0, len(point_list)):
            x = point_list[i][0][0]
            y = point_list[i][0][1]
            point_color = point_list[i][1]
            qp.setBrush(point_color)
            qp.setPen(point_color)
            qp.drawEllipse(x,y,10,10)
    
    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_A:
            self.DecrX()
        elif key == QtCore.Qt.Key_D:
            self.IncrX()
        elif key == QtCore.Qt.Key_W:
            self.IncrY()
        elif key == QtCore.Qt.Key_S:
            self.DecrY()

#DRAWING FUNCTIONS

    def DecrX(self):
        pass

    def IncrX(self):
        pass

    def DecrY(self):
        if self.checkBox.isChecked():
            self.Paint()
        global t, theta1, theta2, theta3

        cur_x = brush_org_x
        cur_y = brush_org_y
        cur_y += 1

        total_l = l1len + l2len + l3len
        print("Old pos is {}".format((brush_org_x, brush_org_y)))
        print("Old theta is {}".format((t[0],t[1],t[2])))

        # possible solution
        if math.sqrt(pow(cur_x - originX, 2) + pow(cur_y - originY, 2)) <= total_l:

             
            
            #t1, t2, t3 = fsolve(equations, (theta1, theta2, theta3), args=(cur_x, cur_y))
            t = fmin_slsqp(func=distance_to_default, x0=t,eqcons=[x_constraint, y_constraint], args=([cur_x, cur_y],))
            print(t)
            # t1 = math.degrees(t1)
            # t2 = math.degrees(t2)
            # t3 = math.degrees(t3)
            # t1 %= 360
            # t2 %= 360
            # t3 %= 360

            # self.horizontalSlider.setValue(t1)
            # self.horizontalSlider_2.setValue(t2)
            # self.horizontalSlider_3.setValue(t3)

            # theta1 = t1
            # theta2 = t2
            # theta3 = t3

        # impossible solution
        else:
            print("impossible solution")

        print("new pos is {}".format((cur_x, cur_y)))
        print("new theta is {}".format((t[0],t[1],t[2])))
    

        self.update()

    def IncrY(self):
        if self.checkBox.isChecked():
            self.Paint()
        global t, theta1, theta2, theta3

        cur_x = brush_org_x
        cur_y = brush_org_y
        cur_y -= 1

        total_l = l1len + l2len + l3len
        print("Old pos is {}".format((brush_org_x, brush_org_y)))
        print("Old theta is {}".format((t[0],t[1],t[2])))

        # possible solution
        if math.sqrt(pow(cur_x - originX, 2) + pow(cur_y - originY, 2)) <= total_l:

            #t1, t2, t3 = fsolve(equations, (theta1, theta2, theta3), args=(cur_x, cur_y))
            t1 = fmin_slsqp(func=distance_to_default, x0=t,eqcons=[x_constraint, y_constraint], args=([cur_x, cur_y],))
            print(t1)
            # t1 = math.degrees(t1)
            # t2 = math.degrees(t2)
            # t3 = math.degrees(t3)
            # t1 %= 360
            # t2 %= 360
            # t3 %= 360

            # self.horizontalSlider.setValue(t1)
            # self.horizontalSlider_2.setValue(t2)
            # self.horizontalSlider_3.setValue(t3)

            # theta1 = t1
            # theta2 = t2
            # theta3 = t3

        # impossible solution
        else:
            print("impossible solution")

        print("new pos is {}".format((cur_x, cur_y)))
        print("new theta is {}".format((t[0],t[1],t[2])))

        self.update()

    def updateSliderRanges(self, delta, num_sliders):
        global slider_start, slider_end
        
        slider_start.reverse()
        slider_end.reverse()

        for i in range(0, num_sliders):
            slider_start[i] += delta
            slider_end[i] += delta
        
        slider_start.reverse()
        slider_end.reverse()

        self.horizontalSlider.setRange(slider_start[0], slider_end[0])
        self.horizontalSlider_2.setRange(slider_start[1], slider_end[1])
        self.horizontalSlider_3.setRange(slider_start[2], slider_end[2])
        
    def updateSliderValues(self):
        global theta1, theta2, theta3
        self.horizontalSlider.setValue(theta1)
        self.horizontalSlider_2.setValue(theta2)
        self.horizontalSlider_3.setValue(theta3)

    def Joint1CCW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta1, theta2, theta3, delta_theta
        theta1 = theta1 + delta_theta
        theta2 = theta2 + delta_theta
        theta3 = theta3 + delta_theta
        self.horizontalSlider.setValue(self.horizontalSlider.value() + delta_theta)
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() + delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() + delta_theta)
        self.updateSliderRanges(delta_theta, 3)
        self.update()

    def Joint1CW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta1, theta2, theta3
        theta1 = theta1 - delta_theta
        theta2 = theta2 - delta_theta
        theta3 = theta3 - delta_theta
        self.horizontalSlider.setValue(self.horizontalSlider.value() - delta_theta)
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() - delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() - delta_theta)
        self.updateSliderRanges(-delta_theta, 3)
        self.update()

    def Joint2CCW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta2, theta3
        theta2 = theta2 + delta_theta
        theta3 = theta3 + delta_theta
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() + delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() + delta_theta)
        self.updateSliderRanges(delta_theta, 2)
        self.update()

    def Joint2CW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta2, theta3
        theta2 = theta2 - delta_theta
        theta3 = theta3 - delta_theta
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() - delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() - delta_theta)
        self.updateSliderRanges(-delta_theta, 2)
        self.update()

    def Joint3CCW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta3 
        theta3 = theta3 + delta_theta
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() + delta_theta)
        self.updateSliderRanges(delta_theta, 1)
        self.update()

    def Joint3CW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta3
        theta3 = theta3 - delta_theta
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() - delta_theta)
        self.updateSliderRanges(-delta_theta, 1)
        self.update()

    def Joint1Slilder(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta1, theta2, theta3
        changeInTheta = self.horizontalSlider.value() - theta1
        theta1 += changeInTheta
        theta2 += changeInTheta
        theta3 += changeInTheta
        self.update()
        
    def Joint2Slilder(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta2, theta3
        changeInTheta = self.horizontalSlider_2.value() - theta2
        theta2 += changeInTheta
        theta3 += changeInTheta
        self.update()
        
    def Joint3Slilder(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta3
        theta3 = self.horizontalSlider_3.value()
        self.update()

    def checkColor(self, color):
        if color.isdigit() and 0 <= int(color) <= 255:
            return int(color)
        else:
            print("bad color")
            return 0

    def redPressed(self):
        self.redEdit.setText('255')
        self.greenEdit.setText('0')
        self.blueEdit.setText('0')
        self.brushColor = QtGui.QColor(255,0,0)
        self.update()

    def greenPressed(self):
        self.redEdit.setText('0')
        self.greenEdit.setText('255')
        self.blueEdit.setText('0')
        self.brushColor = QtGui.QColor(0,255,0)
        self.update()

    def bluePressed(self):
        self.redEdit.setText('0')
        self.greenEdit.setText('0')
        self.blueEdit.setText('255')
        self.brushColor = QtGui.QColor(0,0,255)
        self.update()

    def customPressed(self):
        red = self.checkColor(self.redEdit.text())
        green = self.checkColor(self.greenEdit.text())
        blue = self.checkColor(self.blueEdit.text())
        self.brushColor = QtGui.QColor(red, green, blue)
        self.update()

    def Paint(self):
        global point_list, brush_x, brush_y
        point_list.append(((brush_x, brush_y),self.brushColor))
        self.update()

    def Clear(self):
        global point_list
        del point_list[:]
        self.update()

    def Undo(self):
        global point_list
        if len(point_list):
            point_list.pop()
        self.update()

def main():
    
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

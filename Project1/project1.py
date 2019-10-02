import sys, math
from PyQt5 import QtGui, uic, QtCore, QtWidgets

originX = 380
originY = 350
d = 0
theta1 = 180 
theta2 = 180
theta3 = 180
l1len= 150
l2len = 100
l3len = 75
joint_rad = 20
brush_rad = 10
brush_x = 0
brush_y = 0
delta_theta = 1

point_list=[]

class MyWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('project1.ui', self)
         
        self.initUI()
        
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

        self.redButton.clicked.connect(self.redPressed)
        self.greenButton.clicked.connect(self.greenPressed)
        self.redButton.clicked.connect(self.bluePressed)
        self.redButton.clicked.connect(self.customPressed)

        intValidator = QtGui.QIntValidator(0,255)
        self.redEdit.setValidator(intValidator)
        self.greenEdit.setValidator(intValidator)
        self.blueEdit.setValidator(intValidator)


        self.horizontalSlider.setRange(-3, 363)
        self.horizontalSlider_2.setRange(-3, 363)
        self.horizontalSlider_3.setRange(-3, 363)
        
        self.horizontalSlider.setValue(theta1)
        self.horizontalSlider_2.setValue(theta2)
        self.horizontalSlider_3.setValue(theta3)
        
        self.horizontalSlider.setTickInterval(0.1)
        self.horizontalSlider_2.setTickInterval(0.1)
        self.horizontalSlider_3.setTickInterval(0.1)
        
        self.horizontalSlider.sliderMoved.connect(self.Joint1Slilder)
        self.horizontalSlider_2.sliderMoved.connect(self.Joint2Slilder)
        self.horizontalSlider_3.sliderMoved.connect(self.Joint3Slilder)
        
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

        #Draw paint brush
        global brush_x, brush_y
        brush_x = link3_endx - brush_rad / 2
        brush_y = link3_endy - brush_rad / 2
        qp.drawEllipse(brush_x, brush_y, brush_rad, brush_rad)


        #Draw paint
        for i in range(0, len(point_list)):
            x = point_list[i][0]
            y = point_list[i][1]
            qp.setBrush(QtCore.Qt.black)
            qp.drawEllipse(x,y,10,10)

#DRAWING FUNCTIONS

    def Joint1CCW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta1, theta2, theta3, delta_theta
        theta1 = theta1 + delta_theta
        theta2 = theta2 + delta_theta
        theta3 = theta3 + delta_theta
        self.horizontalSlider.setValue(self.horizontalSlider.value() - delta_theta)
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() - delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() - delta_theta)
        self.update()

    def Joint1CW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta1, theta2, theta3
        theta1 = theta1 - delta_theta
        theta2 = theta2 - delta_theta
        theta3 = theta3 - delta_theta
        self.horizontalSlider.setValue(self.horizontalSlider.value() + delta_theta)
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() + delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() + delta_theta)
        self.update()

    def Joint2CCW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta2, theta3
        theta2 = theta2 + delta_theta
        theta3 = theta3 + delta_theta
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() - delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() - delta_theta)
        self.update()

    def Joint2CW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta2, theta3
        theta2 = theta2 - delta_theta
        theta3 = theta3 - delta_theta
        self.horizontalSlider_2.setValue(self.horizontalSlider_2.value() + delta_theta)
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() + delta_theta)
        self.update()

    def Joint3CCW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta3 
        theta3 = theta3 + delta_theta
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() - delta_theta)
        self.update()

    def Joint3CW(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta3
        theta3 = theta3 - delta_theta
        self.horizontalSlider_3.setValue(self.horizontalSlider_3.value() + delta_theta)
        self.update()

    def Joint1Slilder(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta1, theta2, theta3
        changeInTheta = -self.horizontalSlider.value() - theta1
        theta1 += changeInTheta
        theta2 += changeInTheta
        theta3 += changeInTheta
        self.update()
        
    def Joint2Slilder(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta2, theta3
        changeInTheta = -self.horizontalSlider_2.value()- theta2
        theta2 += changeInTheta
        theta3 += changeInTheta
        self.update()
        
    def Joint3Slilder(self):
        if self.checkBox.isChecked():
            self.Paint()
        global theta3
        theta3 = -self.horizontalSlider_3.value()
        self.update()

    def redPressed(self):
        self.redEdit.setText(255)
        self.greenEdit.setText(0)
        self.blueEdit.setText(0)

        pass

    def greenPressed(self):
        pass

    def bluePressed(self):
        pass

    def customPressed(self):
        pass

    def setPaintBrushColor(self):
        pass

    def Paint(self):
        global point_list, brush_x, brush_y
        point_list.append((brush_x, brush_y))
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

import sys, math, pprint, collections, copy
from functools import total_ordering
from PyQt5 import QtGui, uic, QtCore, QtWidgets
from priodict import priorityDictionary
from itertools import groupby

items_dict = {'robot': None, 'box100': None, 'box150': None, 'box200': None,
              'HorizontalLines': [], 'VerticalLines': [], 'Path': [] }
items = []
originX = 20
originY = 20
maxX = 520
maxY = 520

# source for Dijkstra algo: http://homepages.uc.edu/~annexsfs/UC_Pages/Sample_Codes_files/dijkstra.py
def Dijkstra(G,start,end=None):
    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    Q = priorityDictionary()    # estimated distances of non-final vertices
    Q[start] = 0
    
    for v in Q:
        D[v] = Q[v]
        if v == end: break
        
        for w in G[v]:
            vwLength = D[v] + G[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise ValueError("Dijkstra: found better path to already-final vertex")
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v
    
    return (D,P)

def shortestPath(G,start,end):
    """
    Find a single shortest path from the given start vertex to the given end vertex.
    The input has the same conventions as Dijkstra().
    The output is a list of the vertices in order along the shortest path.
    """

    D,P = Dijkstra(G,start,end)
    P[0] = list(G[0])[0]
    P[1] = list(G[1])[0]
    # print(P)
    Path = []
    while 1:
        Path.append(end)
        if end == start: break
        if end not in P.keys():
            print("Cannot find a connecting path")
            return -1
            break
        end = P[end]
    Path.reverse()
    return Path
            
def distance(point1, point2):
    return math.sqrt((point2.y-point1.y)**2 + (point2.x-point1.x)**2)

# creates adjacency matrix
def generateGraph(centerpoints,cells):
    #initialize graph
    graph = {}
    for point in centerpoints:
        graph[centerpoints.index(point)] = {}

    graph[0] = {}
    graph[1] = {}
    
    pointstart = centerpoints[0]
    pointend = centerpoints[1]
    minimum = sys.maxsize
    index = 0
    for point in centerpoints[2:]:
        dist = distance(pointstart, point)
        if minimum > dist:
            minimum = dist
            index = centerpoints.index(point)
    graph[0][index] = minimum

    minimum = sys.maxsize
    index = 0
    for point in centerpoints[2:]:
        dist = distance(pointend, point)
        if minimum > dist:
            minimum = dist
            index = centerpoints.index(point)
    graph[1][index] = minimum
    
    for cell in cells:
        centerpoint = cell.getCenter()
        for othercell in cells:
            if cell is not othercell and cell.isCellAdjacent(othercell):
                othercenterpoint = othercell.getCenter()
                ctrptidx = centerpoints.index(centerpoint)
                otherctrptidx = centerpoints.index(othercenterpoint)
                graph[ctrptidx][otherctrptidx] = distance(centerpoint, othercenterpoint)

    # pprint.pprint(graph)
    return graph

# define various classes for ui elements

# parent class
class UIItem:
    def __init__(self):
        self.X = 20
        self.Y = 20
        
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return (self.x , self.y) == (other.x, other.y)
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x , other.y)
    
class Box(UIItem):
    def __init__(self, x, y, size):
        UIItem.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        
    def getTop(self):
        return Point(self.x + self.size[0]/2, self.y)
    
    def getBottom(self):
        return Point(self.x + self.size[0]/2, self.y + self.size[1])
    
    def getLeft(self):
        return Point(self.x, self.y + self.size[1]/2)
    
    def getRight(self):
        return Point(self.x + self.size[0], self.y + self.size[1]/2)

    def getCenter(self):
        return Point(self.getTop().x, self.getRight().y)

    def isInside(self, point):
        return (point.x <= (self.x+self.size[0]) and point.x >= self.x) and \
                   (point.y <= (self.y+self.size[1]) and point.y >= self.y)
    
    def draw(self, painter):
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRect(self.X + self.x, self.Y + self.y, self.size[0], self.size[1])
        
class Robot(UIItem):
    def __init__(self, x, y, x_end, y_end):
        UIItem.__init__(self)
        self.x = x
        self.y = y
        self.x_end = x_end
        self.y_end = y_end
        self.size = [10, 10]
        
    def getPosition(self):
        return [self.x, self.y]
    
    def draw(self, painter):
        painter.setBrush(QtCore.Qt.white)
        painter.drawEllipse(self.X + self.x, self.Y + self.y, self.size[0], self.size[1])
        painter.setBrush(QtCore.Qt.black)
        painter.drawEllipse(self.X + self.x_end, self.Y + self.y_end, self.size[0], self.size[1])
        
class VerticalLine(UIItem):
    def __init__(self, x, y1, y2):
        UIItem.__init__(self)
        self.x = x
        self.y1 = y1
        self.y2 = y2
    
    def draw(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine))
        # painter.drawLine(self.X + self.x, self.Y + self.y1, self.X + self.x, self.Y + self.y2)
        
class HorizontalLine(UIItem):
    def __init__(self, x1, x2, y):
        UIItem.__init__(self)
        self.x1 = x1
        self.y = y
        self.x2 = x2
    
    def draw(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine))
        # painter.drawLine(self.X + self.x1, self.Y + self.y, self.X + self.x2, self.Y + self.y)
        
class Path(UIItem):
    def __init__(self, x1, y1, x2, y2):
        UIItem.__init__(self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def draw(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine))
        painter.drawLine(self.X + self.x1, self.Y + self.y1, self.X + self.x2, self.Y + self.y2)
        
class Cell(Box):
    def isAdjacent(self, point):
        if point in [self.getTop(), self.getBottom(), self.getLeft(), self.getRight()]:
            return True
        
        return False
    def isCellAdjacent(self, cell):
        if self.getTop() == cell.getBottom() or self.getRight() == cell.getLeft() \
            or self.getBottom() == cell.getTop() or self.getLeft() == cell.getRight():
            return True
        else:
            return False
        
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('project5.ui', self)
        self.initUI()
        
    def initUI(self):
        # functions for button press
        self.addRobotButton.clicked.connect(self.addRobot)
        self.addBox1Button.clicked.connect(self.addBox1)
        self.addBox2Button.clicked.connect(self.addBox2)
        self.addBox3Button.clicked.connect(self.addBox3)
        self.calculateButton.clicked.connect(self.calculate)
        self.removePathButton.clicked.connect(self.removePath)
        self.removeAllButton.clicked.connect(self.removeAll)
        self.pathNotFoundLabel.hide()

        self.centralWidget.mouseReleaseEvent = self.addItem
        self.setWindowTitle('Project 5: Robot Motion Planning')    
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))

        global originX, originY, items
        qp.drawRect(originX, originY, originX+500, originY+500)

        # draw every item according to its draw function
        for item in items_dict.values():
            if item != None:
                if isinstance(item, collections.Iterable):
                    for it in item:
                        it.draw(qp)
                else:
                    item.draw(qp)

    def addItem(self, event):
        global items_dict, items, originX, originY
        x = event.pos().x() - originX
        y = event.pos().y() - originY

        if self.mouseEntryCheckBox.isChecked():
            if self.robotStartRadioButton.isChecked():
                if items_dict['robot'] != None:
                    addItem = False
                    items_dict['robot'].x = x
                    items_dict['robot'].y = y
                else:
                    robot = Robot(x, y, 0, 0)
                    items_dict['robot'] = robot
                    items.append(robot)
                
                self.lineEditRobotX.setText(str(x))
                self.lineEditRobotY.setText(str(y))
            elif self.robotEndRadioButton.isChecked():
                if items_dict['robot'] != None:
                    addItem = False
                    items_dict['robot'].x_end = x
                    items_dict['robot'].y_end = y
                else:
                    robot = Robot(0, 0, x, y)
                    item_dict['robot'] = robot
                    items.append(robot)

                self.lineEditRobotXend.setText(str(x))
                self.lineEditRobotYend.setText(str(y))
            elif self.block1RadioButton.isChecked():
                self.addBox(x, y, 200, 200, "box200")
                self.lineEditBoxX_1.setText(str(x))
                self.lineEditBoxY_1.setText(str(y))
            elif self.block2RadioButton.isChecked():
                self.addBox(x, y, 150, 150, "box150")
                self.lineEditBoxX_2.setText(str(x))
                self.lineEditBoxY_2.setText(str(y))
            elif self.block3RadioButton.isChecked():
                self.addBox(x, y, 100, 100, "box100")
                self.lineEditBoxX_3.setText(str(x))
                self.lineEditBoxY_3.setText(str(y))
            else:
                pass

        self.update()

    def addRobot(self):
        x = int(self.lineEditRobotX.text())
        y = int(self.lineEditRobotY.text())
        x_end = int(self.lineEditRobotXend.text())
        y_end = int(self.lineEditRobotYend.text())

        global items, items_dict
        addItem = True

        #if item already created, don't create new item. Modify existing item
        if items_dict['robot'] != None:
            items_dict['robot'].x = x
            items_dict['robot'].y = y
            items_dict['robot'].x_end = x
            items_dict['robot'].y_end = y
        #otherwise create new item
        else:
            robot = Robot(x, y, x_end, y_end)
            items_dict['robot'] = robot

        self.update()

    # generic add box function for the functions below
    def addBox(self, x, y, sizex, sizey, obj):
        global items, items_dict

        if items_dict[obj] != None:
            items_dict[obj].x = x
            items_dict[obj].y = y
        else:
            box = Box(x, y, [sizex, sizey])
            items_dict[obj] = box

        self.update()

    def addBox1(self):
        x = int(self.lineEditBoxX_1.text())
        y = int(self.lineEditBoxY_1.text())
        
        self.addBox(x, y, 200, 200, "box200")

    def addBox2(self):
        x = int(self.lineEditBoxX_2.text())
        y = int(self.lineEditBoxY_2.text())

        self.addBox(x,y, 150, 150, "box150")

    def addBox3(self):
        x = int(self.lineEditBoxX_3.text())
        y = int(self.lineEditBoxY_3.text())

        self.addBox(x, y, 100, 100, "box100")

    def displayPathNotFound(self):
        self.pathNotFoundLabel.show()

    def removePathNotFound(self):
        self.pathNotFoundLabel.hide()

    def calculate(self):
        global items, items_dict
        boxes = [items_dict['box100'], items_dict['box150'], items_dict['box200']]
        # remove any none objects
        boxes = [box for box in boxes if box != None]

        # check if either start or end point is inside a box
        for box in boxes:
            startpoint = Point(items_dict['robot'].x, items_dict['robot'].y)
            endpoint = Point(items_dict['robot'].x_end, items_dict['robot'].y_end)
            if box.isInside(startpoint) or box.isInside(endpoint):
                self.displayPathNotFound()
                self.update()
                return

        items_dict['VerticalLines'].append(VerticalLine(0,0,maxY))
        items_dict['VerticalLines'].append(VerticalLine(maxX,0,maxY))
        items_dict['HorizontalLines'].append(HorizontalLine(0,maxX,0))
        items_dict['HorizontalLines'].append(HorizontalLine(0,maxX,maxY))

        for box in boxes:
            items_dict['VerticalLines'].append(VerticalLine(box.x, 0, maxY))
            items_dict['VerticalLines'].append(VerticalLine(box.x+box.size[0], 0, maxY))
            items_dict['HorizontalLines'].append(HorizontalLine(0, maxX, box.y))
            items_dict['HorizontalLines'].append(HorizontalLine(0, maxX, box.y+box.size[1]))

        # sort lines
        hlines = items_dict['HorizontalLines']
        vlines = items_dict['VerticalLines']

        # sort functions
        def sort_by_x(vline):
            return vline.x

        def sort_by_y(hline):
            return hline.y

        vlines = sorted(vlines, key = sort_by_x)
        hlines = sorted(hlines, key = sort_by_y)


        # create cell representations
        cells = []
        for i in range(0,len(vlines)-1):
            for j in range(0,len(hlines)-1):
                x = vlines[i].x
                y = hlines[j].y
                xsize = vlines[i+1].x - vlines[i].x
                ysize = hlines[j+1].y - hlines[j].y
                cells.append(Cell(x,y,[xsize,ysize]))
        # print("Number of cells: " + str(len(cells)))

        # remove boxes from the cell list
        tempcells = copy.copy(cells)
        for cell in tempcells:
            point = cell.getCenter()
            for box in boxes:
                if box.isInside(point) and cell in cells:
                    cells.remove(cell) 

        centerpoints = []
        centerpoints.append(Point(items_dict['robot'].x, items_dict['robot'].y))
        centerpoints.append(Point(items_dict['robot'].x_end, items_dict['robot'].y_end))
        for cell in cells:
            centerpoints.append(cell.getCenter())

        graph = generateGraph(centerpoints,cells)
        path = shortestPath(graph,0,1)
        if path == -1:
            self.displayPathNotFound()
            self.update()
            return

        for index in range(len(path) - 1):
            p = Path(centerpoints[path[index]].x, centerpoints[path[index]].y, centerpoints[path[index+1]].x, centerpoints[path[index+1]].y)
            items_dict['Path'].append(p)

        # print(path)
        # print('plotted')
        self.update()

    def removePath(self):
        global items, items_dict
        items_dict['HorizontalLines'] = []
        items_dict['VerticalLines'] = []
        items_dict['Path'] = []
        self.removePathNotFound()
        self.update()

    def removeAll(self):
        global items, items_dict
        items_dict = {'robot': None, 'box100': None, 'box150': None, 'box200': None,
              'HorizontalLines': [], 'VerticalLines': [], 'Path': [] }
        # print('Items removed')
        self.removePathNotFound()
        self.update()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

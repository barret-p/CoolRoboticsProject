import sys, math, pprint, collections   
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

def distance(point1, point2):
    print(point1)
    print(point2)
    return math.sqrt((point2.y-point1.y)**2 + (point2.x-point1.x)**2)

def uniquify(li):
    checked = []
    for e in li:
        if e not in checked:
            checked.append(e)
    return checked

#Returns a graph represented as a list of lists of size n by n.
#Nonexistant edges are represented by None
#It is an adjacency matrix
def generateGraph(midpoints,cells):
    #initialize graph
    graph = {}
    for point in midpoints:
        graph[midpoints.index(point)] = {}

    graph[0] = {}
    graph[1] = {}
    
    pointstart = midpoints[0]
    pointend = midpoints[1]
    minimum = sys.maxsize
    index = 0
    for point in midpoints[2:]:
        dist = distance(pointstart.x,pointstart.y,point.x,point.y)
        if minimum > dist:
            minimum = dist
            index = midpoints.index(point)
    graph[0][index] = minimum

    minimum = sys.maxsize
    index = 0
    for point in midpoints[2:]:
        dist = distance(pointend.x,pointend.y,point.x,point.y)
        if minimum > dist:
            minimum = dist
            index = midpoints.index(point)
    graph[1][index] = minimum
    
    #Fill in values 
    for point in midpoints:
        for cell in cells:
            if cell.isAdjacent(point):
                for p in midpoints:
                    if cell.isAdjacent(p) and p != point:
                        x = midpoints.index(p)
                        y = midpoints.index(point)
                        
                        graph[x][y] = distance(p.x,p.y,point.x,point.y)
    pprint.pprint(graph)
    return graph

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
    print(P)
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

#@total_ordering
#class Point:
    #def __init__(self,x1,y1):
        #self.x = x1
        #self.y = y1
    #def __repr__(self):
        #return "[" + str(self.x) + "," + str(self.y) + "]"
    #def __eq__(self,other):
        #return (self.x,self.y)==(other.x,other.y)
    #def __lt__(self,other):
        #return (self.x,self.y) < (other.x,other.y)

#class Block:
    #def __init__(self,posx,posy,sizex,sizey):
        #self.sizex = sizex
        #self.sizey = sizey
        #self.posx = posx
        #self.posy = posy
        #self.name = "box" + str(sizex)
        #print('initializing box')
    #def top(self):
        #return Point(self.posx + self.sizex/2, self.posy)
    #def bottom(self):
        #return Point(self.posx + self.sizex/2, self.posy + self.sizey)
    #def left(self):
        #return Point(self.posx, self.posy + self.sizey/2)
    #def right(self):
        #return Point(self.posx + self.sizex, self.posy + self.sizey/2)

#class Robot:
    #def __init__(self,posx,posy,posxend,posyend):
        #self.posx = posx
        #self.posy = posy
        #self.posxend = posxend
        #self.posyend = posyend
        #self.sizex = 10
        #self.sizey = 10
        #self.name = "robot"
        #print('initializing robot')
        #def getPosition(self):
            #return [posx,posy]

#class VerticalLine:
    #def __init__(self,posx,posy1,posy2):
        #self.posx = posx
        #self.posy1 = posy1
        #self.posy2 = posy2
        #self.name = "verticalline"
    #def getMidpoint(self):
        #return [posx, (posy1-posy2)/2 + posy1]  #Double check this
    #def __repr__(self):
        #return "vline_" + str(self.posx)

#class HorizonalLine:
    #def __init__(self,posx1,posx2,posy):
        #self.posx1 = posx1
        #self.posx2 = posx2
        #self.posy = posy
        #self.name = "horizonalline"
    #def __repr__(self):
        #return "hline_" + str(self.posy)

# class PathLine:
#     def __init__(self,x1,y1, x2, y2):
#         self.x1 = x1
#         self.x2 = x2
#         self.y1 = y1
#         self.y2 = y2
#         # self.name = "path"

#     def draw(self, painter):
#         painter.setBrush(QtCore.Qt.black)
#         painter.drawLine(self.x1, self.y1, self.x2, self.y2)

#class Cell:
    #def __init__(self,posx,posy,sizex,sizey):
        #self.sizex = sizex
        #self.sizey = sizey
        #self.posx = posx
        #self.posy = posy
        #self.name = "cell"
    #def __repr__(self):
        #return "cell_[" + str(self.posx)+ "," + str(self.posy) + "]"
    #def top(self):
        #return Point(self.posx + self.sizex/2, self.posy)
    #def bottom(self):
        #return Point(self.posx + self.sizex/2, self.posy + self.sizey)
    #def left(self):
        #return Point(self.posx, self.posy + self.sizey/2)
    #def right(self):
        #return Point(self.posx + self.sizex, self.posy + self.sizey/2)
    #def isAdjacent(self,point):
        #if point == self.top() or point == self.bottom() or point == self.left() or point == self.right():
            #return True
        #else:
            #return False
            
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
        
    # def getMidpoint(self):
    #     return [self.x, (self.y1-self.y2)/2 + self.y1]
    
    def draw(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine))
        painter.drawLine(self.X + self.x, self.Y + self.y1, self.X + self.x, self.Y + self.y2)
        
class HorizontalLine(UIItem):
    def __init__(self, x1, x2, y):
        UIItem.__init__(self)
        self.x1 = x1
        self.y = y
        self.x2 = x2
        
    # def getMidpoint(self):
    #     return [self.x1 + (self.x1 - self.x2)/2, self.y]
    
    def draw(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine))
        painter.drawLine(self.X + self.x1, self.Y + self.y, self.X + self.x2, self.Y + self.y)
        
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
        
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('project5.ui', self)
        self.initUI()
        
    def initUI(self):
        #Go to functions when buttons are pressed
        self.pushButtonRobotAdd.clicked.connect(self.RobotAdd)
        self.pushButtonBlockAdd_1.clicked.connect(self.BlockAdd_1)
        self.pushButtonBlockAdd_2.clicked.connect(self.BlockAdd_2)
        self.pushButtonBlockAdd_3.clicked.connect(self.BlockAdd_3)
        self.pushButtonRemoveAll.clicked.connect(self.RemoveAll)
        self.pushButtonCalculate.clicked.connect(self.Calculate)
        self.pushButtonRemovePath.clicked.connect(self.RemovePath)
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
                # for item in items:
                #     if isinstance(item, Robot):
                #         addItem = False
                #         item.posx = posx
                #         item.posy = posy
                self.lineEditRobotX.setText(str(x))
                self.lineEditRobotY.setText(str(y))
            elif self.robotEndRadioButton.isChecked():
                if items_dict['robot'] != None:
                    addItem = False
                    items_dict['robot'].x_end = x
                    items_dict['robot'].y_end = y
                # for item in items:
                #     if isinstance(item, Robot):
                #         addItem = False
                #         item.posxend = posx
                #         item.posyend = posy
                else:
                    robot = Robot(0, 0, x, y)
                    item_dict['robot'] = robot
                    items.append(robot)

                self.lineEditRobotXend.setText(str(x))
                self.lineEditRobotYend.setText(str(y))
            elif self.block1RadioButton.isChecked():
                self.AddBlock(x, y, 200, 200, "box200")
                self.lineEditBlockX_1.setText(str(x))
                self.lineEditBlockY_1.setText(str(y))
            elif self.block2RadioButton.isChecked():
                self.AddBlock(x, y, 150, 150, "box150")
                self.lineEditBlockX_2.setText(str(x))
                self.lineEditBlockY_2.setText(str(y))
            elif self.block3RadioButton.isChecked():
                self.AddBlock(x, y, 100, 100, "box100")
                self.lineEditBlockX_3.setText(str(x))
                self.lineEditBlockY_3.setText(str(y))
            else:
                pass

        self.update()

    def RobotAdd(self):
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

    def BlockAdd_1(self):
        x = int(self.lineEditBlockX_1.text())
        y = int(self.lineEditBlockY_1.text())
        
        self.AddBlock(x, y, 200, 200, "box200")

    def BlockAdd_2(self):
        x = int(self.lineEditBlockX_2.text())
        y = int(self.lineEditBlockY_2.text())

        self.AddBlock(x,y, 150, 150, "box150")

    def BlockAdd_3(self):
        x = int(self.lineEditBlockX_3.text())
        y = int(self.lineEditBlockY_3.text())

        self.AddBlock(x, y, 100, 100, "box100")

    def AddBlock(self, x, y, sizex, sizey, obj):
        global items, items_dict

        if items_dict[obj] != None:
            items_dict[obj].x = x
            items_dict[obj].y = y
        else:
            box = Box(x, y, [sizex, sizey])
            items_dict[obj] = box

        self.update()

    def displayPathNotFound(self):
        self.pathNotFoundLabel.show()

    def removePathNotFound(self):
        self.pathNotFoundLabel.hide()

    def RemovePath(self):
        global items, items_dict
        items = [item for item in items if isinstance(item, Robot) or isinstance(item, Box)]
        items_dict['HorizontalLines'] = []
        items_dict['VerticalLines'] = []
        items_dict['Path'] = []
        self.removePathNotFound()
        self.update()

    def RemoveAll(self):
        global items, items_dict
        items_dict = {'robot': None, 'box100': None, 'box150': None, 'box200': None,
              'HorizontalLines': [], 'VerticalLines': [], 'Path': [] }
        print('Items removed')
        self.removePathNotFound()
        self.update()

    def Calculate(self):
        #Draw Vertical and Horizonal Lines
        global items, items_dict
        boxes = [items_dict['box100'], items_dict['box150'], items_dict['box200']]
        #Remove any None objects
        boxes = [box for box in boxes if box != None]
        
        # for item in items:
        #     if isinstance(item, Box):
        #         boxes.append(item)

        items_dict['VerticalLines'].append(VerticalLine(0,0,maxY))
        items_dict['VerticalLines'].append(VerticalLine(maxX,0,maxY))
        items_dict['HorizontalLines'].append(HorizontalLine(0,maxX,0))
        items_dict['HorizontalLines'].append(HorizontalLine(0,maxX,maxY))
        # items.append(VerticalLine(0,0,maxY))
        # items.append(HorizonalLine(0,maxX,0))
        # items.append(VerticalLine(maxX,0,maxY))
        # items.append(HorizonalLine(0,maxX,maxY))
        # for box in boxes:
        #     items.append(VerticalLine(box.x, 0, maxY))
        #     items.append(VerticalLine(box.x+box.size[0], 0, maxY))
        #     items.append(HorizonalLine(0, maxX, box.y))
        #     items.append(HorizonalLine(0, maxX, box.y+box.size[1]))
        for box in boxes:
            items_dict['VerticalLines'].append(VerticalLine(box.x, 0, maxY))
            items_dict['VerticalLines'].append(VerticalLine(box.x+box.size[0], 0, maxY))
            items_dict['HorizontalLines'].append(HorizontalLine(0, maxX, box.y))
            items_dict['HorizontalLines'].append(HorizontalLine(0, maxX, box.y+box.size[1]))

        #Sort Lines
        hlines = items_dict['HorizontalLines']
        vlines = items_dict['VerticalLines']

        # for item in items:
        #     if isinstance(item, HorizontalLine):
        #         hlines.append(item)
        #     if isinstance(item, VerticalLine):
        #         vlines.append(item)
        
        # sort functions
        def sort_by_x(vline):
            return vline.x

        def sort_by_y(hline):
            return hline.y

        vlines = sorted(vlines, key = sort_by_x)
        hlines = sorted(hlines, key = sort_by_y)

        #Create Cell Representations
        cells = []
        for i in range(0,len(vlines)-1):
            for j in range(0,len(hlines)-1):
                xpos = vlines[i].x
                ypos = hlines[j].y
                xsize = vlines[i+1].x - vlines[i].x
                ysize = hlines[j+1].y - hlines[j].y
                cells.append(Cell(xpos,ypos,[xsize,ysize]))
        print("Number of cells: " + str(len(cells)))

        #Remove boxes from the cell list
        for cell in cells:
            for box in boxes:
                if(cell.x == box.x and cell.y == box.y):
                    cells.remove(cell)  #Remove the cell that coincides with a box
        print("Number of cells: " + str(len(cells)))

        #Get list of midpoints
        all_cells = []
        for box in boxes:
            all_cells.append((box.getCenter(), False))
        
        for cell in cells:
            all_cells.append((cell.getCenter(), True))
        
        all_cells.sort(key = lambda x: x[0].y)
        
        board_matrix = [[all_cells[0]]]
        idx = 0
        
        for cell in all_cells[1:]:
            if cell[0].y == board_matrix[idx][0][0].y:
                board_matrix[idx].append(cell)
            else:
                idx += 1
                board_matrix.append([cell])
        
        midpoints = []
        # for item in items:  #Add robot positions to graph
        #     if isinstance(item, Robot):
        #         midpoints.append(Point(item.x,item.y))
        #         midpoints.append(Point(item.x_end,item.y_end))
        robot = items_dict['robot']
        start_point = sorted([(distance(Point(robot.x, robot.y), cell[0]), cell) for cell in all_cells], key = lambda x: x[0])[0]
        end_point = sorted([(distance(Point(robot.x_end, robot.y_end), cell[0]), cell) for cell in all_cells], key = lambda x: x[0])[0]
        print(f'Start cell: {start_point[1][0].x}, {start_point[1][0].y}')
        print(f'End cell: {end_point[1][0].x}, {end_point[1][0].y}')
        
        midpoints.append(Point(robot.x, robot.y))
        midpoints.append(Point(robot.x_end, robot.y_end))

        for point in cellmidpoints: #Remove points that touch boxes
            doesnt_touch_box = True
            for box in boxes:
                if (point.x <= (box.x+box.size[0]) and point.x >= box.x) and \
                   (point.y <= (box.y+box.size[1]) and point.y >= box.y):
                    doesnt_touch_box = False
            if doesnt_touch_box == True:
                tempmidpoints.append(point)

        for point in tempmidpoints: #Remove points that touch the boundary
            if not (point.x == 0 or point.y == 0 or point.x == maxX or point.y == maxY):
                midpoints.append(point)

        print("Final Midpoints")
        print(midpoints)
        print(len(midpoints))

        #Create the graph
        graph = generateGraph(midpoints,cells)

        #Use Dijkstras to find the shortest path
        path = shortestPath(graph,0,1)

        #Check if path connects start and end point
        if path == -1:
            self.displayPathNotFound()
            self.update()
            return

        print("Midpoints to solution:")
        for index in range(len(path) - 1):
            p = Path(midpoints[path[index]].x, midpoints[path[index]].y, midpoints[path[index+1]].x, midpoints[path[index+1]].y)
            items_dict['Path'].append(p)

        print(path)
        print('plotted')
        self.update()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

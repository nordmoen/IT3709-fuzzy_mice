#!/usr/bin/env python

import sys
import math
from PySide import QtCore, QtGui
from fuzzy_mice.mouse import Mouse
from fuzzy_mice import fuzzy_tools

import fuzzy_mice.mice_rc

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    scene = QtGui.QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

    mouse = Mouse(5, 5)
    mouse.setPos(math.sin(6.28) * 200,
                 math.cos(6.28) * 200)
    scene.addItem(mouse)
	
    mouse2 = Mouse(3, 7)
    mouse.setPos(math.sin(6.28) * 200,
                 math.cos(6.28) * 200)
    scene.addItem(mouse2)
    
    mouse3 = Mouse(7, 3)
    mouse.setPos(math.sin(6.28) * 200,
                 math.cos(6.28) * 200)
    scene.addItem(mouse3)

    view = QtGui.QGraphicsView(scene)
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    view.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(':/images/cheese.jpg')))
    view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
    view.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
    view.setWindowTitle("Colliding Mice")
    view.resize(400, 300)
    view.show()

    sys.exit(app.exec_())

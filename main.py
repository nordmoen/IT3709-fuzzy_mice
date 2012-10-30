#!/usr/bin/env python

import sys
import math
from PySide import QtCore, QtGui
from fuzzy_mice.mouse import Mouse

import fuzzy_mice.mice_rc

if __name__ == '__main__':


    MouseCount = 7

    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    scene = QtGui.QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)

    for i in range(MouseCount):
        mouse = Mouse()
        mouse.setPos(math.sin((i * 6.28) / MouseCount) * 200,
                     math.cos((i * 6.28) / MouseCount) * 200)
        scene.addItem(mouse)

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

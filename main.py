#!/usr/bin/env python

import sys
import math
import random
from PySide import QtCore, QtGui
from fuzzy_mice.mouse import Mouse
from fuzzy_mice.fuzzy_tools import parse_file
from fuzzy_mice.reasoner import FuzzyReasoner

import fuzzy_mice.mice_rc

scene = None

def fight(mouse1, mouse2):
    s1 = mouse1.rate()*random.random()
    s2 = mouse2.rate()*random.random()
    if s1 > s2:
        mouse2.hurt(mouse1.strength*random.random()*100)
    else:
        mouse1.hurt(mouse2.strength*random.random()*100)

def fight_mice():
    mice = scene.items()[:]
    for mouse in mice:
        if mouse.lastFightTime < 5:
            mouse.lastFightTime += 1
        else:
            for mouse2 in scene.collidingItems(mouse):
                if mouse2.lastFightTime < 5:
                    mouse2.lastFightTime += 1
                else:
                    if mouse2 in mice:
                        mice.remove(mouse2)
                    fight(mouse, mouse2)
                    mouse.lastFightTime = 0
                    mouse2.lastFightTime = 0
            

if __name__ == '__main__':
    mice_count = 4
    if_cond, action_sets = parse_file('fuzzy_rules.txt')
    reason = FuzzyReasoner(if_cond, action_sets, range(201))
    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    scene = QtGui.QGraphicsScene()
    scene.setSceneRect(-300, -300, 600, 600)
    scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
    scene.changed.connect(fight_mice)

    for i in range(mice_count):
        mouse = Mouse(random.random(), random.randint(4, 10), reason)
        mouse.setPos(math.sin(6.28*random.random()) * 200,
                     math.cos(6.28*random.random()) * 200)
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

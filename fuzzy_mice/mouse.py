#!/usr/bin/python

import math
import random
from PySide import QtGui, QtCore

class Mouse(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    # Create the bounding rectangle once.
    adjust = 0.3
    BoundingRect = QtCore.QRectF(-20 - adjust, -22 - adjust, 40 + adjust,
            83 + adjust)

    def __init__(self, strength, speed, reasoner):
        '''Strength = [0, 100], speed = [1, 5]'''
        super(Mouse, self).__init__()

        self.strength = strength
        self.speed = speed
        self.reasoner = reasoner
        self.health = 100
        self.angle = 0.0
        self.setScale(1)
        self.mouseEyeDirection = 0.0
        self.color = QtGui.QColor(0.0,255,0.0)

        self.rotate(QtCore.qrand() % (360 * 16))

        # In the C++ version of this example, this class is also derived from
        # QObject in order to receive timer events.  PyQt does not support
        # deriving from more than one wrapped class so we just create an
        # explicit timer instead.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000 / 33)

    @staticmethod
    def normalizeAngle(angle):
        while angle < 0:
            angle += Mouse.TwoPi
        while angle > Mouse.TwoPi:
            angle -= Mouse.TwoPi
        return angle

    def boundingRect(self):
        return Mouse.BoundingRect

    def paint(self, painter, option, widget):
        # Body.
        painter.setBrush(self.color)
        painter.drawEllipse(-10, -20, 20, 40)

        # Eyes.
        painter.setBrush(QtCore.Qt.white)
        painter.drawEllipse(-10, -17, 8, 8)
        painter.drawEllipse(2, -17, 8, 8)


        # Nose.
        painter.setBrush(QtCore.Qt.black)
        painter.drawEllipse(QtCore.QRectF(-2, -22, 4, 4))

        # Pupils.
        painter.drawEllipse(QtCore.QRectF(-8.0 + self.mouseEyeDirection, -17, 4, 4))
        painter.drawEllipse(QtCore.QRectF(4.0 + self.mouseEyeDirection, -17, 4, 4))

        # Ears.
        if self.scene().collidingItems(self):
            painter.setBrush(QtCore.Qt.red)
        else:
            painter.setBrush(QtCore.Qt.darkYellow)

        painter.drawEllipse(-17, -12, 16, 16)
        painter.drawEllipse(1, -12, 16, 16)

        # Tail.
        path = QtGui.QPainterPath(QtCore.QPointF(0, 20))
        path.cubicTo(-5, 22, -5, 22, 0, 25)
        path.cubicTo(5, 27, 5, 32, 0, 30)
        path.cubicTo(-5, 32, -5, 42, 0, 35)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(path)

    def timerEvent(self):
        if self.health < 0.0:
            self.speed = 0
        else:
            # Don't move too far away.
            lineToCenter = QtCore.QLineF(QtCore.QPointF(0, 0), self.mapFromScene(0, 0))
            if lineToCenter.length() > 150:
                angleToCenter = math.acos(lineToCenter.dx() / lineToCenter.length())
                if lineToCenter.dy() < 0:
                    angleToCenter = Mouse.TwoPi - angleToCenter;
                angleToCenter = Mouse.normalizeAngle((Mouse.Pi - angleToCenter) + Mouse.Pi / 2)

                if angleToCenter < Mouse.Pi and angleToCenter > Mouse.Pi / 4:
                    # Rotate left.
                    self.angle += [-0.25, 0.25][self.angle < -Mouse.Pi / 2]
                elif angleToCenter >= Mouse.Pi and angleToCenter < (
                        Mouse.Pi + Mouse.Pi / 2 + Mouse.Pi / 4):
                    # Rotate right.
                    self.angle += [-0.25, 0.25][self.angle < Mouse.Pi / 2]
            elif math.sin(self.angle) < 0:
                self.angle += 0.25
            elif math.sin(self.angle) > 0:
                self.angle -= 0.25

            height = 100*-1
            x = (math.sqrt(3) / 2) * (2*height)
            # Try not to crash with any other mice.
            dangerMice = self.scene().items(QtGui.QPolygonF([self.mapToScene(0, 0),
                                                             self.mapToScene(x, height),
                                                             self.mapToScene(-x, height)]))

            two_worst = [None, None]
            two_worst_rate = [0, 0]
            for item in dangerMice:
                if item is self:
                    continue
                for i in range(len(two_worst)):
                    if item.rate() > two_worst_rate[i]:
                        two_worst[i] = item
                        two_worst_rate[i] = item.rate()
                        break

            for mouse in two_worst:
                if mouse != None:
                    dist = math.sqrt((mouse.scenePos().x() - self.scenePos().x())**2 +
                            (mouse.scenePos().y() - self.scenePos().y())**2)
                    rate1 = mouse.rate()
                    action = self.reasoner.eval(distance=dist, rate=rate1, health=self.health)

            dx = math.sin(self.angle) * 10
            self.mouseEyeDirection = [dx / 5, 0.0][QtCore.qAbs(dx / 5) < 1]

            self.rotate(dx)
            self.setPos(self.mapToParent(0, -(self.speed)))

    def hurt(self, amount):
        self.health -= amount
        scale = self.health / 100.0
        if scale < 0.5:
            scale = 0.5
        self.setScale(scale)
        self.update_color()
        if self.health < 0.0:
            self.timer.stop()
            self.scene().removeItem(self)

    def update_color(self):
        red = (100 - self.health) / 100.0
        green = self.health / 100.0
        if red > 1.0:
            red = 1.0
        if green < 0.0:
            green = 0.0
        self.color = QtGui.QColor(red*255,green*255,0.0)

    def rate(self):
        return self.health + self.strength

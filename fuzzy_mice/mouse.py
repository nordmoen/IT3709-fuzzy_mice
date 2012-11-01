#!/usr/bin/python

import math
from PySide import QtGui, QtCore

class Mouse(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    # Create the bounding rectangle once.
    adjust = 0.5
    BoundingRect = QtCore.QRectF(-20 - adjust, -22 - adjust, 40 + adjust,
            83 + adjust)

    def __init__(self, strength, speed):
        super(Mouse, self).__init__()

        self.strength = strength
        self.speed = speed
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
        self.hurt(0.3)
        if self.health == 0.0:
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
                elif angleToCenter >= Mouse.Pi and angleToCenter < (Mouse.Pi + Mouse.Pi / 2 + Mouse.Pi / 4):
                    # Rotate right.
                    self.angle += [-0.25, 0.25][self.angle < Mouse.Pi / 2]
            elif math.sin(self.angle) < 0:
                self.angle += 0.25
            elif math.sin(self.angle) > 0:
                self.angle -= 0.25

            # Try not to crash with any other mice.
            dangerMice = self.scene().items(QtGui.QPolygonF([self.mapToScene(0, 0),
                                                             self.mapToScene(-30, -50),
                                                             self.mapToScene(30, -50)]))

            for item in dangerMice:
                if item is self:
                    continue

                lineToMouse = QtCore.QLineF(QtCore.QPointF(0, 0), self.mapFromItem(item, 0, 0))
                
                if lineToMouse.length() == 0:
                    angleToMouse = 0
                else:
                    angleToMouse = math.acos(lineToMouse.dx() / lineToMouse.length())
                
                if lineToMouse.dy() < 0:
                    angleToMouse = Mouse.TwoPi - angleToMouse
                angleToMouse = Mouse.normalizeAngle((Mouse.Pi - angleToMouse) + Mouse.Pi / 2)

                if angleToMouse >= 0 and angleToMouse < Mouse.Pi / 2:
                    # Rotate right.
                    self.angle += 0.5
                elif angleToMouse <= Mouse.TwoPi and angleToMouse > (Mouse.TwoPi - Mouse.Pi / 2):
                    # Rotate left.
                    self.angle -= 0.5

            # Add some random movement.
            if len(dangerMice) > 1 and (QtCore.qrand() % 10) == 0:
                if QtCore.qrand() % 1:
                    self.angle += (QtCore.qrand() % 100) / 500.0
                else:
                    self.angle -= (QtCore.qrand() % 100) / 500.0

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
        if self.health <= 0.0:
            self.health = 0.0
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

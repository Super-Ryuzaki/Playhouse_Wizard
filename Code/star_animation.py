import random
import math
from PyQt5.QtCore import Qt, QTimer, QPoint, QPointF
from PyQt5.QtGui import QPainter, QColor, QCursor, QPolygonF
from PyQt5.QtWidgets import QWidget


class FairyDustParticle:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.velocity = QPointF(random.uniform(-1.5, 1.5), random.uniform(1, 2))
        self.alpha = 255
        self.size = random.randint(3, 6)

    def update(self):
        self.position += self.velocity
        self.alpha -= 5
        if self.alpha <= 0:
            self.alpha = 0

    def isFadedOut(self):
        return self.alpha == 0


class FairyDustAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(16)  # 60 FPS
        
        self.particles = []

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawFairyDust(painter)

    def drawFairyDust(self, painter):
        background_color = self.palette().color(self.backgroundRole())
        fairy_color = QColor(255 - background_color.red(),
                             255 - background_color.green(),
                             255 - background_color.blue())

        for particle in self.particles:
            painter.setPen(Qt.NoPen)
            particle_color = QColor(fairy_color.red(), fairy_color.green(), fairy_color.blue(), particle.alpha)
            painter.setBrush(particle_color)

            # Draw star-shaped polygons
            points = []
            num_points = 5
            outer_radius = particle.size
            inner_radius = particle.size // 2

            angle = 2 * math.pi / num_points
            start_angle = -math.pi / 2

            for i in range(num_points * 2):
                radius = outer_radius if i % 2 == 0 else inner_radius
                x = particle.position.x() + radius * (1 + 0.6 * (i % 2)) * math.cos(start_angle + angle * i)
                y = particle.position.y() + radius * (1 + 0.6 * (i % 2)) * math.sin(start_angle + angle * i)
                points.append(QPointF(x, y))

            painter.drawPolygon(QPolygonF(points))

    def updateAnimation(self):
        self.generateFairyDust()
        self.updateParticles()
        self.repaint()

    def generateFairyDust(self):
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        particle_pos = QPoint(cursor_pos.x() + 9, cursor_pos.y() + 20)
        self.particles.append(FairyDustParticle(particle_pos, self.palette().color(self.backgroundRole())))

    def updateParticles(self):
        for particle in self.particles:
            particle.update()
        self.particles = [particle for particle in self.particles if not particle.isFadedOut()]

    def mouseMoveEvent(self, event):
        self.update()

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

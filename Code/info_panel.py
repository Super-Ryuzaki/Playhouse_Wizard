
from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class InfoPanel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hibp_window = None
        self.speedtest_window = None
        self.pc_specs_window = None 

        # Set font properties
        font = QFont("Arial", 14)  # Customize the font and size as desired
        self.setFont(font)

        # Create a layout to hold the child windows
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(self.rect())
        super().paintEvent(event)

    def setHIBPWindow(self, hibp_window):
        if self.hibp_window is not None:
            self.hibp_window.hide()  # Hide the current hibp window
            self.layout.removeWidget(self.hibp_window)
        self.hibp_window = hibp_window
        self.layout.addWidget(self.hibp_window)

    def setSpeedTestWindow(self, speedtest_window):
        if self.speedtest_window is not None:
            self.speedtest_window.hide()  # Hide the current speedtest window
            self.layout.removeWidget(self.speedtest_window)
        self.speedtest_window = speedtest_window
        self.layout.addWidget(self.speedtest_window)
        
    def setPcSpecsWindow (self, pc_specs_window):
        if self.pc_specs_window is not None:
            self.pc_specs_window.hide() # Hide the current Pc Specs window
            self.layout.removeWidget(self.pc_specs_window)
        self.pc_specs_window = pc_specs_window
        self.layout.addWidget(self.pc_specs_window)

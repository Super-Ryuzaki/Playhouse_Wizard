import threading
import platform
import socket
import psutil
from requests import get
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont

class PcSpecsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: transparent")
        self.setWindowTitle("PlayHouse Wizard")
        self.setFont(QFont('Trajan', 12))

        self.init_gui()

    def init_gui(self):
        # Create labels for displaying system specs
        self.fetching_data_label = QLabel("Fetching Data...", self)
        self.platform_system_label = QLabel("Operating System: ", self)
        self.platform_version_label = QLabel("Version: ", self)
        self.platform_platform_label = QLabel("Platform: ", self)
        self.platform_machine_label = QLabel("Architecture: ", self)
        self.platform_processor_label = QLabel("Processor: ", self)
        self.ram_label = QLabel("RAM: ", self)
        self.local_ip_label = QLabel("Local IP: ", self)
        self.pub_ip_label = QLabel("Public IP: ", self)

        # Position labels
        self.fetching_data_label.setGeometry(10, 10, 450, 25)
        self.platform_system_label.setGeometry(10, 40, 450, 25)
        self.platform_version_label.setGeometry(10, 70, 450, 25)
        self.platform_platform_label.setGeometry(10, 100, 450, 25)
        self.platform_machine_label.setGeometry(10, 130, 450, 25)
        self.platform_processor_label.setGeometry(10, 160, 450, 25)
        self.ram_label.setGeometry(10, 190, 450, 25)
        self.local_ip_label.setGeometry(10, 220, 450, 25)
        self.pub_ip_label.setGeometry(10, 250, 450, 25)

        # Set label styles
        self.set_label_style(self.fetching_data_label)
        self.set_label_style(self.platform_system_label)
        self.set_label_style(self.platform_version_label)
        self.set_label_style(self.platform_platform_label)
        self.set_label_style(self.platform_machine_label)
        self.set_label_style(self.platform_processor_label)
        self.set_label_style(self.ram_label)
        self.set_label_style(self.local_ip_label)
        self.set_label_style(self.pub_ip_label)

        # Hide system specs labels initially
        self.hide_system_specs_labels()

        # Get PC specs in a separate thread
        threading.Thread(target=self.get_pc_specs, daemon=True).start()

    def set_label_style(self, label):
        label.setStyleSheet("color: white")
        label.setFont(QFont('Trajan', 11))

    def get_pc_specs(self):
        # Show "Fetching Data" label
        self.fetching_data_label.setVisible(True)

        # Fetch PC specifications
        platform_system = platform.system()
        platform_version = platform.version()
        platform_platform = platform.platform()
        platform_machine = platform.machine()
        platform_processor = platform.processor()
        ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3)))
        local_ip = socket.gethostbyname(socket.gethostname())
        pub_ip = get('https://api.ipify.org').text

        # Update labels with the fetched data
        self.platform_system_label.setText("Operating System: " + platform_system)
        self.platform_version_label.setText("Version: " + platform_version)
        self.platform_platform_label.setText("Platform: " + platform_platform)
        self.platform_machine_label.setText("Architecture: " + platform_machine)
        self.platform_processor_label.setText("Processor: " + platform_processor)
        self.ram_label.setText("RAM: " + ram + " GB")
        self.local_ip_label.setText("Local IP: " + local_ip)
        self.pub_ip_label.setText("Public IP: " + pub_ip)

        # Reposition labels (in case text length has changed)
        self.reposition_labels()

        # Hide "Fetching Data" label
        self.fetching_data_label.setVisible(False)

        # Show system specs labels
        self.show_system_specs_labels()

    def hide_system_specs_labels(self):
        # Hide system specs labels
        labels = [
            self.platform_system_label,
            self.platform_version_label,
            self.platform_platform_label,
            self.platform_machine_label,
            self.platform_processor_label,
            self.ram_label,
            self.local_ip_label,
            self.pub_ip_label
        ]
        for label in labels:
            label.setVisible(False)

    def show_system_specs_labels(self):
        # Show system specs labels
        labels = [
            self.platform_system_label,
            self.platform_version_label,
            self.platform_platform_label,
            self.platform_machine_label,
            self.platform_processor_label,
            self.ram_label,
            self.local_ip_label,
            self.pub_ip_label
        ]
        for label in labels:
            label.setVisible(True)

    def reposition_labels(self):
        label_y = 40
        label_height = 30

        # Adjust the position of each label
        labels = [
            self.platform_system_label,
            self.platform_version_label,
            self.platform_platform_label,
            self.platform_machine_label,
            self.platform_processor_label,
            self.ram_label,
            self.local_ip_label,
            self.pub_ip_label
        ]

        for label in labels:
            label.setGeometry(label.x(), label_y, label.width(), label_height)
            label_y += label_height

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_labels()

if __name__ == "__main__":
    app = QApplication([])
    window = PcSpecsWindow()
    window.show()
    app.exec()

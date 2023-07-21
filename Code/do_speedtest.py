from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QMovie
from PyQt5 import QtWidgets, QtCore
import speedtest


class SpeedTestWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(float, float)
    error = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run_speedtest(self):
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 10**6  # Convert to Mbps
            upload_speed = st.upload() / 10**6  # Convert to Mbps
            self.finished.emit(download_speed, upload_speed)
        except Exception as e:
            self.error.emit(str(e))


class SpeedTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: transparent;")
        self.setWindowTitle("Assistant")
        self.setFont(QFont('Trajan', 12))

        self.download_speed_holder = "-"
        self.upload_speed_holder = "-"
        self.speedtest_running_label = None  # Store reference to the label

        self.speedtest_ui()

    def speedtest_ui(self):
        self.download_speed_label = QLabel("Download speed: " + self.download_speed_holder, self)
        self.download_speed_label.setStyleSheet("color: white")
        self.download_speed_label.setGeometry(10, 10, 450, 25)
        self.download_speed_label.setFont(QFont('Trajan', 11))

        self.upload_speed_label = QLabel("Upload speed: " + self.upload_speed_holder, self)
        self.upload_speed_label.setStyleSheet("color: white")
        self.upload_speed_label.setGeometry(10, 40, 450, 25)
        self.upload_speed_label.setFont(QFont('Trajan', 11))

        self.start_speedtest_button = QPushButton("Start Speedtest", self)
        self.start_speedtest_button.setGeometry(95, 80, 210, 30)
        self.start_speedtest_button.setStyleSheet("background-color: transparent; color: #FFFFFF; font-size: 14px; border: 2px solid #0066CC; border-radius: 5px;")
        self.start_speedtest_button.clicked.connect(self.start_speedtest)
        self.start_speedtest_button.setFont(QFont('Trajan'))

        # Add a loading spinner
        self.loading_spinner = QLabel(self)
        self.loading_spinner.setGeometry(180, 150, 40, 40)
        self.loading_spinner_movie = QMovie("spinner.gif")
        self.loading_spinner.setMovie(self.loading_spinner_movie)

    def start_speedtest(self):
        self.start_speedtest_button.setEnabled(False)
        self.show_speedtest_running_label()  # Show the "Speedtest Running" label
        self.loading_spinner_movie.start()  # Start the loading spinner animation

        self.worker = SpeedTestWorker()
        self.worker.finished.connect(self.handle_speedtest_result)
        self.worker.error.connect(self.handle_speedtest_error)

        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)  # Quit the thread if an error occurs
        self.worker_thread.started.connect(self.worker.run_speedtest)
        self.worker_thread.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.hide_speedtest_running_label)  # Hide the label when speedtest finishes
        self.worker_thread.finished.connect(self.loading_spinner_movie.stop)  # Stop the loading spinner animation
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()

    def show_speedtest_running_label(self):
        self.speedtest_running_label = QLabel("Speedtest Running", self)
        self.speedtest_running_label.setStyleSheet("color: white; font-size: 24px")
        self.speedtest_running_label.setGeometry(10, 160, 380, 60)
        self.speedtest_running_label.setAlignment(QtCore.Qt.AlignCenter)
        self.speedtest_running_label.show()

    def hide_speedtest_running_label(self):
        if self.speedtest_running_label is not None:
            self.speedtest_running_label.hide()
            self.speedtest_running_label.deleteLater()
            self.speedtest_running_label = None

    def handle_speedtest_result(self, download_speed, upload_speed):
        self.download_speed_holder = "{:.2f}".format(download_speed)
        self.upload_speed_holder = "{:.2f}".format(upload_speed)
        self.download_speed_label.setText("Download speed: " + (str(self.download_speed_holder) + " Mbps"))
        self.upload_speed_label.setText("Upload speed: " + (str(self.upload_speed_holder) + " Mbps"))
        self.download_speed_label.adjustSize()
        self.upload_speed_label.adjustSize()
        self.start_speedtest_button.setEnabled(True)

    def handle_speedtest_error(self, error_message):
        self.start_speedtest_button.setEnabled(True)
        self.hide_speedtest_running_label()
        self.loading_spinner_movie.stop()

        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Speedtest Error")
        error_box.setText("An error occurred during the speed test.")
        error_box.setInformativeText(error_message)
        error_box.exec()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = SpeedTestWindow()
    window.show()
    sys.exit(app.exec())

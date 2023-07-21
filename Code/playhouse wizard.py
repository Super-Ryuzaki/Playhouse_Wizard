import sys
import subprocess

from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QPushButton,
        QVBoxLayout,
        QHBoxLayout,
        QLineEdit,
        QListWidget,
        QListWidgetItem,
        QLabel,
    )
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt

from star_animation import FairyDustAnimation
import software_list
import filters
import hibp
import install_soft
from info_panel import InfoPanel
import do_speedtest
import pc_specs

class CustomButton(QPushButton):
    def enterEvent(self, event):
        self.parentWidget().fairy_dust_animation.enterEvent(event)

    def leaveEvent(self, event):
        self.parentWidget().fairy_dust_animation.leaveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PlayHouse Wizard")
        self.setFixedSize(800, 600)  # Set window size to 800x600

        # Customized Background
        self.set_background()

        self.fairy_dust_animation = FairyDustAnimation(self)

        # Create a layout and set the animation widget as its central widget
        layout = QVBoxLayout()
        layout.addWidget(self.fairy_dust_animation)

        # Set the layout as the central widget of the main window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Buttons
        self.create_elements()

        # Available options
        self.options = software_list.soft_list

        # Initialize options
        self.initialize_options()

        # Disable maximize and minimize buttons
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        # Layout for info panel and hibp/speedtest windows
        self.info_layout = QVBoxLayout()

    def set_background(self):
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(25, 25, 25))  # Customize the RGB values as desired
        self.setPalette(palette)

    def create_elements(self):
        # Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setGeometry(10, 10, 200, 30)
        self.search_bar.setStyleSheet("QLineEdit { background-color: transparent; color: #FFFFFF; }")  # Change color to white
        self.search_bar.textChanged.connect(self.update_options)

        # Filter Button
        self.filter_button = QPushButton(self)
        self.filter_button.setGeometry(220, 10, 60, 30)
        self.filter_button.setText("Filters")
        self.filter_button.setIconSize(self.filter_button.size())
        self.filter_button.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #FFFFFF; color: #FFFFFF; font-weight: bold; }")
        self.filter_button.clicked.connect(self.filter_button_clicked)

        # Panel with options
        self.search_panel = QListWidget(self)
        self.search_panel.setGeometry(10, 50, 200, 540)  # Adjusted height to fit the available space
        self.search_panel.setStyleSheet("QListWidget { background-color: transparent; color: #FFFFFF; }")  # Change text color to white
        self.search_panel.itemClicked.connect(self.option_clicked)

        # Info Panel
        self.info_panel = InfoPanel(self)
        self.info_panel.setGeometry(220, 50, 570, 540)  # Adjusted width and height to fit the available space
        self.info_panel.setStyleSheet("QLabel { background-color: transparent; color: #FFFFFF; }")  # Change text color to white

        # Application Name Label
        self.app_name_label = QLabel(self)
        self.app_name_label.setGeometry(290, 60, 300, 30)
        self.app_name_label.setStyleSheet("QLabel { background-color: transparent; color: #FFFFFF; font-size: 14px; font-weight: bold; }")

        # Install Button
        self.install_button = QPushButton("Install", self)
        self.install_button.setGeometry(290, 10, 80, 30)
        self.install_button.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #FFFFFF; color: #FFFFFF; font-weight: bold; }")
        self.install_button.clicked.connect(lambda: install_soft.install_button_clicked(self))

    def open_script_window(self, script_name):
        subprocess.Popen(["python", script_name])

    def initialize_options(self):
        self.search_panel.clear()
        sorted_options = sorted(self.options, key=lambda x: x["Software title"])
        for option in sorted_options:
            item = QListWidgetItem(option["Software title"], self.search_panel)
            if option.get("Checkbox") == "Yes":
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if option.get("Checked", False):
                    item.setCheckState(Qt.Checked)  # Set the checkbox state based on the "Checked" key
                else:
                    item.setCheckState(Qt.Unchecked)
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)

    def update_options(self, search_text):
        self.search_panel.clear()
        filtered_options = [
            option for option in self.options if search_text.lower() in option["Software title"].lower()
        ]
        sorted_options = sorted(filtered_options, key=lambda x: x["Software title"])
        for option in sorted_options:
            item = QListWidgetItem(option["Software title"], self.search_panel)
            if option.get("Checkbox") == "Yes":
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if option.get("Checked", False):
                    item.setCheckState(Qt.Checked)  # Set the checkbox state based on the "Checked" key
                else:
                    item.setCheckState(Qt.Unchecked)
            else:
                item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)

    def option_clicked(self, item):
        selected_option = next(
            (option for option in self.options if option["Software title"] == item.text()), None
        )

        if selected_option:
            # Update the "Checked" status based on the checkbox state
            selected_option["Checked"] = item.checkState() == Qt.Checked

            # Hide the hibp window if it's currently visible
            if self.info_panel.hibp_window is not None and self.info_panel.hibp_window.isVisible():
                self.info_panel.hibp_window.hide()

            # Hide the speedtest window if it's currently visible
            if self.info_panel.speedtest_window is not None and self.info_panel.speedtest_window.isVisible():
                self.info_panel.speedtest_window.hide()

            # Hide the pc_specs window if it's currently visible
            if self.info_panel.pc_specs_window is not None and self.info_panel.pc_specs_window.isVisible():
                self.info_panel.pc_specs_window.hide()

            info_text = f"Software: {selected_option['Software title']}\n"
            info_text += f"OS Available: {', '.join(selected_option['OS Available'])}\n"
            info_text += f"Category: {selected_option['Category']}"
            self.info_panel.setText(info_text)
            self.app_name_label.setText(selected_option['Software title'])

            if selected_option.get("Got_Window") == "Yes":
                self.info_panel.setText("")  # Clear the info panel
                script_name = selected_option.get("Script")
                if script_name:
                    if script_name == "hibp.py":
                        if self.info_panel.hibp_window is None:
                            # Call the hibp.py script and display its GUI in the info panel
                            self.info_panel.hibp_window = hibp.MainWindow()
                            self.info_panel.hibp_window.setParent(self.info_panel)
                            self.info_panel.hibp_window.setGeometry(self.info_panel.rect())
                            self.info_panel.setHIBPWindow(self.info_panel.hibp_window)
                        self.info_panel.hibp_window.show()

                    elif script_name == "speedtest.py":
                        if self.info_panel.speedtest_window is None:
                            # Call the speedtest.py script and display its GUI in the info panel
                            self.info_panel.speedtest_window = do_speedtest.SpeedTestWindow()
                            self.info_panel.speedtest_window.setParent(self.info_panel)
                            self.info_panel.speedtest_window.setGeometry(self.info_panel.rect())
                            self.info_panel.setSpeedTestWindow(self.info_panel.speedtest_window)
                        self.info_panel.speedtest_window.show()

                    elif script_name == "pc_specs.py":
                        if self.info_panel.pc_specs_window is None:
                            self.info_panel.pc_specs_window = pc_specs.PcSpecsWindow()
                            self.info_panel.pc_specs_window.setParent(self.info_panel)
                            self.info_panel.pc_specs_window.setGeometry(self.info_panel.rect())
                            self.info_panel.setPcSpecsWindow(self.info_panel.pc_specs_window)
                        self.info_panel.pc_specs_window.show()

                    else:
                        self.open_script_window(script_name)
        else:
            self.info_panel.setText("")
            self.app_name_label.setText("")
            # Hide the hibp window if it's currently visible
            if self.info_panel.hibp_window is not None and self.info_panel.hibp_window.isVisible():
                self.info_panel.hibp_window.hide()
            # Hide the speedtest window if it's currently visible
            if self.info_panel.speedtest_window is not None and self.info_panel.speedtest_window.isVisible():
                self.info_panel.speedtest_window.hide()
            # Hide the pc specs window if it's currently visible
            if self.info_panel.pc_specs_window is not None and self.info_panel.pc_specs_window.isVisible():
                self.info_panel.pc_specs_window.hide()

    def update_filtered_options(self, selected_categories):
        filtered_options = [
            option for option in software_list.soft_list if option["Category"] in selected_categories
        ]
        self.options = filtered_options
        self.initialize_options()

    def filter_button_clicked(self):
        filter_dialog = filters.FilterWindow(self)
        filter_dialog.filterSelected.connect(self.update_filtered_options)

        # Calculate the position for the filter dialog
        button_geometry = self.filter_button.geometry()
        dialog_x = self.mapToGlobal(button_geometry.bottomRight()).x()
        dialog_y = self.mapToGlobal(button_geometry.bottomRight()).y()

        filter_dialog.move(dialog_x, dialog_y)
        filter_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setFixedSize(800, 600)  # Set fixed window size
    mainWindow.show()
    sys.exit(app.exec_())

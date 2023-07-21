import platform
import os
import requests
import subprocess
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QProgressDialog, QApplication


class DownloadWorker(QThread):
    progress_updated = pyqtSignal(int)

    def __init__(self, url, destination, software_name):
        super().__init__()
        self.url = url
        self.destination = destination
        self.software_name = software_name

    def run(self):
        try:
            session = requests.Session()
            response = session.get(self.url, stream=True)
            total_size = int(response.headers.get("content-length", 0))

            with open(self.destination, "wb") as f:
                downloaded_size = 0
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    downloaded_size += len(data)
                    progress = int((downloaded_size / total_size) * 100)
                    self.progress_updated.emit(progress)
        except Exception as e:
            print(f"Error occurred during download of {self.software_name}: {str(e)}")
        finally:
            session.close()


class InstallThread(QThread):
    progress_updated = pyqtSignal(int)
    progress_message = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, selected_options):
        super().__init__()
        self.selected_options = selected_options
        self.is_running = False  # Flag to track if the thread is already running

    def run(self):
        if self.is_running:  # Check if the thread is already running
            return

        self.is_running = True  # Set the flag to indicate that the thread is running

        system_bit = platform.architecture()[0]

        folder_path = os.path.join(os.path.dirname(__file__), "playhouse_wizard")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for index, selected_option in enumerate(self.selected_options):
            app_name = selected_option["Software title"]
            link = selected_option.get("Generic link")
            bit_link = None
            software_name = selected_option.get("Software_name:")
            software_type = selected_option.get("Software_type:")
            special_command = selected_option.get("Special_Command:")
            special_command_exists = selected_option.get("Special_command_exists:")

            if system_bit == "64bit" and "64-bit link:" in selected_option:
                bit_link = selected_option.get("64-bit link:")
            elif system_bit == "32bit" and "32-bit link:" in selected_option:
                bit_link = selected_option.get("32-bit link:")
            elif "Generic link:" in selected_option:
                bit_link = selected_option.get("Generic link:")

            if software_name:
                download_path = os.path.join(folder_path, software_name)
                if bit_link:
                    download_link = bit_link
                else:
                    download_link = link

                if download_link:
                    try:
                        self.progress_message.emit(f"Now Downloading: {app_name}")
                        self.progress_updated.emit(index)
                        progress_worker = DownloadWorker(download_link, download_path, software_name)
                        progress_worker.start()
                        progress_worker.progress_updated.connect(self.progress_updated.emit)
                        progress_worker.wait()

                        if software_type == "msi":
                            install_command = f"cd {folder_path} && msiexec /i {software_name} /qn"
                        elif special_command_exists == "Yes" and software_type == "exe":
                            install_command = f"cd {folder_path} && {special_command} "
                        elif software_type == "exe":
                            install_command = f"cd {folder_path} && {software_name} /S"

                        else:
                            print(f"Unsupported software type for '{app_name}'. Skipping installation.")
                            continue

                        subprocess.run(install_command, shell=True)

                        self.progress_updated.emit(index + 1)
                    except Exception as e:
                        print(f"Error occurred during installation of {software_name}: {str(e)}")
            else:
                print(f"No software name specified for '{app_name}'. Skipping download and installation.")

        self.is_running = False  # Reset the flag to indicate that the thread has finished
        self.finished.emit()


def install_button_clicked(main_window):
    selected_options = []

    for option in main_window.options:
        if option.get("Checkbox") == "Yes" and option.get("Checked"):
            selected_options.append(option)
            if option.get("Got_Window") == "Yes":
                main_window.info_panel.setText("")  # Clear the info panel
                script_name = option.get("Script")
                if script_name:
                    main_window.open_script_window(script_name)

    if selected_options:
        dialog = QProgressDialog("Downloading", "Cancel", 0, len(selected_options))
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowTransparentForInput)

        dialog.setWindowTitle("Download Progress")
        dialog.setAutoClose(True)
        dialog.setMinimumDuration(0)
        dialog.show()

        # Check if the install thread is already running
        install_thread = getattr(main_window, "install_thread", None)
        if install_thread is None or not install_thread.isRunning():
            # If the install thread is not running, create a new one
            install_thread = InstallThread(selected_options)
            main_window.install_thread = install_thread

            install_thread.progress_updated.connect(dialog.setValue)
            install_thread.progress_message.connect(dialog.setLabelText)
            install_thread.finished.connect(lambda: dialog.setLabelText("All software installed"))
            dialog.canceled.connect(install_thread.quit)
            dialog.canceled.connect(install_thread.wait)

            install_thread.start()
        else:
            # If the install thread is already running, do nothing
            print("Installation is already in progress.")
    else:
        print("No software selected for download and installation.")


# Create an instance of QApplication to run the progress dialog
app = QApplication([])

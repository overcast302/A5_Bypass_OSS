import sys
import os
import time
import shutil
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.afc import AfcService
from pymobiledevice3.services.diagnostics import DiagnosticsService

SUPPORTED_DEVICES = {
    'iPhone4,1',
    'iPad2,1', 'iPad2,2', 'iPad2,3', 'iPad2,4',
    'iPad2,5', 'iPad2,6', 'iPad2,7',
    'iPad3,1', 'iPad3,2', 'iPad3,3',
    'iPod5,1'
}

SUPPORTED_VERSIONS = {'8.4.1', '9.3.5', '9.3.6'}

SERVER_URL = ""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def wait_for_device(self):
        self.status_update.emit("Waiting for device to return...")
        while True:
            try:
                lockdown = create_using_usbmux()
                if lockdown.get_value(key='ProductType'):
                    return lockdown
            except Exception:
                time.sleep(1)

    def run(self):
        temp_payload = None
        try:
            lockdown = create_using_usbmux()
            
            activation_state = lockdown.get_value(key='ActivationState')
            if activation_state == 'Activated':
                self.finished.emit("Device is already activated")
                return

            product = lockdown.get_value(key='ProductType')
            if product not in SUPPORTED_DEVICES:
                self.finished.emit(f"{product} is not A5")
                return

            version = lockdown.get_value(key='ProductVersion')
            if version not in SUPPORTED_VERSIONS:
                self.finished.emit(f"iOS {version} is not supported.")
                return

            self.status_update.emit("Activating device...")

            payload_path = resource_path('payload')
            temp_payload = payload_path + '.tmp'
            shutil.copy2(payload_path, temp_payload)

            conn = sqlite3.connect(temp_payload)
            cursor = conn.cursor()
            cursor.execute("UPDATE asset SET url = ? WHERE pid = 1234567893", (SERVER_URL,))
            conn.commit()
            conn.close()

            with AfcService(lockdown=lockdown) as afc:
                afc.set_file_contents(
                    'Downloads/downloads.28.sqlitedb',
                    open(temp_payload, 'rb').read()
                )
            
            DiagnosticsService(lockdown=lockdown).restart()
            time.sleep(10)
            
            lockdown = self.wait_for_device()

            diag = DiagnosticsService(lockdown=lockdown)
            
            gestalt = diag.mobilegestalt(keys=['ShouldHactivate'])
            should_hactivate = gestalt.get('ShouldHactivate')

            if should_hactivate is False:
                for i in range(5):
                    self.status_update.emit(f"Fixing activation (Attempt {i+1}/5)...")
                    
                    with AfcService(lockdown=lockdown) as afc:
                        afc.set_file_contents(
                            'Downloads/downloads.28.sqlitedb',
                            open(temp_payload, 'rb').read()
                        )
                    
                    diag.restart()
                    time.sleep(10) 
                    
                    lockdown = self.wait_for_device()
                    
                    diag = DiagnosticsService(lockdown=lockdown)
                    gestalt = diag.mobilegestalt(keys=['ShouldHactivate'])
                    should_hactivate = gestalt.get('ShouldHactivate')
                    
                    if should_hactivate is not False:
                        break
                
                if should_hactivate is False:
                    self.error.emit("Activation failed after multiple attempts. Make sure the device is connected to the Wi-Fi.")
                    return
                
            DiagnosticsService(lockdown=lockdown).restart()
            self.finished.emit("Done!")

            if temp_payload and os.path.exists(temp_payload):
                os.remove(temp_payload)

        except Exception as e:
            if temp_payload and os.path.exists(temp_payload):
                os.remove(temp_payload)
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A5 Bypass OSS v1.0.1")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status_label = QLabel("No device connected")
        self.btn_activate = QPushButton("Activate Device")

        layout.addWidget(self.status_label)
        layout.addWidget(self.btn_activate)

        self.btn_activate.clicked.connect(self.activate_device)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_device)
        self.timer.start(1000)

    def check_device(self):
        try:
            lockdown = create_using_usbmux()
            product = lockdown.get_value(key='ProductType')
            version = lockdown.get_value(key='ProductVersion')

            if product in SUPPORTED_DEVICES:
                if version in SUPPORTED_VERSIONS:
                    self.status_label.setText(f"Connected: {product} ({version})")
                    self.btn_activate.setEnabled(True)
                else:
                    self.status_label.setText(f"Unsupported iOS: {version}")
                    self.btn_activate.setEnabled(False)
            else:
                self.status_label.setText(f"Unsupported Device: {product}")
                self.btn_activate.setEnabled(False)

        except Exception:
            self.status_label.setText("No device connected")
            self.btn_activate.setEnabled(False)

    def activate_device(self):
        QMessageBox.information(self, "Info", "Your device will now be activated. Please ensure it is connected to Wi-Fi.")
        
        self.timer.stop()
        self.btn_activate.setEnabled(False)

        self.thread = WorkerThread()
        self.thread.status_update.connect(self.update_status)
        self.thread.finished.connect(self.on_success)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_success(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, "Success", message)
        self.btn_activate.setEnabled(True)
        self.timer.start(1000)

    def on_error(self, message):
        QMessageBox.critical(self, "Error", message)
        self.status_label.setText("Error occurred")
        self.btn_activate.setEnabled(True)
        self.timer.start(1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

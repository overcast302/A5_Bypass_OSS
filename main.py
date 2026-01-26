import sys
import os
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

class ActivationThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def wait_for_device(self, timeout=90):
        self.status_update.emit('Waiting for device to return...')
        start = time.monotonic()

        while time.monotonic() - start < timeout:
            try:
                lockdown = create_using_usbmux()
                if lockdown.get_value(key='ProductType'):
                    return lockdown
            except RuntimeError:
                pass
            time.sleep(1)

        raise TimeoutError('Device did not reconnect in time')

    def push_payload(self, lockdown, payload_path, delay=10):
        with AfcService(lockdown=lockdown) as afc:
            afc.set_file_contents(
                'Downloads/downloads.28.sqlitedb',
                open(payload_path, 'rb').read()
            )
        time.sleep(delay)
        DiagnosticsService(lockdown=lockdown).restart()
        time.sleep(10)
        return self.wait_for_device()   

    def get_should_hactivate(self, lockdown):
        diag = DiagnosticsService(lockdown=lockdown)
        return diag.mobilegestalt(keys=['ShouldHactivate']).get('ShouldHactivate')
    
    def run(self):
        try:
            lockdown = create_using_usbmux()

            if lockdown.get_value(key='ActivationState') == 'Activated':
                self.finished.emit('Device is already activated')
                return

            if lockdown.get_value(key='ProductVersion') == '8.4.1' and lockdown.get_value(key='TelephonyCapability'):
                self.finished.emit('Cellular iOS 8.4.1 devices activation is partially broken. Proceed with caution.') # https://github.com/overcast302/A5_Bypass_OSS/issues/7

            self.status_update.emit('Activating device...')
            payload_path = resource_path('payload')

            lockdown = self.push_payload(lockdown, payload_path)

            should_hactivate = self.get_should_hactivate(lockdown)

            if should_hactivate is False:
                for i in range(5):
                    self.status_update.emit(f'Retrying activation\n Attempt {i+1}/5')
                    lockdown = self.push_payload(lockdown, payload_path, 10+i*5)
                    should_hactivate = self.get_should_hactivate(lockdown)
                    if should_hactivate is not False:
                        break

                if should_hactivate is False:
                    self.error.emit('Activation failed after multiple attempts. Make sure the device is connected to the Wi-Fi.')
                    return

            DiagnosticsService(lockdown=lockdown).restart()
            self.finished.emit('Done!')

        except TimeoutError as e:
            self.error.emit('Device did not reconnect in time. Please ensure it is connected and try again.')
        except Exception as e:
            self.error.emit(repr(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('A5 Bypass OSS v1.0.2')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status_label = QLabel('No device connected')
        self.btn_activate = QPushButton('Activate Device')

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
                    self.status_label.setText(f'Connected: {product} ({version})')
                    self.btn_activate.setEnabled(True)
                else:
                    self.status_label.setText(f'Unsupported iOS: {version}')
                    self.btn_activate.setEnabled(False)
            else:
                self.status_label.setText(f'Unsupported Device: {product}')
                self.btn_activate.setEnabled(False)

        except Exception:
            self.status_label.setText('No device connected')
            self.btn_activate.setEnabled(False)

    def activate_device(self):
        QMessageBox.information(
            self,
            'Info',
            'Your device will now be activated. Please ensure it is connected to Wi-Fi.'
        )

        self.timer.stop()
        self.btn_activate.setEnabled(False)

        self.thread = ActivationThread()
        self.thread.status_update.connect(self.update_status)
        self.thread.finished.connect(self.on_success)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_success(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, 'Success', message)
        self.btn_activate.setEnabled(True)
        self.timer.start(1000)

    def on_error(self, message):
        QMessageBox.critical(self, 'Error', message)
        self.status_label.setText('Error occurred')
        self.btn_activate.setEnabled(True)
        self.timer.start(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
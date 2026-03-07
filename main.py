import sys
import os
import time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.afc import AfcService
from pymobiledevice3.services.diagnostics import DiagnosticsService


SUPPORTED = {
    'iPhone4,1': {'9.3.5', '9.3.6'},

    'iPad2,1': {'8.4.1', '9.3.5'},
    'iPad2,2': {'9.3.5', '9.3.6'},
    'iPad2,3': {'9.3.5', '9.3.6'},
    'iPad2,4': {'8.4.1', '9.3.5'},

    'iPad2,5': {'8.4.1', '9.3.5'},
    'iPad2,6': {'9.3.5', '9.3.6'},
    'iPad2,7': {'9.3.5', '9.3.6'},

    'iPad3,1': {'8.4.1', '9.3.5'},
    'iPad3,2': {'9.3.5', '9.3.6'},
    'iPad3,3': {'9.3.5', '9.3.6'},

    'iPod5,1': {'8.4.1', '9.3.5'}
}

# pyinstaller resource path fix
def resource_path(name):
    base = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base, name)


class ActivationThread(QThread):
    status = pyqtSignal(str)
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def wait_for_device(self, timeout=160):
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            try:
                lockdown = create_using_usbmux()
                DiagnosticsService(lockdown=lockdown).mobilegestalt(
                    keys=['ProductType']
                )
                return lockdown
            except Exception:
                time.sleep(2)

        raise TimeoutError()


    def push_payload(self, lockdown, payload):
        with AfcService(lockdown=lockdown) as afc, open(payload, 'rb') as payload_db:
            afc.set_file_contents(
                'Downloads/downloads.28.sqlitedb',
                payload_db.read()
            )

        DiagnosticsService(lockdown=lockdown).restart()
        return self.wait_for_device()

    def should_hactivate(self, lockdown):
        diag = DiagnosticsService(lockdown=lockdown)
        return diag.mobilegestalt(
            keys=['ShouldHactivate']
        ).get('ShouldHactivate')

    def run(self):
        try:
            lockdown = create_using_usbmux()

            if lockdown.get_value(key='ActivationState') == 'Activated':
                self.success.emit('Device is already activated')
                return

            payload = resource_path('payload')
            self.status.emit('Activating device...')

            for attempt in range(5):
                lockdown = self.push_payload(lockdown, payload)

                delay = 10 + attempt * 5
                time.sleep(delay)

                if self.should_hactivate(lockdown):
                    DiagnosticsService(lockdown=lockdown).restart()
                    self.success.emit('Done!')
                    return

                self.status.emit(f'Retrying activation\nAttempt {attempt + 1}/5')
                time.sleep(5)

            self.error.emit(
                'Activation failed after multiple attempts. Make sure the device is connected to the Wi-Fi.'
            )

        except TimeoutError:
            self.error.emit(
                'Device did not reconnect in time. Please ensure it is connected and try again.'
            )
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('A5 Bypass OSS v1.0.6')
        self.setFixedSize(500, 200)

        self.status = QLabel('No device connected')
        self.activate = QPushButton('Activate Device')
        self.activate.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.activate)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.activate.clicked.connect(self.start_activation)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_device)
        self.timer.start(1000)

    def poll_device(self):
        try:
            lockdown = create_using_usbmux()
            info = lockdown.get_value()

            product = info.get('ProductType')
            version = info.get('ProductVersion')

            is_supported = SUPPORTED.get(product)

            if not is_supported:
                self._set_state(f'Unsupported Device: {product}', False)
                return

            if version not in is_supported:
                self._set_state(f'Unsupported {product} iOS version: {version}', False)
                return

            self._set_state(f'Connected: {product} ({version})', True)

        except Exception:
            self._set_state('No device connected', False)

    def _set_state(self, text, enabled):
        self.status.setText(text)
        self.activate.setEnabled(enabled)

    def start_activation(self):
        QMessageBox.information(
            self,
            'Info',
            'Your device will now be activated. Please ensure it is connected to Wi-Fi.'
        )

        self.timer.stop()
        self.activate.setEnabled(False)

        self.worker = ActivationThread()
        self.worker.status.connect(self.status.setText)
        self.worker.success.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, msg):
        self.status.setText(msg)
        QMessageBox.information(self, 'Success', msg)
        self.activate.setEnabled(True)
        self.timer.start(1000)

    def on_error(self, msg):
        QMessageBox.critical(self, 'Error', msg)
        self.status.setText('Error occurred')
        self.timer.start(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
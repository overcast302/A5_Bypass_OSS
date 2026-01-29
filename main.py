import sys
import os
import time

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

from pymobiledevice3.lockdown import create_using_usbmux, NoDeviceConnectedError
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

# pyinstaller resource path fix
def resource_path(name):
    base = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base, name)


class ActivationThread(QThread):
    status = pyqtSignal(str)
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def wait_for_device(self, timeout=120):
        start = time.monotonic()

        while time.monotonic() - start < timeout:
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
        with AfcService(lockdown=lockdown) as afc, open(payload, 'rb') as f:
            afc.set_file_contents(
                'Downloads/downloads.28.sqlitedb',
                f.read()
            )

        DiagnosticsService(lockdown=lockdown).restart()
        time.sleep(10)
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

                if self.should_hactivate(lockdown) is not False:
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

        self.setWindowTitle('A5 Bypass OSS v1.0.2')
        self.setFixedSize(300, 200)

        self.warning_shown = False

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

            if product not in SUPPORTED_DEVICES:
                self._set_state(f'Unsupported Device: {product}', False)
                return

            if version not in SUPPORTED_VERSIONS:
                self._set_state(f'Unsupported iOS: {version}', False)
                return

            # https://github.com/overcast302/A5_Bypass_OSS/issues/7
            if (
                version == '8.4.1'
                and info.get('TelephonyCapability')
                and not self.warning_shown
            ):
                QMessageBox.information(
                    self,
                    'Warning',
                    'Cellular iOS 8.4.1 devices activation is partially broken. Proceed with caution.'
                )
                self.warning_shown = True

            self._set_state(f'Connected: {product} ({version})', True)

        except NoDeviceConnectedError:
            self.warning_shown = False
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
        self.activate.setEnabled(True)
        self.timer.start(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
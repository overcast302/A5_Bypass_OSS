import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from pymobiledevice3.lockdown import create_using_usbmux

from exploits import get_exploit
from exploits.common import parse_version
from exploits.itunesstored.itunesstored import ItunesstoredExploit


class ActivationThread(QThread):
    status = pyqtSignal(str)
    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            lockdown = create_using_usbmux()
            values = lockdown.get_value()

            if values.get('ActivationState') == 'Activated':
                self.success.emit('Device is already activated')
                return

            exploit_cls = get_exploit(parse_version(values.get('ProductVersion')), lockdown.udid)
            if exploit_cls is None:
                self.error.emit('Unsupported iOS version')
                return

            self.status.emit('Activating device...')
            exploit_cls(log=self.status.emit).run(lockdown)
            self.success.emit('Done!')

        except TimeoutError:
            self.error.emit(
                'Device did not reconnect in time. Please ensure it is connected and try again.'
            )
        except Exception as e:
            self.error.emit(repr(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('hacktiv8 v1.2.0')
        self.setFixedSize(500, 200)

        self.version = (0,)

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
            values = lockdown.get_value()

            product = values.get('ProductType')
            version = values.get('ProductVersion')
            build = values.get('BuildVersion')
            version_tuple = parse_version(version)
            exploit_cls = get_exploit(version_tuple, lockdown.udid)
        except Exception:
            self._set_state('No device connected', False)
            return

        if exploit_cls is None:
            self._set_state(f'Unsupported {product} iOS version: {version}', False)
            return

        try:
            supported = exploit_cls.available(product, build, lockdown.udid)
        except Exception:
            self._set_state('Could not reach backend. Please check your internet connection!', False)
            return

        if not supported:
            self._set_state(exploit_cls.unavailable.format(product=product, version=version), False)
            return

        self.version = version_tuple
        self._set_state(f'Connected: {product} ({version})', True)

    def _set_state(self, text, enabled):
        self.status.setText(text)
        self.activate.setEnabled(enabled)

    def start_activation(self):
        if ItunesstoredExploit.supports(self.version):
            note = 'Please ensure it is connected to Wi-Fi.'
        else:
            note = 'Your device will reboot during the process.'
        QMessageBox.information(
            self,
            'Info',
            'Your device will now be activated. ' + note
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
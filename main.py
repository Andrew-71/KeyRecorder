import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QMessageBox

import keyboard
import mouse


# Check that a filename is valid
# True codes:
# 1 == no extension
# 2 == .krf extension
# 3 == .custom extension, show warning
# TODO: Bad verification, likely redundant checks or edge cases not accounted for
def verify_filename(filename):
    if len(filename) == 0:
        return False, 'Empty filename'

    if True in [x in '<>:;"/\\|?*\'' for x in filename]:
        return False, 'Forbidden character, preferably only use Latin, Digits and Cyrillic'

    with_extension = filename.split('.')

    if len(with_extension) == 2:
        if with_extension[0] == '' or with_extension[1] == '':
            return False, 'Empty filename or extension'

        if with_extension[1] != 'krf':
            return True, 3
        else:
            return True, 2
    elif len(with_extension) > 2:
        return False, 'More than 1 extension'
    elif len(with_extension) == 1 and '.' in filename:
        return False, 'Empty extension'
    return True, 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('app_ui.ui', self)  # Load in UI  TODO: Replace with a class

        self.events = []

        self.configure_buttons()

    def configure_buttons(self):
        self.open_from_file_btn.clicked.connect(self.open_file)
        self.save_to_file_btn.clicked.connect(self.save_file)

        self.start_recording_btn.clicked.connect(self.start_recording)
        self.stop_recording_btn.clicked.connect(self.stop_recording)
        self.stop_recording_btn.setEnabled(False)
        self.clear_recording_btn.clicked.connect(self.clear_recording)

        self.play_btn.clicked.connect(self.play_recording)

    # Everything related to recording ===============================

    def start_recording(self):
        mouse.hook(self.events.append)  # starting the mouse recording
        keyboard.hook(self.events.append)
        self.stop_recording_btn.setEnabled(True)
        self.start_recording_btn.setEnabled(False)

    def stop_recording(self):
        mouse.unhook_all()
        keyboard.unhook_all()
        self.refresh_list()
        self.stop_recording_btn.setEnabled(False)
        self.start_recording_btn.setEnabled(True)

    def clear_recording(self):
        confirm_window = QMessageBox
        ret = confirm_window.question(self, 'Question', "Are you sure you want to clear recording?",
                                      confirm_window.Yes | confirm_window.No)
        if ret == confirm_window.Yes:
            self.events = []
            self.refresh_list()

    def play_recording(self):
        mouse_events = []
        for i in self.events:
            if i.__class__ != keyboard.KeyboardEvent:
                mouse_events.append(i)
            else:
                mouse.play(mouse_events)
                mouse_events = []
                keyboard.play([i])
        mouse.play(mouse_events)

    # File management ===============================================

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'Select file', '',
                                                   'Key Recorder File (*.krf);;All files (*) ')  # Key Recorder File
        if not ok or len(filename.split('.')) != 2:
            return 0

    def save_file(self):
        try:
            filename = self.save_filename.text()
            check = verify_filename(filename)
            if not check[0]:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Saving Error")
                msg.setInformativeText(check[1])
                msg.setWindowTitle("Error")
                msg.exec_()
            else:
                if check[1] == 1:
                    filename += '.krf'
                elif check[1] == 3:
                    confirm_window = QMessageBox
                    ret = confirm_window.question(self, 'Question', "You entered a custom filename. Use '.krf' instead?",
                                                  confirm_window.Yes | confirm_window.No)
                    if ret == confirm_window.Yes:
                        filename = filename.split('.')[0] + '.krf'
                open(filename, 'w').write('test')
        except Exception as e:
            print(e)

    # ===============================================================

    def refresh_list(self):
        self.list.clear()
        self.list.addItems(list(map(lambda x: x.__class__.__name__, self.events)))




if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Open login window

    KeyRecorder = MainWindow()
    KeyRecorder.show()

    sys.exit(app.exec_())

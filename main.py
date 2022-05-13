import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QMessageBox

import keyboard
import mouse

import pickle


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
        self.is_recording = False

        self.configure_buttons()

    def configure_buttons(self):
        self.open_from_file_btn.clicked.connect(self.open_file)
        self.save_to_file_btn.clicked.connect(self.save_file)

        self.clear_recording_btn.clicked.connect(self.clear_recording)
        self.toggle_recording_btn.clicked.connect(self.toggle_recording)

        self.play_btn.clicked.connect(self.play_recording)

        self.setWindowTitle('KeyRecorder')

    # Everything related to recording ===============================

    def toggle_recording(self):
        if not self.is_recording:
            mouse.hook(self.events.append)  # starting the mouse recording
            keyboard.hook(self.events.append)
            self.is_recording = True
            self.toggle_recording_btn.setText('Stop recording')
        else:
            mouse.unhook_all()
            keyboard.unhook_all()
            self.is_recording = False
            self.toggle_recording_btn.setText('Start recording')

            # TODO: DO WE NEED THIS?
            self.events = self.events[:-2]

            self.refresh_list()

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
                time.sleep(self.typing_delay_spinbox.value())
        mouse.play(mouse_events)

    # File management ===============================================

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, 'Select file', '',
                                                   'Key Recorder File (*.krf);;All files (*) ')  # Key Recorder File
        if not ok or len(filename.split('.')) != 2:
            return 0
        with open(filename, 'rb') as f:
            self.events = pickle.load(f)
        self.refresh_list()

    def save_file(self):
        filename, ok = QFileDialog.getSaveFileName(self, 'Select file', '',
                                                   'Key Recorder File (*.krf);;All files (*) ')  # Key Recorder File
        if not ok or len(filename.split('.')) != 2:
            return 0
        with open(filename, 'wb') as f:
            pickle.dump(self.events, f)

    # ===============================================================

    def refresh_list(self):
        self.list.clear()
        self.list_advanced.clear()

        short_view = []
        long_view = []
        current = []
        for i in self.events:
            long_view.append(str(i))
            if i.__class__ != keyboard.KeyboardEvent and \
                    (len(current) == 0 or (len(current) > 0 and i.__class__.__name__ == current[0])):
                current.append(i.__class__.__name__)
            else:
                if len(current) > 0:
                    short_view.append(f'{current[0]} ({len(current)})')
                    current = []
                short_view.append(i.__class__.__name__)
        if len(current) > 0:
            short_view.append(f'{current[0]} ({len(current)})')

        self.list.addItems(short_view)
        self.list_advanced.addItems(long_view)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    KeyRecorder = MainWindow()
    KeyRecorder.show()

    sys.exit(app.exec_())

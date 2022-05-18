import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QMessageBox

import keyboard
import mouse

import pickle


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
            mouse.hook(self.add_item)
            keyboard.hook(self.add_item)
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
        self.toggle_buttons()

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

    # List management ===============================================

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

    def add_item(self, item):
        self.events.append(item)
        self.list_advanced.addItem(str(item))

    # ===============================================================

    def toggle_buttons(self):
        enabled = (not self.is_recording)
        elements = [self.save_to_file_btn, self.open_from_file_btn,
                    self.play_btn, self.clear_recording_btn, self.typing_delay_spinbox]
        for i in elements:
            i.setEnabled(enabled)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    KeyRecorder = MainWindow()
    KeyRecorder.show()

    sys.exit(app.exec_())

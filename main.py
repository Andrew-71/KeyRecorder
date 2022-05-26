import json
import sys
import time

from PyQt5 import uic
from PyQt5.QtCore import QThread, QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QMessageBox

import keyboard
import mouse

import pickle

from settings_window import SettingsWindow
from playback_thread import PlaybackThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('app_ui.ui', self)  # Load in UI  TODO: Replace with a class

        # Load in user settings
        self.config = json.load(open('config.json', encoding="utf8"))
        self.language_pack = json.load(open('languages.json', encoding="utf8"))
        self.settings = SettingsWindow(self)

        self.events = []
        self.is_recording = False

        self.configure_buttons()
        self.retranslate_ui()

    def configure_buttons(self):
        self.open_from_file_btn.clicked.connect(self.open_file)
        self.save_to_file_btn.clicked.connect(self.save_file)

        self.clear_recording_btn.clicked.connect(self.clear_recording)
        self.toggle_recording_btn.clicked.connect(self.toggle_recording)

        self.play_btn.clicked.connect(self.play_recording)

        self.typing_delay_spinbox.setValue(self.config['default_delay'])

        self.setWindowTitle('KeyRecorder')

        self.settings_btn.clicked.connect(self.show_settings)

    # Recording management ==========================================

    def toggle_recording(self):
        self.is_recording = (not self.is_recording)
        self.toggle_recording_btn.setText(self.language_pack['toggle_recording_btn'][self.config['lang']][('start' if not self.is_recording else 'stop')])
        self.toggle_buttons()

        if self.is_recording:
            if self.config['dynamic_refresh']:
                mouse.hook(self.add_item)
                keyboard.hook(self.add_item)
            else:
                mouse.hook(self.events.append)
                keyboard.hook(self.events.append)
        else:
            mouse.unhook_all()
            keyboard.unhook_all()
            del self.events[-3:]  # Prevent program from restarting recording at the end of playback
            self.refresh_list()

    def clear_recording(self):
        confirm_window = QMessageBox
        ret = confirm_window.question(self, 'Question', "Are you sure you want to clear recording?",
                                      confirm_window.Yes | confirm_window.No)
        if ret == confirm_window.Yes:
            self.events.clear()
            self.refresh_list()

    def play_recording(self):
        pool = QThreadPool.globalInstance()
        runnable = PlaybackThread(self.events, self.typing_delay_spinbox.value())
        pool.start(runnable)

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
        if self.config['dynamic_refresh']:
            self.list_advanced.addItem(str(item))

    # UI management =================================================

    def toggle_buttons(self):
        elements = [self.save_to_file_btn, self.open_from_file_btn,
                    self.play_btn, self.clear_recording_btn, self.typing_delay_spinbox]
        for i in elements:
            i.setEnabled(not self.is_recording)
    
    # This function has not been tested and may contain errors
    def retranslate_ui(self):
        elements = [self.save_to_file_btn, self.open_from_file_btn,
                    self.play_btn, self.clear_recording_btn, self.typing_delay_label, self.settings_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.config['lang']])

        self.tabWidget.setTabText(0, self.language_pack['tab'][self.config['lang']])
        self.tabWidget.setTabText(1, self.language_pack['tab_2'][self.config['lang']])

        self.toggle_recording_btn.setText(self.language_pack['toggle_recording_btn'][self.config['lang']][('start' if not self.is_recording else 'stop')])

    def show_settings(self):
        self.settings.load_settings()
        self.settings.show()

    def reload_config(self):
        self.config = json.load(open('config.json', encoding="utf8"))
        self.retranslate_ui()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    KeyRecorder = MainWindow()
    KeyRecorder.show()

    sys.exit(app.exec_())

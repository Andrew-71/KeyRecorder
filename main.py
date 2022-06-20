import json
import sys
import time

import win32gui
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QThread, QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QMessageBox

import keyboard
import mouse

import pickle

from win32gui import GetWindowText, GetForegroundWindow, EnumWindows
from win32api import GetSystemMetrics

from settings_window import SettingsWindow
from playback_thread import PlaybackThread
from resolution_change_window import ResolutionWindow
from delete_events_window import SelectDeleteWindowWindow
from advanced_save_window import AdvancedSaveWindow
from event_states_window import EventStatesWindow

from resolution_management_utils import resize, check_compatibility


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('app_ui.ui', self)  # Load in UI  TODO: Replace with a class
        self.setFixedSize(700, 1000)

        # Load in user settings
        self.config = json.load(open('config.json', encoding="utf8"))
        self.language_pack = json.load(open('languages.json', encoding="utf8"))['main']

        # Windows
        self.settings = SettingsWindow(self)
        self.res_window = ResolutionWindow(self)
        self.delete_manager = SelectDeleteWindowWindow(self)
        self.advanced_save = AdvancedSaveWindow(self)
        self.enable_window = EventStatesWindow(self)

        self.events = []
        self.is_recording = False

        self.configure_buttons()
        self.retranslate_ui()
        self.refresh_list()

    def configure_buttons(self):
        self.open_from_file_btn.clicked.connect(self.open_file)
        self.save_to_file_btn.clicked.connect(self.save_file)

        self.clear_recording_btn.clicked.connect(self.clear_recording)
        self.toggle_recording_btn.clicked.connect(self.toggle_recording)

        self.play_btn.clicked.connect(self.play_recording)

        self.typing_delay_spinbox.setValue(self.config['default_delay'])

        self.setWindowTitle('KeyRecorder')

        self.change_res_btn.clicked.connect(self.show_resolution)
        self.settings_btn.clicked.connect(self.show_settings)
        self.clear_specific_recording_btn.clicked.connect(self.show_delete)

        self.custom_checkbox.stateChanged.connect(self.custom_pick)
        self.change_enabled_btn.clicked.connect(self.change_events_states)

    # Recording management ==========================================

    def toggle_recording(self):
        self.is_recording = (not self.is_recording)
        self.toggle_recording_btn.setText(self.language_pack['toggle_recording_btn'][self.config['lang']][
                                              ('start' if not self.is_recording else 'stop')])
        self.toggle_buttons()

        if self.is_recording:
            mouse.hook(self.add_item)
            keyboard.hook(self.add_item)
        else:
            mouse.unhook_all()
            keyboard.unhook_all()
            self.refresh_list()

    def clear_recording(self):
        confirm_window = QMessageBox
        ret = confirm_window.question(self, 'Question', "Are you sure you want to clear recording?",
                                      confirm_window.Yes | confirm_window.No)
        if ret == confirm_window.Yes:
            self.events.clear()
            self.refresh_list()

    def play_recording(self):
        check = check_compatibility(self.events)
        if check in ('full', 'partial'):

            confirm = False
            if not self.config['auto_compatibility'] and check == 'partial':
                confirm_window = QMessageBox
                if self.config['lang'] == 'en':
                    ret = confirm_window.question(self, 'Can\'t run',
                                                  "Not all events are same resolution as your monitor's\n"
                                                  "However we could run it in compatibility mode instead.\nDo that?",
                                                  confirm_window.Yes | confirm_window.No)
                else:
                    ret = confirm_window.question(self, 'Невозможно запустить',
                                                  "Не все события в Вашей записи одного разрешения с Вашим монитором\n"
                                                  "Однако программу можно запустить в режиме совместимости.\n"
                                                  "Сделать так?",
                                                  confirm_window.Yes | confirm_window.No)
                if ret == confirm_window.Yes:
                    confirm = True
                else:
                    return
            if confirm or self.config['auto_compatibility']:
                self.events = resize(self.events)
                self.refresh_list()

            pool = QThreadPool.globalInstance()
            runnable = PlaybackThread(self, self.events, self.typing_delay_spinbox.value())
            pool.start(runnable)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            if self.config['lang'] == 'en':
                msg.setText("Can't run")
                msg.setInformativeText('You need to convert all events to match your monitor\'s resolution first')
            else:
                msg.setText("Не удалось запустить")
                msg.setInformativeText('Требуется, чтобы все события записи были одного разрешение с Вашим монитором')

            msg.setWindowTitle("Error")
            msg.exec_()

    def custom_pick(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                choices.append(win32gui.GetWindowText(hwnd))

        self.custom_choice.setEnabled(not self.custom_choice.isEnabled())

        self.custom_choice.clear()

        if self.custom_choice.isEnabled():
            choices = []
            win32gui.EnumWindows(winEnumHandler, None)
            self.custom_choice.addItems(list(set(choices)))

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

        if self.config['advanced_save']:
            self.advanced_save.render_options(filename)
            return
        with open(filename, 'wb') as f:
            pickle.dump(self.events, f)

    # List management ===============================================

    def refresh_list(self):
        enable_buttons = len(list(filter(lambda x: x["enabled"], self.events))) > 1
        buttons = [self.clear_recording_btn, self.save_to_file_btn, self.play_btn, self.clear_specific_recording_btn,
                   self.change_res_btn]
        for i in buttons:
            i.setEnabled(enable_buttons)
        self.change_enabled_btn.setEnabled(len(self.events) > 1)

        self.list.clear()
        self.list_advanced.clear()

        short_view = [f'Enabled: {len(list(filter(lambda x: x["enabled"], self.events)))} events\n'
                      f'Total: {len(self.events)} events\n']
        long_view = []
        current = []
        for i in self.events:
            long_view.append(str(i))

            # Short view only displays enabled events
            if not i['enabled']:
                continue

            if i['event'].__class__ != keyboard.KeyboardEvent and \
                    (len(current) == 0 or (len(current) > 0 and i['event'].__class__.__name__ == current[0])):
                current.append(i['event'].__class__.__name__)
            else:
                if len(current) > 0:
                    short_view.append(f'{current[0]} ({len(current)})')
                    current = []
                short_view.append(i['event'].__class__.__name__)
        if len(current) > 0:
            short_view.append(f'{current[0]} ({len(current)})')

        self.list.addItems(short_view)
        self.list_advanced.addItems(long_view)

    def add_item(self, item):
        new_event = {'event': item,
                     'window': GetWindowText(GetForegroundWindow()),
                     'resolution': {'w': GetSystemMetrics(0), 'h': GetSystemMetrics(1)},
                     'enabled': True}

        # If we don't need to record the event disable it
        if self.custom_choice.isEnabled() and GetWindowText(GetForegroundWindow()) not in ('KeyRecorder', '', self.custom_choice.currentText()) and not \
                (self.custom_choice.currentText() == 'Архитектор' and GetWindowText(GetForegroundWindow()) in ('BimCad', 'Сохранение изменений')):
            new_event['enabled'] = False

        self.events.append(new_event)

        # Dynamically refresh if needed
        if self.config['dynamic_refresh']:
            self.list_advanced.addItem(str(new_event))

    # UI management =================================================

    def toggle_buttons(self, enabled=None, include_stop=False):
        if enabled is None:
            enabled = not self.is_recording
        elements = [self.save_to_file_btn, self.open_from_file_btn,
                    self.play_btn, self.clear_recording_btn, self.typing_delay_spinbox,
                    self.change_res_btn, self.settings_btn, self.clear_specific_recording_btn]
        if include_stop:
            elements.append(self.toggle_recording_btn)
        for i in elements:
            i.setEnabled(enabled)

    def retranslate_ui(self):
        elements = [self.save_to_file_btn, self.open_from_file_btn,
                    self.play_btn, self.clear_recording_btn, self.typing_delay_label, self.settings_btn,
                    self.change_res_btn, self.clear_specific_recording_btn, self.custom_checkbox,
                    self.change_enabled_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.config['lang']])

        self.tabWidget.setTabText(0, self.language_pack['tab'][self.config['lang']])
        self.tabWidget.setTabText(1, self.language_pack['tab_2'][self.config['lang']])

        self.toggle_recording_btn.setText(self.language_pack['toggle_recording_btn'][self.config['lang']][
                                              ('start' if not self.is_recording else 'stop')])

        for i in [self.settings, self.delete_manager, self.res_window, self.enable_window, self.advanced_save]:
            i.retranslate_ui()

    def show_settings(self):
        self.settings.load_settings()
        self.settings.show()

    def reload_config(self):
        self.config = json.load(open('config.json', encoding="utf8"))
        self.retranslate_ui()

    def show_resolution(self):
        self.res_window.show()

    def show_delete(self):
        self.delete_manager.show_options()
        self.delete_manager.show()

    def change_events_states(self):
        self.enable_window.render_options()
        self.enable_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    KeyRecorder = MainWindow()
    KeyRecorder.show()

    sys.exit(app.exec_())

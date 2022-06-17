import json

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        uic.loadUi('settings_ui.ui', self)  # Load in UI  TODO: Replace with a class
        self.setWindowTitle('Settings')

        self.parent = parent
        self.save_btn.clicked.connect(self.save_settings)

        self.language_pack = json.load(open('languages.json', encoding="utf8"))['settings']

    def load_settings(self):
        if self.parent.config['lang'] == 'ru':
            self.russian_radio.setChecked(True)
        else:
            self.english_radio.setChecked(True)

        self.dynamic_refresh_checkbox.setChecked(self.parent.config['dynamic_refresh'])

        self.auto_compatibility_checkbox.setChecked(self.parent.config['auto_compatibility'])

        self.stop_unexpected_playback_checkbox.setChecked(self.parent.config['stop_unexpected_playback'])

        self.default_delay_spinbox.setValue(self.parent.config['default_delay'])

        self.advanced_save_check.setChecked(self.parent.config['advanced_save'])

    def save_settings(self):
        if self.russian_radio.isChecked():
            lang = 'ru'
        else:
            lang = 'en'

        new_cfg = {"lang": lang,
                   "default_delay": self.default_delay_spinbox.value(),
                   "dynamic_refresh": self.dynamic_refresh_checkbox.isChecked(),
                   "stop_unexpected_playback": self.stop_unexpected_playback_checkbox.isChecked(),
                   "auto_compatibility": self.auto_compatibility_checkbox.isChecked(),
                   "advanced_save": self.advanced_save_check.isChecked()}

        with open("config.json", "w") as write_file:
            json.dump(new_cfg, write_file)

        self.parent.reload_config()

    def retranslate_ui(self):
        elements = [self.save_btn, self.settings_label,
                    self.language_label, self.default_delay_label, self.dynamic_refresh_checkbox,
                    self.stop_unexpected_playback_checkbox, self.auto_compatibility_checkbox]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])

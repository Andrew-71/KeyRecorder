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

        if self.parent.config['dynamic_refresh']:
            self.dynamic_refresh_checkbox.setChecked(True)
        else:
            self.dynamic_refresh_checkbox.setChecked(False)

        self.default_delay_spinbox.setValue(self.parent.config['default_delay'])

    def save_settings(self):
        if self.russian_radio.isChecked():
            lang = 'ru'
        else:
            lang = 'en'

        new_cfg = {"lang": lang,
                   "default_delay": self.default_delay_spinbox.value(),
                   "dynamic_refresh": self.dynamic_refresh_checkbox.isChecked()}

        with open("config.json", "w") as write_file:
            json.dump(new_cfg, write_file)

        self.parent.reload_config()

    def retranslate_ui(self):
        elements = [self.save_btn, self.settings_label,
                    self.language_label, self.default_delay_label, self.dynamic_refresh_checkbox]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])

import json

import keyboard
import mouse
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class SelectDeleteWindowWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        uic.loadUi('select_for_deletion.ui', self)  # Load in UI  TODO: Replace with a class
        self.setWindowTitle('Select what window\'s actions to delete')

        self.parent = parent
        self.cancel_btn.clicked.connect(self.hide)
        self.confirm_btn.clicked.connect(self.delete_selected)
        self.language_pack = json.load(open('languages.json', encoding="utf8"))['delete_app_events']

    def show_options(self):
        self.select_box.clear()
        try:
            options = set()
            for i in self.parent.events:

                if i['window'] == '':
                    options.add('"" (Windows desktop)')
                else:
                    options.add(i['window'])
            self.select_box.addItems(list(options))
        except Exception as e:
            print(e)

    def delete_selected(self):
        for_deletion = self.select_box.currentText()
        if for_deletion == '"" (Windows desktop)':
            for_deletion = ''

        self.parent.events = list(filter(lambda x: x['window'] != for_deletion, self.parent.events))
        self.parent.refresh_list()

        self.hide()

    def retranslate_ui(self):
        elements = [self.confirm_btn, self.cancel_btn, self.label]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])
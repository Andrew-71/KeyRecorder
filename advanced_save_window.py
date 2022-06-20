import json
import pickle

import keyboard
import mouse
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from win32api import GetSystemMetrics

from resolution_management_utils import resize


class AdvancedSaveWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        uic.loadUi('app_selection.ui', self)  # Load in UI  TODO: Replace with a class
        self.setFixedSize(400, 530)
        self.setWindowTitle('Advanced Check')

        self.parent = parent

        self.language_pack = json.load(open('languages.json', encoding="utf8"))['advanced_save_window']

        self.filename = 'placeholder'
        self.save_btn.clicked.connect(self.save_file)

    def render_options(self, filename):
        self.list_view.clear()

        names = set()
        for i in self.parent.events:
            names.add((i['window'], i['enabled']))
        names = list(names)

        for i in names:
            item = QtWidgets.QListWidgetItem(i[0])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState((QtCore.Qt.Checked if i[1] else QtCore.Qt.Unchecked))
            self.list_view.addItem(item)

        self.filename = filename
        self.show()

    def save_file(self):
        valid = []
        for i in [self.list_view.item(i) for i in range(self.list_view.count())]:
            if i.checkState() != 0:
                valid.append(i.text())

        new_events = list(filter(lambda x: x['window'] in valid, list(self.parent.events)))
        for i in new_events:
            i['enabled'] = True

        with open(self.filename, 'wb') as f:
            pickle.dump(new_events, f)
        self.hide()

    def retranslate_ui(self):
        elements = [self.label, self.save_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])


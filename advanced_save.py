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

        uic.loadUi('save_check.ui', self)  # Load in UI  TODO: Replace with a class
        self.setWindowTitle('Advanced Check')

        self.parent = parent

        self.language_pack = json.load(open('languages.json', encoding="utf8"))['resolution_window']

        self.filename = 'placeholder'
        self.save_btn.clicked.connect(self.save_file)

    def render_options(self, filename):
        names = set()
        for i in self.parent.events:
            names.add(i['window'])
        names = list(names)

        for i in names:
            testcase_name = i

            item = QtWidgets.QListWidgetItem(testcase_name)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.list_view.addItem(item)

        self.filename = filename
        self.show()

    def save_file(self):
        valid = []
        for i in [self.list_view.item(i) for i in range(self.list_view.count())]:
            if i.checkState() != 0:
                valid.append(i.text())

        new_events = list(filter(lambda x: x['window'] in valid, list(self.parent.events)))

        with open(self.filename, 'wb') as f:
            pickle.dump(new_events, f)
        self.hide()

    def retranslate_ui(self):
        return
        elements = [self.label, self.save_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])


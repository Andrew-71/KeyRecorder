import json
import pickle

import keyboard
import mouse
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from win32api import GetSystemMetrics


class EventStatesWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        uic.loadUi('app_selection.ui', self)  # Load in UI  TODO: Replace with a class
        self.setFixedSize(400, 530)
        self.setWindowTitle('Set events status')

        self.parent = parent

        self.language_pack = json.load(open('languages.json', encoding="utf8"))['event_states_window']

        self.save_btn.clicked.connect(self.save_status)

    def render_options(self):
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

        self.show()

    def save_status(self):
        enabled = []
        for i in [self.list_view.item(i) for i in range(self.list_view.count())]:
            if i.checkState() != 0:
                enabled.append(i.text())

        for i in self.parent.events:
            i['enabled'] = i['window'] in enabled

        self.parent.refresh_list()
        self.hide()

    def retranslate_ui(self):
        elements = [self.label, self.save_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])

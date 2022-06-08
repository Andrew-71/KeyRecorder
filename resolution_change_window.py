import json

import keyboard
import mouse
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from win32api import GetSystemMetrics

from resolution_management_utils import resize


class ResolutionWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        uic.loadUi('resolution_change.ui', self)  # Load in UI  TODO: Replace with a class
        self.setWindowTitle('Change resolution')

        self.parent = parent
        self.change_res_btn.clicked.connect(self.change_res)

        self.custom_output_check.stateChanged.connect(self.custom_out_switch)
        self.monitor_res_btn.clicked.connect(self.set_monitor_res)

        self.language_pack = json.load(open('languages.json', encoding="utf8"))['resolution_window']

    def set_monitor_res(self):
        self.custom_output_width.setValue(GetSystemMetrics(0))
        self.custom_output_height.setValue(GetSystemMetrics(1))

    def custom_out_switch(self):
        self.output_select.setEnabled(not self.output_select.isEnabled())
        self.custom_output_width.setEnabled((not self.custom_output_width.isEnabled()))
        self.custom_output_height.setEnabled((not self.custom_output_height.isEnabled()))
        self.monitor_res_btn.setEnabled((not self.monitor_res_btn.isEnabled()))

    def change_res(self):
        if not self.output_select.isEnabled():
            x_out, y_out = int(self.custom_output_width.value()), int(self.custom_output_height.value())
        else:
            x_out, y_out = map(int, self.output_select.currentText().split('x'))

        try:
            self.parent.events = resize(self.parent.events, target_res=(x_out, y_out))
        except Exception as e:
            print(e)
        self.parent.refresh_list()

    def retranslate_ui(self):
        elements = [self.label, self.new_res_label, self.custom_output_check, self.change_res_btn,  self.monitor_res_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])
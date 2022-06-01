import json

import keyboard
import mouse
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class ResolutionWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        uic.loadUi('resolution_change.ui', self)  # Load in UI  TODO: Replace with a class
        self.setWindowTitle('Change resolution')

        self.parent = parent
        self.change_res_btn.clicked.connect(self.change_res)

        self.custom_input_check.stateChanged.connect(self.custom_in_switch)
        self.custom_output_check.stateChanged.connect(self.custom_out_switch)

        self.language_pack = json.load(open('languages.json', encoding="utf8"))['resolution_window']

    def custom_out_switch(self):
        self.output_select.setEnabled(not self.output_select.isEnabled())
        self.custom_output_width.setEnabled((not self.custom_output_width.isEnabled()))
        self.custom_output_height.setEnabled((not self.custom_output_height.isEnabled()))

    def custom_in_switch(self):
        self.input_select.setEnabled(not self.input_select.isEnabled())
        self.custom_input_width.setEnabled((not self.custom_input_width.isEnabled()))
        self.custom_input_height.setEnabled((not self.custom_input_height.isEnabled()))

    def change_res(self):
        if not self.input_select.isEnabled():
            x_in, y_in = int(self.custom_input_width.value()), int(self.custom_input_height.value())
        else:
            x_in, y_in = map(int, self.input_select.currentText().split('x'))

        if not self.output_select.isEnabled():
            x_out, y_out = int(self.custom_output_width.value()), int(self.custom_output_height.value())
        else:
            x_out, y_out = map(int, self.output_select.currentText().split('x'))

        ratio_w = x_in / x_out
        ratio_h = y_in / y_out
        new_events = [mouse.MoveEvent(x=int(i.x * ratio_w), y=int(i.y * ratio_h), time=i.time) if i.__class__ != keyboard.KeyboardEvent else i for i in self.parent.events]
        self.parent.events = new_events
        self.parent.refresh_list()

    def retranslate_ui(self):
        elements = [self.label, self.original_res_label, self.new_res_label,
                    self.custom_input_check, self.custom_output_check, self.change_res_btn]
        for i in elements:
            i.setText(self.language_pack[i.objectName()][self.parent.config['lang']])
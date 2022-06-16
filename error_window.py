from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class ErrorWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('error_window.ui', self)  # Load in UI  TODO: Replace with a class
        self.setWindowTitle('Error')

        self.ok_btn.clicked.connect(self.hide)

    def show_msg(self, msg, desc):
        self.msg.setText(msg)
        self.desc.setText(desc)
        self.show()

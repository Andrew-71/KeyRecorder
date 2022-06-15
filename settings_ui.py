# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 421)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(750, 370))
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 8, 731, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.settings_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(32)
        self.settings_label.setFont(font)
        self.settings_label.setObjectName("settings_label")
        self.verticalLayout.addWidget(self.settings_label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.language_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.language_label.setObjectName("language_label")
        self.verticalLayout.addWidget(self.language_label)
        self.russian_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.russian_radio.setObjectName("russian_radio")
        self.verticalLayout.addWidget(self.russian_radio)
        self.english_radio = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.english_radio.setObjectName("english_radio")
        self.verticalLayout.addWidget(self.english_radio)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.default_delay_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.default_delay_label.setObjectName("default_delay_label")
        self.horizontalLayout.addWidget(self.default_delay_label)
        self.default_delay_spinbox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.default_delay_spinbox.setObjectName("default_delay_spinbox")
        self.horizontalLayout.addWidget(self.default_delay_spinbox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.dynamic_refresh_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.dynamic_refresh_checkbox.setObjectName("dynamic_refresh_checkbox")
        self.verticalLayout.addWidget(self.dynamic_refresh_checkbox)
        self.auto_compatibility_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.auto_compatibility_checkbox.setObjectName("auto_compatibility_checkbox")
        self.verticalLayout.addWidget(self.auto_compatibility_checkbox)
        self.stop_unexpected_playback_checkbox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.stop_unexpected_playback_checkbox.setObjectName("stop_unexpected_playback_checkbox")
        self.verticalLayout.addWidget(self.stop_unexpected_playback_checkbox)
        self.save_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.save_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.save_btn.setObjectName("save_btn")
        self.verticalLayout.addWidget(self.save_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.settings_label.setText(_translate("Form", "Settings"))
        self.language_label.setText(_translate("Form", "Language"))
        self.russian_radio.setText(_translate("Form", "Russian (Русский)"))
        self.english_radio.setText(_translate("Form", "English"))
        self.default_delay_label.setText(_translate("Form", "Default typing delay"))
        self.dynamic_refresh_checkbox.setText(_translate("Form", "Dynamic Refresh (May hurt perfomance)"))
        self.auto_compatibility_checkbox.setText(_translate("Form", "Auto launch playback in compatibility mode when possible"))
        self.stop_unexpected_playback_checkbox.setText(_translate("Form", "Stop playback in unexpected situation"))
        self.save_btn.setText(_translate("Form", "SAVE"))

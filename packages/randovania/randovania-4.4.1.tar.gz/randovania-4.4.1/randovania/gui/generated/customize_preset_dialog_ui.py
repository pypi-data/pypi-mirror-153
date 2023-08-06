# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'customize_preset_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_CustomizePresetDialog(object):
    def setupUi(self, CustomizePresetDialog):
        if not CustomizePresetDialog.objectName():
            CustomizePresetDialog.setObjectName(u"CustomizePresetDialog")
        CustomizePresetDialog.resize(700, 768)
        self.root_layout = QVBoxLayout(CustomizePresetDialog)
        self.root_layout.setSpacing(6)
        self.root_layout.setContentsMargins(11, 11, 11, 11)
        self.root_layout.setObjectName(u"root_layout")
        self.name_layout = QHBoxLayout()
        self.name_layout.setSpacing(6)
        self.name_layout.setObjectName(u"name_layout")
        self.name_label = QLabel(CustomizePresetDialog)
        self.name_label.setObjectName(u"name_label")

        self.name_layout.addWidget(self.name_label)

        self.name_edit = QLineEdit(CustomizePresetDialog)
        self.name_edit.setObjectName(u"name_edit")

        self.name_layout.addWidget(self.name_edit)


        self.root_layout.addLayout(self.name_layout)

        self.main_tab_widget = QTabWidget(CustomizePresetDialog)
        self.main_tab_widget.setObjectName(u"main_tab_widget")
        self.main_tab_widget.setTabPosition(QTabWidget.North)
        self.main_tab_widget.setTabShape(QTabWidget.Rounded)
        self.main_tab_widget.setTabBarAutoHide(False)
        self.logic_tab_widget = QTabWidget()
        self.logic_tab_widget.setObjectName(u"logic_tab_widget")
        self.main_tab_widget.addTab(self.logic_tab_widget, "")
        self.patches_tab_widget = QTabWidget()
        self.patches_tab_widget.setObjectName(u"patches_tab_widget")
        self.main_tab_widget.addTab(self.patches_tab_widget, "")

        self.root_layout.addWidget(self.main_tab_widget)

        self.button_box = QDialogButtonBox(CustomizePresetDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.root_layout.addWidget(self.button_box)


        self.retranslateUi(CustomizePresetDialog)

        self.main_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CustomizePresetDialog)
    # setupUi

    def retranslateUi(self, CustomizePresetDialog):
        CustomizePresetDialog.setWindowTitle(QCoreApplication.translate("CustomizePresetDialog", u"Customize Preset", None))
        self.name_label.setText(QCoreApplication.translate("CustomizePresetDialog", u"Name:", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.logic_tab_widget), QCoreApplication.translate("CustomizePresetDialog", u"Randomizer Logic", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.patches_tab_widget), QCoreApplication.translate("CustomizePresetDialog", u"Game Modifications", None))
    # retranslateUi


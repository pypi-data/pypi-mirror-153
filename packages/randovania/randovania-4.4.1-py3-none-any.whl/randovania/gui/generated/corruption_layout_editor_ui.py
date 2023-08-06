# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'corruption_layout_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_CorruptionLayoutEditor(object):
    def setupUi(self, CorruptionLayoutEditor):
        if not CorruptionLayoutEditor.objectName():
            CorruptionLayoutEditor.setObjectName(u"CorruptionLayoutEditor")
        CorruptionLayoutEditor.resize(1025, 508)
        self.actionAction = QAction(CorruptionLayoutEditor)
        self.actionAction.setObjectName(u"actionAction")
        self.menu_reset_action = QAction(CorruptionLayoutEditor)
        self.menu_reset_action.setObjectName(u"menu_reset_action")
        self.central_widget = QWidget(CorruptionLayoutEditor)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, -1, 4, -1)
        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 1015, 439))
        self.scroll_area_layout = QHBoxLayout(self.scroll_area_contents)
        self.scroll_area_layout.setSpacing(6)
        self.scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.scroll_area_layout.setObjectName(u"scroll_area_layout")
        self.scroll_area_layout.setContentsMargins(2, 2, 2, 2)
        self.scroll_area.setWidget(self.scroll_area_contents)

        self.gridLayout.addWidget(self.scroll_area, 0, 0, 1, 2)

        self.layout_label = QLabel(self.central_widget)
        self.layout_label.setObjectName(u"layout_label")

        self.gridLayout.addWidget(self.layout_label, 1, 0, 1, 1)

        self.layout_edit = QLineEdit(self.central_widget)
        self.layout_edit.setObjectName(u"layout_edit")
        self.layout_edit.setReadOnly(True)

        self.gridLayout.addWidget(self.layout_edit, 1, 1, 1, 1)

        CorruptionLayoutEditor.setCentralWidget(self.central_widget)
        self.menu_bar = QMenuBar(CorruptionLayoutEditor)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1025, 21))
        CorruptionLayoutEditor.setMenuBar(self.menu_bar)

        self.retranslateUi(CorruptionLayoutEditor)

        QMetaObject.connectSlotsByName(CorruptionLayoutEditor)
    # setupUi

    def retranslateUi(self, CorruptionLayoutEditor):
        CorruptionLayoutEditor.setWindowTitle(QCoreApplication.translate("CorruptionLayoutEditor", u"Tracker", None))
        self.actionAction.setText(QCoreApplication.translate("CorruptionLayoutEditor", u"Action", None))
        self.menu_reset_action.setText(QCoreApplication.translate("CorruptionLayoutEditor", u"Reset", None))
        self.layout_label.setText(QCoreApplication.translate("CorruptionLayoutEditor", u"Layout string:", None))
    # retranslateUi


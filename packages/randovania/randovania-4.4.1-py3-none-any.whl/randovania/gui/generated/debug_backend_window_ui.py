# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debug_backend_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_DebugBackendWindow(object):
    def setupUi(self, DebugBackendWindow):
        if not DebugBackendWindow.objectName():
            DebugBackendWindow.setObjectName(u"DebugBackendWindow")
        DebugBackendWindow.resize(697, 430)
        self.central_widget = QWidget(DebugBackendWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.central_widget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 4, 3, 1, 1)

        self.messages_list = QListWidget(self.central_widget)
        self.messages_list.setObjectName(u"messages_list")

        self.gridLayout.addWidget(self.messages_list, 0, 2, 4, 2)

        self.inventory_box = QGroupBox(self.central_widget)
        self.inventory_box.setObjectName(u"inventory_box")
        self.gridLayout_2 = QGridLayout(self.inventory_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.inventory_box)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 305, 270))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.inventory_label = QLabel(self.scrollAreaWidgetContents)
        self.inventory_label.setObjectName(u"inventory_label")

        self.verticalLayout.addWidget(self.inventory_label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.inventory_box, 2, 0, 2, 2)

        self.collect_location_combo = QComboBox(self.central_widget)
        self.collect_location_combo.setObjectName(u"collect_location_combo")

        self.gridLayout.addWidget(self.collect_location_combo, 0, 0, 1, 2)

        self.collect_location_button = QPushButton(self.central_widget)
        self.collect_location_button.setObjectName(u"collect_location_button")

        self.gridLayout.addWidget(self.collect_location_button, 1, 1, 1, 1)

        self.collect_randomly_check = QCheckBox(self.central_widget)
        self.collect_randomly_check.setObjectName(u"collect_randomly_check")

        self.gridLayout.addWidget(self.collect_randomly_check, 4, 2, 1, 1)

        DebugBackendWindow.setCentralWidget(self.central_widget)
        self.menuBar = QMenuBar(DebugBackendWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 697, 22))
        DebugBackendWindow.setMenuBar(self.menuBar)

        self.retranslateUi(DebugBackendWindow)

        QMetaObject.connectSlotsByName(DebugBackendWindow)
    # setupUi

    def retranslateUi(self, DebugBackendWindow):
        DebugBackendWindow.setWindowTitle(QCoreApplication.translate("DebugBackendWindow", u"Debug Backend", None))
        self.reset_button.setText(QCoreApplication.translate("DebugBackendWindow", u"Reset", None))
        self.inventory_box.setTitle(QCoreApplication.translate("DebugBackendWindow", u"Inventory", None))
        self.inventory_label.setText("")
        self.collect_location_button.setText(QCoreApplication.translate("DebugBackendWindow", u"Collect Location", None))
        self.collect_randomly_check.setText(QCoreApplication.translate("DebugBackendWindow", u"Collect locations randomly periodically", None))
    # retranslateUi


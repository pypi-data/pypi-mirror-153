# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auto_tracker_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_AutoTrackerWindow(object):
    def setupUi(self, AutoTrackerWindow):
        if not AutoTrackerWindow.objectName():
            AutoTrackerWindow.setObjectName(u"AutoTrackerWindow")
        AutoTrackerWindow.resize(168, 199)
        self.action_theme_2d_style = QAction(AutoTrackerWindow)
        self.action_theme_2d_style.setObjectName(u"action_theme_2d_style")
        self.action_theme_2d_style.setCheckable(True)
        self.action_theme_game_icons = QAction(AutoTrackerWindow)
        self.action_theme_game_icons.setObjectName(u"action_theme_game_icons")
        self.action_theme_game_icons.setCheckable(True)
        self.actionasdf = QAction(AutoTrackerWindow)
        self.actionasdf.setObjectName(u"actionasdf")
        self.action_force_update = QAction(AutoTrackerWindow)
        self.action_force_update.setObjectName(u"action_force_update")
        self.centralwidget = QWidget(AutoTrackerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.connection_status_label = QLabel(self.centralwidget)
        self.connection_status_label.setObjectName(u"connection_status_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connection_status_label.sizePolicy().hasHeightForWidth())
        self.connection_status_label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.connection_status_label)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.inventory_group = QGroupBox(self.centralwidget)
        self.inventory_group.setObjectName(u"inventory_group")
        self.inventory_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.inventory_layout = QGridLayout(self.inventory_group)
        self.inventory_layout.setObjectName(u"inventory_layout")

        self.gridLayout.addWidget(self.inventory_group, 0, 0, 1, 1)

        AutoTrackerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(AutoTrackerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 168, 17))
        self.menu_options = QMenu(self.menubar)
        self.menu_options.setObjectName(u"menu_options")
        self.menu_tracker = QMenu(self.menu_options)
        self.menu_tracker.setObjectName(u"menu_tracker")
        self.menu_backend = QMenu(self.menu_options)
        self.menu_backend.setObjectName(u"menu_backend")
        AutoTrackerWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_options.menuAction())
        self.menu_options.addAction(self.menu_tracker.menuAction())
        self.menu_options.addAction(self.menu_backend.menuAction())
        self.menu_options.addAction(self.action_force_update)

        self.retranslateUi(AutoTrackerWindow)

        QMetaObject.connectSlotsByName(AutoTrackerWindow)
    # setupUi

    def retranslateUi(self, AutoTrackerWindow):
        AutoTrackerWindow.setWindowTitle(QCoreApplication.translate("AutoTrackerWindow", u"Auto Tracker", None))
        self.action_theme_2d_style.setText(QCoreApplication.translate("AutoTrackerWindow", u"2D Style", None))
        self.action_theme_game_icons.setText(QCoreApplication.translate("AutoTrackerWindow", u"Game Icons (Echoes only)", None))
        self.actionasdf.setText(QCoreApplication.translate("AutoTrackerWindow", u"asdf", None))
        self.action_force_update.setText(QCoreApplication.translate("AutoTrackerWindow", u"Force Update", None))
        self.connection_status_label.setText(QCoreApplication.translate("AutoTrackerWindow", u"Connection Status", None))
        self.inventory_group.setTitle(QCoreApplication.translate("AutoTrackerWindow", u"Inventory", None))
        self.menu_options.setTitle(QCoreApplication.translate("AutoTrackerWindow", u"Options", None))
        self.menu_tracker.setTitle(QCoreApplication.translate("AutoTrackerWindow", u"Tracker", None))
        self.menu_backend.setTitle(QCoreApplication.translate("AutoTrackerWindow", u"Choose game connection", None))
    # retranslateUi


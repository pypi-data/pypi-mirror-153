# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_details_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_GameDetailsWindow(object):
    def setupUi(self, GameDetailsWindow):
        if not GameDetailsWindow.objectName():
            GameDetailsWindow.setObjectName(u"GameDetailsWindow")
        GameDetailsWindow.resize(624, 471)
        self.centralWidget = QWidget(GameDetailsWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.centralWidget.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.layout_info_tab = QTabWidget(self.centralWidget)
        self.layout_info_tab.setObjectName(u"layout_info_tab")
        self.details_tab = QWidget()
        self.details_tab.setObjectName(u"details_tab")
        self.details_tab_layout = QGridLayout(self.details_tab)
        self.details_tab_layout.setSpacing(6)
        self.details_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.details_tab_layout.setObjectName(u"details_tab_layout")
        self.details_tab_layout.setContentsMargins(4, 8, 4, 0)
        self.layout_description_left_label = QLabel(self.details_tab)
        self.layout_description_left_label.setObjectName(u"layout_description_left_label")
        self.layout_description_left_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.layout_description_left_label.setWordWrap(True)

        self.details_tab_layout.addWidget(self.layout_description_left_label, 3, 0, 1, 3)

        self.layout_description_right_label = QLabel(self.details_tab)
        self.layout_description_right_label.setObjectName(u"layout_description_right_label")
        self.layout_description_right_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.layout_description_right_label.setWordWrap(True)

        self.details_tab_layout.addWidget(self.layout_description_right_label, 3, 3, 1, 4)

        self.layout_title_label = QLabel(self.details_tab)
        self.layout_title_label.setObjectName(u"layout_title_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layout_title_label.sizePolicy().hasHeightForWidth())
        self.layout_title_label.setSizePolicy(sizePolicy)
        self.layout_title_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.details_tab_layout.addWidget(self.layout_title_label, 1, 0, 1, 4)

        self.player_index_combo = QComboBox(self.details_tab)
        self.player_index_combo.setObjectName(u"player_index_combo")

        self.details_tab_layout.addWidget(self.player_index_combo, 2, 0, 1, 4)

        self.customize_user_preferences_button = QPushButton(self.details_tab)
        self.customize_user_preferences_button.setObjectName(u"customize_user_preferences_button")

        self.details_tab_layout.addWidget(self.customize_user_preferences_button, 2, 4, 1, 2)

        self.export_log_button = QPushButton(self.details_tab)
        self.export_log_button.setObjectName(u"export_log_button")

        self.details_tab_layout.addWidget(self.export_log_button, 1, 5, 1, 1)

        self.export_iso_button = QPushButton(self.details_tab)
        self.export_iso_button.setObjectName(u"export_iso_button")

        self.details_tab_layout.addWidget(self.export_iso_button, 1, 4, 1, 1)

        self.permalink_edit = QLineEdit(self.details_tab)
        self.permalink_edit.setObjectName(u"permalink_edit")
        self.permalink_edit.setReadOnly(True)

        self.details_tab_layout.addWidget(self.permalink_edit, 0, 1, 1, 3)

        self.permalink_label = QLabel(self.details_tab)
        self.permalink_label.setObjectName(u"permalink_label")

        self.details_tab_layout.addWidget(self.permalink_label, 0, 0, 1, 1)

        self.progress_box = QGroupBox(self.details_tab)
        self.progress_box.setObjectName(u"progress_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progress_box.sizePolicy().hasHeightForWidth())
        self.progress_box.setSizePolicy(sizePolicy1)
        self.progress_box_layout = QGridLayout(self.progress_box)
        self.progress_box_layout.setSpacing(6)
        self.progress_box_layout.setContentsMargins(11, 11, 11, 11)
        self.progress_box_layout.setObjectName(u"progress_box_layout")
        self.progress_box_layout.setContentsMargins(2, 4, 2, 4)
        self.stop_background_process_button = QPushButton(self.progress_box)
        self.stop_background_process_button.setObjectName(u"stop_background_process_button")
        self.stop_background_process_button.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stop_background_process_button.sizePolicy().hasHeightForWidth())
        self.stop_background_process_button.setSizePolicy(sizePolicy2)
        self.stop_background_process_button.setMaximumSize(QSize(75, 16777215))
        self.stop_background_process_button.setCheckable(False)
        self.stop_background_process_button.setFlat(False)

        self.progress_box_layout.addWidget(self.stop_background_process_button, 0, 3, 1, 1)

        self.progress_label = QLabel(self.progress_box)
        self.progress_label.setObjectName(u"progress_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progress_label.sizePolicy().hasHeightForWidth())
        self.progress_label.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setPointSize(7)
        self.progress_label.setFont(font)
        self.progress_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_label.setWordWrap(True)

        self.progress_box_layout.addWidget(self.progress_label, 0, 2, 1, 1)

        self.progress_bar = QProgressBar(self.progress_box)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMinimumSize(QSize(150, 0))
        self.progress_bar.setMaximumSize(QSize(150, 16777215))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setInvertedAppearance(False)

        self.progress_box_layout.addWidget(self.progress_bar, 0, 0, 1, 2)


        self.details_tab_layout.addWidget(self.progress_box, 4, 0, 1, 7)

        self.tool_button = QToolButton(self.details_tab)
        self.tool_button.setObjectName(u"tool_button")
        self.tool_button.setPopupMode(QToolButton.InstantPopup)

        self.details_tab_layout.addWidget(self.tool_button, 1, 6, 1, 1)

        self.layout_info_tab.addTab(self.details_tab, "")

        self.verticalLayout.addWidget(self.layout_info_tab)

        GameDetailsWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(GameDetailsWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 624, 20))
        GameDetailsWindow.setMenuBar(self.menuBar)

        self.retranslateUi(GameDetailsWindow)

        self.layout_info_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(GameDetailsWindow)
    # setupUi

    def retranslateUi(self, GameDetailsWindow):
        GameDetailsWindow.setWindowTitle(QCoreApplication.translate("GameDetailsWindow", u"Game Details", None))
        self.layout_description_left_label.setText(QCoreApplication.translate("GameDetailsWindow", u"<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None))
        self.layout_description_right_label.setText(QCoreApplication.translate("GameDetailsWindow", u"<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None))
        self.layout_title_label.setText(QCoreApplication.translate("GameDetailsWindow", u"<html><head/><body><p>Seed Hash: ????<br/>Preset Name: ???</p></body></html>", None))
        self.customize_user_preferences_button.setText(QCoreApplication.translate("GameDetailsWindow", u"Customize cosmetic options", None))
        self.export_log_button.setText(QCoreApplication.translate("GameDetailsWindow", u"Save Spoiler", None))
        self.export_iso_button.setText(QCoreApplication.translate("GameDetailsWindow", u"Export Game", None))
        self.permalink_edit.setText(QCoreApplication.translate("GameDetailsWindow", u"<insert permalink here>", None))
        self.permalink_label.setText(QCoreApplication.translate("GameDetailsWindow", u"Permalink:", None))
        self.progress_box.setTitle(QCoreApplication.translate("GameDetailsWindow", u"Progress", None))
        self.stop_background_process_button.setText(QCoreApplication.translate("GameDetailsWindow", u"Stop", None))
        self.progress_label.setText("")
        self.tool_button.setText(QCoreApplication.translate("GameDetailsWindow", u"...", None))
        self.layout_info_tab.setTabText(self.layout_info_tab.indexOf(self.details_tab), QCoreApplication.translate("GameDetailsWindow", u"Summary", None))
    # retranslateUi


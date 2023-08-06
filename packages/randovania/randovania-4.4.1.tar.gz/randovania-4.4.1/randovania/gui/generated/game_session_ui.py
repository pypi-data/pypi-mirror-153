# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_session.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_GameSessionWindow(object):
    def setupUi(self, GameSessionWindow):
        if not GameSessionWindow.objectName():
            GameSessionWindow.setObjectName(u"GameSessionWindow")
        GameSessionWindow.resize(773, 418)
        GameSessionWindow.setDockNestingEnabled(True)
        self.action_add_player = QAction(GameSessionWindow)
        self.action_add_player.setObjectName(u"action_add_player")
        self.action_add_row = QAction(GameSessionWindow)
        self.action_add_row.setObjectName(u"action_add_row")
        self.rename_session_action = QAction(GameSessionWindow)
        self.rename_session_action.setObjectName(u"rename_session_action")
        self.change_password_action = QAction(GameSessionWindow)
        self.change_password_action.setObjectName(u"change_password_action")
        self.delete_session_action = QAction(GameSessionWindow)
        self.delete_session_action.setObjectName(u"delete_session_action")
        self.actionbar = QAction(GameSessionWindow)
        self.actionbar.setObjectName(u"actionbar")
        self.actionasdf = QAction(GameSessionWindow)
        self.actionasdf.setObjectName(u"actionasdf")
        self.central_widget = QWidget(GameSessionWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.game_connection_tool = QToolButton(self.central_widget)
        self.game_connection_tool.setObjectName(u"game_connection_tool")
        self.game_connection_tool.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.game_connection_tool)

        self.game_connection_label = QLabel(self.central_widget)
        self.game_connection_label.setObjectName(u"game_connection_label")

        self.horizontalLayout.addWidget(self.game_connection_label)

        self.connection_line_1 = QFrame(self.central_widget)
        self.connection_line_1.setObjectName(u"connection_line_1")
        self.connection_line_1.setFrameShape(QFrame.VLine)
        self.connection_line_1.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.connection_line_1)

        self.server_connection_button = QPushButton(self.central_widget)
        self.server_connection_button.setObjectName(u"server_connection_button")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.server_connection_button.sizePolicy().hasHeightForWidth())
        self.server_connection_button.setSizePolicy(sizePolicy)
        self.server_connection_button.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.server_connection_button)

        self.server_connection_label = QLabel(self.central_widget)
        self.server_connection_label.setObjectName(u"server_connection_label")

        self.horizontalLayout.addWidget(self.server_connection_label)

        self.connection_line_2 = QFrame(self.central_widget)
        self.connection_line_2.setObjectName(u"connection_line_2")
        self.connection_line_2.setFrameShape(QFrame.VLine)
        self.connection_line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.connection_line_2)

        self.session_status_tool = QToolButton(self.central_widget)
        self.session_status_tool.setObjectName(u"session_status_tool")
        self.session_status_tool.setMaximumSize(QSize(80, 16777215))
        self.session_status_tool.setPopupMode(QToolButton.MenuButtonPopup)

        self.horizontalLayout.addWidget(self.session_status_tool)

        self.session_status_label = QLabel(self.central_widget)
        self.session_status_label.setObjectName(u"session_status_label")

        self.horizontalLayout.addWidget(self.session_status_label)

        self.connection_line_3 = QFrame(self.central_widget)
        self.connection_line_3.setObjectName(u"connection_line_3")
        self.connection_line_3.setFrameShape(QFrame.VLine)
        self.connection_line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.connection_line_3)

        self.advanced_options_tool = QToolButton(self.central_widget)
        self.advanced_options_tool.setObjectName(u"advanced_options_tool")
        self.advanced_options_tool.setPopupMode(QToolButton.InstantPopup)

        self.horizontalLayout.addWidget(self.advanced_options_tool)

        GameSessionWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QMenuBar(GameSessionWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 773, 17))
        GameSessionWindow.setMenuBar(self.menu_bar)
        self.players_dock = QDockWidget(GameSessionWindow)
        self.players_dock.setObjectName(u"players_dock")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.players_dock.sizePolicy().hasHeightForWidth())
        self.players_dock.setSizePolicy(sizePolicy1)
        self.players_dock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.players_dock_contents = QWidget()
        self.players_dock_contents.setObjectName(u"players_dock_contents")
        self.players_dock_layout = QVBoxLayout(self.players_dock_contents)
        self.players_dock_layout.setSpacing(0)
        self.players_dock_layout.setContentsMargins(11, 11, 11, 11)
        self.players_dock_layout.setObjectName(u"players_dock_layout")
        self.players_dock_layout.setContentsMargins(0, 0, 0, 0)
        self.players_box_scroll = QScrollArea(self.players_dock_contents)
        self.players_box_scroll.setObjectName(u"players_box_scroll")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.players_box_scroll.sizePolicy().hasHeightForWidth())
        self.players_box_scroll.setSizePolicy(sizePolicy2)
        self.players_box_scroll.setWidgetResizable(True)
        self.players_box = QWidget()
        self.players_box.setObjectName(u"players_box")
        self.players_box.setGeometry(QRect(0, 0, 203, 180))
        self.players_layout = QGridLayout(self.players_box)
        self.players_layout.setSpacing(6)
        self.players_layout.setContentsMargins(11, 11, 11, 11)
        self.players_layout.setObjectName(u"players_layout")
        self.presets_line = QFrame(self.players_box)
        self.presets_line.setObjectName(u"presets_line")
        self.presets_line.setFrameShape(QFrame.HLine)
        self.presets_line.setFrameShadow(QFrame.Sunken)

        self.players_layout.addWidget(self.presets_line, 1, 0, 1, 2)

        self.title_connection_state_label = QLabel(self.players_box)
        self.title_connection_state_label.setObjectName(u"title_connection_state_label")

        self.players_layout.addWidget(self.title_connection_state_label, 0, 4, 1, 1)

        self.players_vertical_line = QFrame(self.players_box)
        self.players_vertical_line.setObjectName(u"players_vertical_line")
        self.players_vertical_line.setFrameShape(QFrame.VLine)
        self.players_vertical_line.setFrameShadow(QFrame.Sunken)

        self.players_layout.addWidget(self.players_vertical_line, 0, 2, 1, 1)

        self.team_line = QFrame(self.players_box)
        self.team_line.setObjectName(u"team_line")
        self.team_line.setFrameShape(QFrame.HLine)
        self.team_line.setFrameShadow(QFrame.Sunken)

        self.players_layout.addWidget(self.team_line, 1, 3, 1, 2)

        self.new_row_button = QPushButton(self.players_box)
        self.new_row_button.setObjectName(u"new_row_button")

        self.players_layout.addWidget(self.new_row_button, 0, 0, 1, 2)

        self.title_player_name_label = QLabel(self.players_box)
        self.title_player_name_label.setObjectName(u"title_player_name_label")

        self.players_layout.addWidget(self.title_player_name_label, 0, 3, 1, 1)

        self.players_box_scroll.setWidget(self.players_box)

        self.players_dock_layout.addWidget(self.players_box_scroll)

        self.players_dock.setWidget(self.players_dock_contents)
        GameSessionWindow.addDockWidget(Qt.TopDockWidgetArea, self.players_dock)
        self.observers_dock = QDockWidget(GameSessionWindow)
        self.observers_dock.setObjectName(u"observers_dock")
        self.observers_dock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.observers_dock_contents = QWidget()
        self.observers_dock_contents.setObjectName(u"observers_dock_contents")
        self.observer_layout = QGridLayout(self.observers_dock_contents)
        self.observer_layout.setSpacing(6)
        self.observer_layout.setContentsMargins(11, 11, 11, 11)
        self.observer_layout.setObjectName(u"observer_layout")
        self.observers_dock.setWidget(self.observers_dock_contents)
        GameSessionWindow.addDockWidget(Qt.TopDockWidgetArea, self.observers_dock)
        self.game_dock = QDockWidget(GameSessionWindow)
        self.game_dock.setObjectName(u"game_dock")
        self.game_dock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.game_dock_contents = QWidget()
        self.game_dock_contents.setObjectName(u"game_dock_contents")
        self.game_dock_layout = QGridLayout(self.game_dock_contents)
        self.game_dock_layout.setSpacing(6)
        self.game_dock_layout.setContentsMargins(11, 11, 11, 11)
        self.game_dock_layout.setObjectName(u"game_dock_layout")
        self.generate_game_label = QLabel(self.game_dock_contents)
        self.generate_game_label.setObjectName(u"generate_game_label")
        self.generate_game_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.game_dock_layout.addWidget(self.generate_game_label, 0, 0, 1, 2)

        self.view_game_details_button = QPushButton(self.game_dock_contents)
        self.view_game_details_button.setObjectName(u"view_game_details_button")

        self.game_dock_layout.addWidget(self.view_game_details_button, 0, 2, 1, 1)

        self.save_iso_button = QToolButton(self.game_dock_contents)
        self.save_iso_button.setObjectName(u"save_iso_button")
        self.save_iso_button.setMinimumSize(QSize(100, 0))
        self.save_iso_button.setPopupMode(QToolButton.MenuButtonPopup)

        self.game_dock_layout.addWidget(self.save_iso_button, 0, 3, 1, 1)

        self.customize_user_preferences_button = QPushButton(self.game_dock_contents)
        self.customize_user_preferences_button.setObjectName(u"customize_user_preferences_button")

        self.game_dock_layout.addWidget(self.customize_user_preferences_button, 0, 4, 1, 1)

        self.line_generate = QFrame(self.game_dock_contents)
        self.line_generate.setObjectName(u"line_generate")
        self.line_generate.setFrameShape(QFrame.HLine)
        self.line_generate.setFrameShadow(QFrame.Sunken)

        self.game_dock_layout.addWidget(self.line_generate, 1, 0, 1, 5)

        self.background_process_button = QToolButton(self.game_dock_contents)
        self.background_process_button.setObjectName(u"background_process_button")
        self.background_process_button.setMinimumSize(QSize(140, 0))
        self.background_process_button.setPopupMode(QToolButton.MenuButtonPopup)

        self.game_dock_layout.addWidget(self.background_process_button, 2, 0, 1, 1)

        self.progress_label = QLabel(self.game_dock_contents)
        self.progress_label.setObjectName(u"progress_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progress_label.sizePolicy().hasHeightForWidth())
        self.progress_label.setSizePolicy(sizePolicy3)
        self.progress_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_label.setWordWrap(True)

        self.game_dock_layout.addWidget(self.progress_label, 2, 1, 1, 2)

        self.progress_bar = QProgressBar(self.game_dock_contents)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)
        self.progress_bar.setInvertedAppearance(False)

        self.game_dock_layout.addWidget(self.progress_bar, 2, 3, 1, 2)

        self.game_dock.setWidget(self.game_dock_contents)
        GameSessionWindow.addDockWidget(Qt.TopDockWidgetArea, self.game_dock)
        self.history_dock = QDockWidget(GameSessionWindow)
        self.history_dock.setObjectName(u"history_dock")
        self.history_dock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.history_dock_contents = QWidget()
        self.history_dock_contents.setObjectName(u"history_dock_contents")
        self.history_layout = QVBoxLayout(self.history_dock_contents)
        self.history_layout.setSpacing(6)
        self.history_layout.setContentsMargins(11, 11, 11, 11)
        self.history_layout.setObjectName(u"history_layout")
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_table_widget = QTableWidget(self.history_dock_contents)
        if (self.history_table_widget.columnCount() < 5):
            self.history_table_widget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.history_table_widget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.history_table_widget.setObjectName(u"history_table_widget")
        self.history_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table_widget.setSortingEnabled(True)
        self.history_table_widget.horizontalHeader().setVisible(False)
        self.history_table_widget.horizontalHeader().setDefaultSectionSize(200)
        self.history_table_widget.verticalHeader().setVisible(False)

        self.history_layout.addWidget(self.history_table_widget)

        self.history_dock.setWidget(self.history_dock_contents)
        GameSessionWindow.addDockWidget(Qt.TopDockWidgetArea, self.history_dock)
        self.audit_dock = QDockWidget(GameSessionWindow)
        self.audit_dock.setObjectName(u"audit_dock")
        self.audit_dock.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.audit_dock_contents = QWidget()
        self.audit_dock_contents.setObjectName(u"audit_dock_contents")
        self.audit_dock_layout = QVBoxLayout(self.audit_dock_contents)
        self.audit_dock_layout.setSpacing(0)
        self.audit_dock_layout.setContentsMargins(11, 11, 11, 11)
        self.audit_dock_layout.setObjectName(u"audit_dock_layout")
        self.audit_dock_layout.setContentsMargins(0, 2, 0, 0)
        self.audit_table_widget = QTableWidget(self.audit_dock_contents)
        if (self.audit_table_widget.columnCount() < 3):
            self.audit_table_widget.setColumnCount(3)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.audit_table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.audit_table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.audit_table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        self.audit_table_widget.setObjectName(u"audit_table_widget")
        self.audit_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.audit_table_widget.setSortingEnabled(True)
        self.audit_table_widget.horizontalHeader().setVisible(True)
        self.audit_table_widget.horizontalHeader().setDefaultSectionSize(200)
        self.audit_table_widget.verticalHeader().setVisible(False)

        self.audit_dock_layout.addWidget(self.audit_table_widget)

        self.audit_dock.setWidget(self.audit_dock_contents)
        GameSessionWindow.addDockWidget(Qt.LeftDockWidgetArea, self.audit_dock)

        self.retranslateUi(GameSessionWindow)

        QMetaObject.connectSlotsByName(GameSessionWindow)
    # setupUi

    def retranslateUi(self, GameSessionWindow):
        GameSessionWindow.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"Game Session", None))
        self.action_add_player.setText(QCoreApplication.translate("GameSessionWindow", u"Add player", None))
        self.action_add_row.setText(QCoreApplication.translate("GameSessionWindow", u"Add row", None))
        self.rename_session_action.setText(QCoreApplication.translate("GameSessionWindow", u"Change title", None))
        self.change_password_action.setText(QCoreApplication.translate("GameSessionWindow", u"Change password", None))
        self.delete_session_action.setText(QCoreApplication.translate("GameSessionWindow", u"Delete session", None))
        self.actionbar.setText(QCoreApplication.translate("GameSessionWindow", u"bar", None))
        self.actionasdf.setText(QCoreApplication.translate("GameSessionWindow", u"asdf", None))
        self.game_connection_tool.setText(QCoreApplication.translate("GameSessionWindow", u"Connect to game", None))
        self.game_connection_label.setText(QCoreApplication.translate("GameSessionWindow", u"Game: Disconnected", None))
        self.server_connection_button.setText(QCoreApplication.translate("GameSessionWindow", u"Connect", None))
        self.server_connection_label.setText(QCoreApplication.translate("GameSessionWindow", u"Server: Disconnected", None))
        self.session_status_tool.setText(QCoreApplication.translate("GameSessionWindow", u"Start", None))
        self.session_status_label.setText(QCoreApplication.translate("GameSessionWindow", u"Session: Not Started", None))
        self.advanced_options_tool.setText(QCoreApplication.translate("GameSessionWindow", u"Advanced options...", None))
        self.players_dock.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"Session", None))
        self.title_connection_state_label.setText(QCoreApplication.translate("GameSessionWindow", u"Connection state", None))
        self.new_row_button.setText(QCoreApplication.translate("GameSessionWindow", u"New Row", None))
        self.title_player_name_label.setText(QCoreApplication.translate("GameSessionWindow", u"Players", None))
        self.observers_dock.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"Observers", None))
        self.game_dock.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"Game", None))
        self.generate_game_label.setText(QCoreApplication.translate("GameSessionWindow", u"<Game not generated>", None))
        self.view_game_details_button.setText(QCoreApplication.translate("GameSessionWindow", u"View Spoiler", None))
        self.save_iso_button.setText(QCoreApplication.translate("GameSessionWindow", u"Export Game", None))
        self.customize_user_preferences_button.setText(QCoreApplication.translate("GameSessionWindow", u"Customize in-game settings", None))
        self.background_process_button.setText(QCoreApplication.translate("GameSessionWindow", u"Stop", None))
        self.progress_label.setText("")
        self.history_dock.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"History", None))
        ___qtablewidgetitem = self.history_table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("GameSessionWindow", u"Provider", None));
        ___qtablewidgetitem1 = self.history_table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("GameSessionWindow", u"Receiver", None));
        ___qtablewidgetitem2 = self.history_table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("GameSessionWindow", u"Pickup", None));
        ___qtablewidgetitem3 = self.history_table_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("GameSessionWindow", u"Location", None));
        ___qtablewidgetitem4 = self.history_table_widget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("GameSessionWindow", u"Time", None));
        self.audit_dock.setWindowTitle(QCoreApplication.translate("GameSessionWindow", u"Audit Log", None))
        ___qtablewidgetitem5 = self.audit_table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("GameSessionWindow", u"User", None));
        ___qtablewidgetitem6 = self.audit_table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("GameSessionWindow", u"Message", None));
        ___qtablewidgetitem7 = self.audit_table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("GameSessionWindow", u"Time", None));
    # retranslateUi


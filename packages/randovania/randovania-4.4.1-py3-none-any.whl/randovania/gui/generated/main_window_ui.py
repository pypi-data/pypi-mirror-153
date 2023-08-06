# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.lib.preset_tree_widget import *  # type: ignore
from randovania.gui.widgets.games_help_widget import *  # type: ignore
from randovania.gui.widgets.randovania_help_widget import *  # type: ignore

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(645, 613)
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.menu_action_edit_existing_database = QAction(MainWindow)
        self.menu_action_edit_existing_database.setObjectName(u"menu_action_edit_existing_database")
        self.menu_action_validate_seed_after = QAction(MainWindow)
        self.menu_action_validate_seed_after.setObjectName(u"menu_action_validate_seed_after")
        self.menu_action_validate_seed_after.setCheckable(True)
        self.menu_action_validate_seed_after.setChecked(True)
        self.menu_action_timeout_generation_after_a_time_limit = QAction(MainWindow)
        self.menu_action_timeout_generation_after_a_time_limit.setObjectName(u"menu_action_timeout_generation_after_a_time_limit")
        self.menu_action_timeout_generation_after_a_time_limit.setCheckable(True)
        self.menu_action_timeout_generation_after_a_time_limit.setChecked(True)
        self.menu_action_open_auto_tracker = QAction(MainWindow)
        self.menu_action_open_auto_tracker.setObjectName(u"menu_action_open_auto_tracker")
        self.action_login_window = QAction(MainWindow)
        self.action_login_window.setObjectName(u"action_login_window")
        self.menu_action_dark_mode = QAction(MainWindow)
        self.menu_action_dark_mode.setObjectName(u"menu_action_dark_mode")
        self.menu_action_dark_mode.setCheckable(True)
        self.menu_action_previously_generated_games = QAction(MainWindow)
        self.menu_action_previously_generated_games.setObjectName(u"menu_action_previously_generated_games")
        self.menu_action_layout_editor = QAction(MainWindow)
        self.menu_action_layout_editor.setObjectName(u"menu_action_layout_editor")
        self.menu_action_log_files_directory = QAction(MainWindow)
        self.menu_action_log_files_directory.setObjectName(u"menu_action_log_files_directory")
        self.menu_action_experimental_games = QAction(MainWindow)
        self.menu_action_experimental_games.setObjectName(u"menu_action_experimental_games")
        self.menu_action_experimental_games.setCheckable(True)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.main_tab_widget = QTabWidget(self.centralWidget)
        self.main_tab_widget.setObjectName(u"main_tab_widget")
        self.welcome_tab = QWidget()
        self.welcome_tab.setObjectName(u"welcome_tab")
        self.welcome_layout = QGridLayout(self.welcome_tab)
        self.welcome_layout.setSpacing(6)
        self.welcome_layout.setContentsMargins(11, 11, 11, 11)
        self.welcome_layout.setObjectName(u"welcome_layout")
        self.welcome_layout.setContentsMargins(4, 4, 4, 0)
        self.intro_vertical_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.welcome_layout.addItem(self.intro_vertical_spacer, 3, 1, 1, 1)

        self.intro_welcome_label = QLabel(self.welcome_tab)
        self.intro_welcome_label.setObjectName(u"intro_welcome_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intro_welcome_label.sizePolicy().hasHeightForWidth())
        self.intro_welcome_label.setSizePolicy(sizePolicy)
        self.intro_welcome_label.setTextFormat(Qt.MarkdownText)
        self.intro_welcome_label.setWordWrap(True)

        self.welcome_layout.addWidget(self.intro_welcome_label, 2, 0, 1, 3)

        self.intro_top_spacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.welcome_layout.addItem(self.intro_top_spacer, 5, 1, 1, 1)

        self.open_faq_button = QPushButton(self.welcome_tab)
        self.open_faq_button.setObjectName(u"open_faq_button")

        self.welcome_layout.addWidget(self.open_faq_button, 7, 0, 1, 1)

        self.intro_play_now_button = QPushButton(self.welcome_tab)
        self.intro_play_now_button.setObjectName(u"intro_play_now_button")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.intro_play_now_button.setFont(font)

        self.welcome_layout.addWidget(self.intro_play_now_button, 4, 1, 1, 1)

        self.intro_label = QLabel(self.welcome_tab)
        self.intro_label.setObjectName(u"intro_label")
        self.intro_label.setTextFormat(Qt.MarkdownText)
        self.intro_label.setScaledContents(False)
        self.intro_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.intro_label.setWordWrap(True)
        self.intro_label.setMargin(7)
        self.intro_label.setIndent(-1)
        self.intro_label.setOpenExternalLinks(False)

        self.welcome_layout.addWidget(self.intro_label, 0, 0, 1, 3)

        self.help_offer_label = QLabel(self.welcome_tab)
        self.help_offer_label.setObjectName(u"help_offer_label")
        self.help_offer_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.help_offer_label.setWordWrap(True)

        self.welcome_layout.addWidget(self.help_offer_label, 6, 0, 1, 3)

        self.intro_bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.welcome_layout.addItem(self.intro_bottom_spacer, 8, 1, 1, 1)

        self.open_database_viewer_button = QPushButton(self.welcome_tab)
        self.open_database_viewer_button.setObjectName(u"open_database_viewer_button")

        self.welcome_layout.addWidget(self.open_database_viewer_button, 7, 2, 1, 1)

        self.intro_games_layout = QHBoxLayout()
        self.intro_games_layout.setSpacing(6)
        self.intro_games_layout.setObjectName(u"intro_games_layout")
        self.intro_games_layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.games_supported_label = QLabel(self.welcome_tab)
        self.games_supported_label.setObjectName(u"games_supported_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.games_supported_label.sizePolicy().hasHeightForWidth())
        self.games_supported_label.setSizePolicy(sizePolicy1)
        self.games_supported_label.setTextFormat(Qt.MarkdownText)

        self.intro_games_layout.addWidget(self.games_supported_label)

        self.games_experimental_label = QLabel(self.welcome_tab)
        self.games_experimental_label.setObjectName(u"games_experimental_label")
        sizePolicy1.setHeightForWidth(self.games_experimental_label.sizePolicy().hasHeightForWidth())
        self.games_experimental_label.setSizePolicy(sizePolicy1)
        self.games_experimental_label.setTextFormat(Qt.MarkdownText)
        self.games_experimental_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.intro_games_layout.addWidget(self.games_experimental_label)


        self.welcome_layout.addLayout(self.intro_games_layout, 1, 0, 1, 3)

        self.main_tab_widget.addTab(self.welcome_tab, "")
        self.tab_play = QWidget()
        self.tab_play.setObjectName(u"tab_play")
        self.play_layout = QVBoxLayout(self.tab_play)
        self.play_layout.setSpacing(6)
        self.play_layout.setContentsMargins(11, 11, 11, 11)
        self.play_layout.setObjectName(u"play_layout")
        self.play_layout.setContentsMargins(4, 0, 0, 0)
        self.play_top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.play_layout.addItem(self.play_top_spacer)

        self.play_existing_permalink_group = QGroupBox(self.tab_play)
        self.play_existing_permalink_group.setObjectName(u"play_existing_permalink_group")
        self.play_existing_permalink_layout = QGridLayout(self.play_existing_permalink_group)
        self.play_existing_permalink_layout.setSpacing(6)
        self.play_existing_permalink_layout.setContentsMargins(11, 11, 11, 11)
        self.play_existing_permalink_layout.setObjectName(u"play_existing_permalink_layout")
        self.import_permalink_button = QPushButton(self.play_existing_permalink_group)
        self.import_permalink_button.setObjectName(u"import_permalink_button")

        self.play_existing_permalink_layout.addWidget(self.import_permalink_button, 1, 0, 1, 1)

        self.browse_sessions_button = QPushButton(self.play_existing_permalink_group)
        self.browse_sessions_button.setObjectName(u"browse_sessions_button")

        self.play_existing_permalink_layout.addWidget(self.browse_sessions_button, 3, 1, 1, 1)

        self.import_permalink_label = QLabel(self.play_existing_permalink_group)
        self.import_permalink_label.setObjectName(u"import_permalink_label")
        self.import_permalink_label.setWordWrap(True)

        self.play_existing_permalink_layout.addWidget(self.import_permalink_label, 0, 0, 1, 1)

        self.import_game_file_label = QLabel(self.play_existing_permalink_group)
        self.import_game_file_label.setObjectName(u"import_game_file_label")
        self.import_game_file_label.setWordWrap(True)

        self.play_existing_permalink_layout.addWidget(self.import_game_file_label, 2, 0, 1, 1)

        self.browse_racetime_label = QLabel(self.play_existing_permalink_group)
        self.browse_racetime_label.setObjectName(u"browse_racetime_label")
        self.browse_racetime_label.setTextFormat(Qt.AutoText)
        self.browse_racetime_label.setWordWrap(True)
        self.browse_racetime_label.setOpenExternalLinks(True)

        self.play_existing_permalink_layout.addWidget(self.browse_racetime_label, 0, 1, 1, 1)

        self.import_game_file_button = QPushButton(self.play_existing_permalink_group)
        self.import_game_file_button.setObjectName(u"import_game_file_button")

        self.play_existing_permalink_layout.addWidget(self.import_game_file_button, 3, 0, 1, 1)

        self.browse_racetime_button = QPushButton(self.play_existing_permalink_group)
        self.browse_racetime_button.setObjectName(u"browse_racetime_button")

        self.play_existing_permalink_layout.addWidget(self.browse_racetime_button, 1, 1, 1, 1)

        self.browse_sessions_label = QLabel(self.play_existing_permalink_group)
        self.browse_sessions_label.setObjectName(u"browse_sessions_label")
        self.browse_sessions_label.setWordWrap(True)

        self.play_existing_permalink_layout.addWidget(self.browse_sessions_label, 2, 1, 1, 1)


        self.play_layout.addWidget(self.play_existing_permalink_group)

        self.play_middle_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.play_layout.addItem(self.play_middle_spacer)

        self.play_new_game_group = QGroupBox(self.tab_play)
        self.play_new_game_group.setObjectName(u"play_new_game_group")
        self.play_new_permalink_layout = QGridLayout(self.play_new_game_group)
        self.play_new_permalink_layout.setSpacing(6)
        self.play_new_permalink_layout.setContentsMargins(11, 11, 11, 11)
        self.play_new_permalink_layout.setObjectName(u"play_new_permalink_layout")
        self.host_new_game_label = QLabel(self.play_new_game_group)
        self.host_new_game_label.setObjectName(u"host_new_game_label")
        self.host_new_game_label.setWordWrap(True)

        self.play_new_permalink_layout.addWidget(self.host_new_game_label, 2, 0, 1, 1)

        self.create_new_seed_label = QLabel(self.play_new_game_group)
        self.create_new_seed_label.setObjectName(u"create_new_seed_label")

        self.play_new_permalink_layout.addWidget(self.create_new_seed_label, 0, 0, 1, 1)

        self.create_new_seed_button = QPushButton(self.play_new_game_group)
        self.create_new_seed_button.setObjectName(u"create_new_seed_button")

        self.play_new_permalink_layout.addWidget(self.create_new_seed_button, 1, 0, 1, 1)

        self.host_new_game_button = QPushButton(self.play_new_game_group)
        self.host_new_game_button.setObjectName(u"host_new_game_button")

        self.play_new_permalink_layout.addWidget(self.host_new_game_button, 3, 0, 1, 1)


        self.play_layout.addWidget(self.play_new_game_group)

        self.play_bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.play_layout.addItem(self.play_bottom_spacer)

        self.main_tab_widget.addTab(self.tab_play, "")
        self.tab_create_seed = QWidget()
        self.tab_create_seed.setObjectName(u"tab_create_seed")
        self.create_layout = QGridLayout(self.tab_create_seed)
        self.create_layout.setSpacing(6)
        self.create_layout.setContentsMargins(11, 11, 11, 11)
        self.create_layout.setObjectName(u"create_layout")
        self.create_layout.setContentsMargins(4, 4, 4, 0)
        self.create_generate_no_retry_button = QPushButton(self.tab_create_seed)
        self.create_generate_no_retry_button.setObjectName(u"create_generate_no_retry_button")

        self.create_layout.addWidget(self.create_generate_no_retry_button, 4, 0, 1, 1)

        self.create_generate_race_button = QPushButton(self.tab_create_seed)
        self.create_generate_race_button.setObjectName(u"create_generate_race_button")

        self.create_layout.addWidget(self.create_generate_race_button, 4, 2, 1, 1)

        self.create_generate_button = QPushButton(self.tab_create_seed)
        self.create_generate_button.setObjectName(u"create_generate_button")

        self.create_layout.addWidget(self.create_generate_button, 4, 1, 1, 1)

        self.num_players_spin_box = QSpinBox(self.tab_create_seed)
        self.num_players_spin_box.setObjectName(u"num_players_spin_box")
        self.num_players_spin_box.setCursor(QCursor(Qt.ArrowCursor))
        self.num_players_spin_box.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.num_players_spin_box.setMinimum(1)

        self.create_layout.addWidget(self.num_players_spin_box, 4, 3, 1, 1)

        self.create_preset_tree = PresetTreeWidget(self.tab_create_seed)
        __qtreewidgetitem = QTreeWidgetItem(self.create_preset_tree)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(self.create_preset_tree)
        self.create_preset_tree.setObjectName(u"create_preset_tree")
        sizePolicy2 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.create_preset_tree.sizePolicy().hasHeightForWidth())
        self.create_preset_tree.setSizePolicy(sizePolicy2)
        self.create_preset_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.create_preset_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.create_preset_tree.setDragDropMode(QAbstractItemView.InternalMove)
        self.create_preset_tree.setAlternatingRowColors(False)
        self.create_preset_tree.setRootIsDecorated(False)

        self.create_layout.addWidget(self.create_preset_tree, 2, 0, 1, 2)

        self.progress_box = QGroupBox(self.tab_create_seed)
        self.progress_box.setObjectName(u"progress_box")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progress_box.sizePolicy().hasHeightForWidth())
        self.progress_box.setSizePolicy(sizePolicy3)
        self.progress_box_layout = QGridLayout(self.progress_box)
        self.progress_box_layout.setSpacing(6)
        self.progress_box_layout.setContentsMargins(11, 11, 11, 11)
        self.progress_box_layout.setObjectName(u"progress_box_layout")
        self.progress_box_layout.setContentsMargins(2, 4, 2, 4)
        self.stop_background_process_button = QPushButton(self.progress_box)
        self.stop_background_process_button.setObjectName(u"stop_background_process_button")
        self.stop_background_process_button.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.stop_background_process_button.sizePolicy().hasHeightForWidth())
        self.stop_background_process_button.setSizePolicy(sizePolicy4)
        self.stop_background_process_button.setMaximumSize(QSize(75, 16777215))
        self.stop_background_process_button.setCheckable(False)
        self.stop_background_process_button.setFlat(False)

        self.progress_box_layout.addWidget(self.stop_background_process_button, 0, 3, 1, 1)

        self.progress_bar = QProgressBar(self.progress_box)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMinimumSize(QSize(150, 0))
        self.progress_bar.setMaximumSize(QSize(150, 16777215))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setInvertedAppearance(False)

        self.progress_box_layout.addWidget(self.progress_bar, 0, 0, 1, 2)

        self.progress_label = QLabel(self.progress_box)
        self.progress_label.setObjectName(u"progress_label")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.progress_label.sizePolicy().hasHeightForWidth())
        self.progress_label.setSizePolicy(sizePolicy5)
        font1 = QFont()
        font1.setPointSize(7)
        self.progress_label.setFont(font1)
        self.progress_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progress_label.setWordWrap(True)

        self.progress_box_layout.addWidget(self.progress_label, 0, 2, 1, 1)


        self.create_layout.addWidget(self.progress_box, 5, 0, 1, 4)

        self.create_scroll_area = QScrollArea(self.tab_create_seed)
        self.create_scroll_area.setObjectName(u"create_scroll_area")
        self.create_scroll_area.setWidgetResizable(True)
        self.create_scroll_area_contents = QWidget()
        self.create_scroll_area_contents.setObjectName(u"create_scroll_area_contents")
        self.create_scroll_area_contents.setGeometry(QRect(0, 0, 302, 442))
        self.create_scroll_area_layout = QVBoxLayout(self.create_scroll_area_contents)
        self.create_scroll_area_layout.setSpacing(6)
        self.create_scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.create_scroll_area_layout.setObjectName(u"create_scroll_area_layout")
        self.create_scroll_area_layout.setContentsMargins(4, 4, 4, 4)
        self.create_preset_description = QLabel(self.create_scroll_area_contents)
        self.create_preset_description.setObjectName(u"create_preset_description")
        sizePolicy6 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.create_preset_description.sizePolicy().hasHeightForWidth())
        self.create_preset_description.setSizePolicy(sizePolicy6)
        self.create_preset_description.setMinimumSize(QSize(0, 40))
        self.create_preset_description.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.create_preset_description.setWordWrap(True)

        self.create_scroll_area_layout.addWidget(self.create_preset_description)

        self.create_scroll_area.setWidget(self.create_scroll_area_contents)

        self.create_layout.addWidget(self.create_scroll_area, 2, 2, 1, 2)

        self.main_tab_widget.addTab(self.tab_create_seed, "")
        self.help_tab = RandovaniaHelpWidget()
        self.help_tab.setObjectName(u"help_tab")
        self.main_tab_widget.addTab(self.help_tab, "")
        self.games_tab = GamesHelpWidget()
        self.games_tab.setObjectName(u"games_tab")
        self.main_tab_widget.addTab(self.games_tab, "")
        self.about_tab = QWidget()
        self.about_tab.setObjectName(u"about_tab")
        self.about_layout = QGridLayout(self.about_tab)
        self.about_layout.setSpacing(6)
        self.about_layout.setContentsMargins(11, 11, 11, 11)
        self.about_layout.setObjectName(u"about_layout")
        self.about_layout.setContentsMargins(0, 0, 0, 0)
        self.about_text_browser = QTextBrowser(self.about_tab)
        self.about_text_browser.setObjectName(u"about_text_browser")
        self.about_text_browser.setFrameShape(QFrame.NoFrame)
        self.about_text_browser.setOpenExternalLinks(True)

        self.about_layout.addWidget(self.about_text_browser, 0, 0, 1, 1)

        self.main_tab_widget.addTab(self.about_tab, "")

        self.verticalLayout_4.addWidget(self.main_tab_widget)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 645, 22))
        self.menu_open = QMenu(self.menu_bar)
        self.menu_open.setObjectName(u"menu_open")
        self.menu_edit = QMenu(self.menu_bar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_database = QMenu(self.menu_edit)
        self.menu_database.setObjectName(u"menu_database")
        self.menu_internal = QMenu(self.menu_database)
        self.menu_internal.setObjectName(u"menu_internal")
        self.menu_advanced = QMenu(self.menu_bar)
        self.menu_advanced.setObjectName(u"menu_advanced")
        MainWindow.setMenuBar(self.menu_bar)

        self.menu_bar.addAction(self.menu_open.menuAction())
        self.menu_bar.addAction(self.menu_edit.menuAction())
        self.menu_bar.addAction(self.menu_advanced.menuAction())
        self.menu_open.addAction(self.menu_action_previously_generated_games)
        self.menu_open.addAction(self.menu_action_log_files_directory)
        self.menu_open.addSeparator()
        self.menu_open.addAction(self.menu_action_open_auto_tracker)
        self.menu_open.addSeparator()
        self.menu_open.addSeparator()
        self.menu_edit.addAction(self.menu_database.menuAction())
        self.menu_database.addAction(self.menu_internal.menuAction())
        self.menu_database.addAction(self.menu_action_edit_existing_database)
        self.menu_advanced.addAction(self.menu_action_validate_seed_after)
        self.menu_advanced.addAction(self.menu_action_timeout_generation_after_a_time_limit)
        self.menu_advanced.addAction(self.menu_action_dark_mode)
        self.menu_advanced.addAction(self.menu_action_experimental_games)
        self.menu_advanced.addSeparator()
        self.menu_advanced.addAction(self.action_login_window)
        self.menu_advanced.addSeparator()
        self.menu_advanced.addAction(self.menu_action_layout_editor)

        self.retranslateUi(MainWindow)

        self.main_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Randovania", None))
        self.menu_action_edit_existing_database.setText(QCoreApplication.translate("MainWindow", u"External file", None))
        self.menu_action_validate_seed_after.setText(QCoreApplication.translate("MainWindow", u"Validate if seed is possible after generation", None))
        self.menu_action_timeout_generation_after_a_time_limit.setText(QCoreApplication.translate("MainWindow", u"Timeout generation after a time limit", None))
        self.menu_action_open_auto_tracker.setText(QCoreApplication.translate("MainWindow", u"Automatic Item Tracker", None))
        self.action_login_window.setText(QCoreApplication.translate("MainWindow", u"Login window", None))
        self.menu_action_dark_mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.menu_action_previously_generated_games.setText(QCoreApplication.translate("MainWindow", u"Previously generated games", None))
        self.menu_action_layout_editor.setText(QCoreApplication.translate("MainWindow", u"Corruption Layout Editor", None))
        self.menu_action_log_files_directory.setText(QCoreApplication.translate("MainWindow", u"Log files folder", None))
        self.menu_action_experimental_games.setText(QCoreApplication.translate("MainWindow", u"Experimental games", None))
#if QT_CONFIG(tooltip)
        self.menu_action_experimental_games.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>These games aren't fully integrated into Randovania and might have any number of issues.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.open_faq_button.setText(QCoreApplication.translate("MainWindow", u"Open Game Help", None))
        self.intro_play_now_button.setText(QCoreApplication.translate("MainWindow", u"Play Now", None))
        self.intro_label.setText(QCoreApplication.translate("MainWindow", u"Welcome to Randovania {version}, a randomizer for a multitude of games.", None))
        self.help_offer_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><hr/><p>Want to learn more about the randomizer?</p><p>Check out the <span style=\" font-weight:600;\">Games </span>for more details for each supported.<br/>Check the Database to check what's required to progress in each room.</p></body></html>", None))
        self.open_database_viewer_button.setText(QCoreApplication.translate("MainWindow", u"Open Database Viewer", None))
        self.games_supported_label.setText(QCoreApplication.translate("MainWindow", u"Supported", None))
        self.games_experimental_label.setText(QCoreApplication.translate("MainWindow", u"Experimental", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.welcome_tab), QCoreApplication.translate("MainWindow", u"Welcome", None))
        self.play_existing_permalink_group.setTitle(QCoreApplication.translate("MainWindow", u"Existing games", None))
        self.import_permalink_button.setText(QCoreApplication.translate("MainWindow", u"Import permalink", None))
        self.browse_sessions_button.setText(QCoreApplication.translate("MainWindow", u"Browse for a multiworld session", None))
        self.import_permalink_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Are you playing with others?</p><p>Ask them for a permalink and import it here. You'll create the same game as them.</p></body></html>", None))
        self.import_game_file_label.setText(QCoreApplication.translate("MainWindow", u"If they've shared a spoiler file instead, you can import it directly. This skips the generation step.", None))
        self.browse_racetime_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Are you joining a race hosted in <a href=\"https://racetime.gg/\"><span style=\" text-decoration: underline; color:#0000ff;\">racetime.gg</span></a>?</p><p>Select the race from Randovania and automatically import the permalink!</p></body></html>", None))
        self.import_game_file_button.setText(QCoreApplication.translate("MainWindow", u"Import game file", None))
        self.browse_racetime_button.setText(QCoreApplication.translate("MainWindow", u"Browse races in racetime.gg", None))
        self.browse_sessions_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Joining a multiworld that someone else created? Browse all existing sessions here!</p></body></html>", None))
        self.play_new_game_group.setTitle(QCoreApplication.translate("MainWindow", u"Creating a new game", None))
        self.host_new_game_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Want to play multiworld?</p><p>Host a new online session and invite people!</p></body></html>", None))
        self.create_new_seed_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Playing alone? Hosting a race?</p><p>Create a new game here and then share the permalink!</p></body></html>", None))
        self.create_new_seed_button.setText(QCoreApplication.translate("MainWindow", u"Create new game", None))
        self.host_new_game_button.setText(QCoreApplication.translate("MainWindow", u"Host new multiworld session", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_play), QCoreApplication.translate("MainWindow", u"Play", None))
        self.create_generate_no_retry_button.setText(QCoreApplication.translate("MainWindow", u"Generate without retry", None))
        self.create_generate_race_button.setText(QCoreApplication.translate("MainWindow", u"Generate for Race", None))
        self.create_generate_button.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.num_players_spin_box.setSuffix(QCoreApplication.translate("MainWindow", u" players", None))
        ___qtreewidgetitem = self.create_preset_tree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Presets (Right click for actions)", None));

        __sortingEnabled = self.create_preset_tree.isSortingEnabled()
        self.create_preset_tree.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.create_preset_tree.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Metroid Prime", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Default Preset", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Your Custom Preset", None));
        ___qtreewidgetitem4 = self.create_preset_tree.topLevelItem(1)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"Metroid Prime 2", None));
        self.create_preset_tree.setSortingEnabled(__sortingEnabled)

        self.progress_box.setTitle(QCoreApplication.translate("MainWindow", u"Progress", None))
        self.stop_background_process_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.progress_label.setText("")
        self.create_preset_description.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>This content should have been replaced by code.</p></body></html>", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.tab_create_seed), QCoreApplication.translate("MainWindow", u"Generate Game", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.help_tab), QCoreApplication.translate("MainWindow", u"Randovania Help", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.games_tab), QCoreApplication.translate("MainWindow", u"Games", None))
        self.main_tab_widget.setTabText(self.main_tab_widget.indexOf(self.about_tab), QCoreApplication.translate("MainWindow", u"About", None))
        self.menu_open.setTitle(QCoreApplication.translate("MainWindow", u"Open", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menu_database.setTitle(QCoreApplication.translate("MainWindow", u"Database", None))
        self.menu_internal.setTitle(QCoreApplication.translate("MainWindow", u"Internal", None))
        self.menu_advanced.setTitle(QCoreApplication.translate("MainWindow", u"Advanced", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_prime_patches.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetPrimePatches(object):
    def setupUi(self, PresetPrimePatches):
        if not PresetPrimePatches.objectName():
            PresetPrimePatches.setObjectName(u"PresetPrimePatches")
        PresetPrimePatches.resize(503, 687)
        self.centralWidget = QWidget(PresetPrimePatches)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(self.centralWidget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.scroll_contents.setObjectName(u"scroll_contents")
        self.scroll_contents.setGeometry(QRect(0, 0, 515, 1590))
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.scroll_layout.setObjectName(u"scroll_layout")
        self.scroll_layout.setContentsMargins(0, 2, 0, 0)
        self.top_spacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.scroll_layout.addItem(self.top_spacer)

        self.warp_to_start_group = QGroupBox(self.scroll_contents)
        self.warp_to_start_group.setObjectName(u"warp_to_start_group")
        self.verticalLayout_6 = QVBoxLayout(self.warp_to_start_group)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.warp_to_start_check = QCheckBox(self.warp_to_start_group)
        self.warp_to_start_check.setObjectName(u"warp_to_start_check")

        self.verticalLayout_6.addWidget(self.warp_to_start_check)

        self.warp_to_start_label = QLabel(self.warp_to_start_group)
        self.warp_to_start_label.setObjectName(u"warp_to_start_label")
        self.warp_to_start_label.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.warp_to_start_label)


        self.scroll_layout.addWidget(self.warp_to_start_group)

        self.qol_group = QGroupBox(self.scroll_contents)
        self.qol_group.setObjectName(u"qol_group")
        self.verticalLayout_2 = QVBoxLayout(self.qol_group)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.description_label = QLabel(self.qol_group)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)
        self.description_label.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.description_label)

        self.qol_game_breaking_check = QCheckBox(self.qol_group)
        self.qol_game_breaking_check.setObjectName(u"qol_game_breaking_check")
        self.qol_game_breaking_check.setEnabled(True)

        self.verticalLayout_2.addWidget(self.qol_game_breaking_check)

        self.qol_game_breaking_label = QLabel(self.qol_group)
        self.qol_game_breaking_label.setObjectName(u"qol_game_breaking_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qol_game_breaking_label.sizePolicy().hasHeightForWidth())
        self.qol_game_breaking_label.setSizePolicy(sizePolicy)
        self.qol_game_breaking_label.setMaximumSize(QSize(16777215, 90))
        self.qol_game_breaking_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.qol_game_breaking_label.setWordWrap(True)
        self.qol_game_breaking_label.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.qol_game_breaking_label)

        self.groupBox = QGroupBox(self.qol_group)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.main_plaza_door_check = QCheckBox(self.groupBox)
        self.main_plaza_door_check.setObjectName(u"main_plaza_door_check")

        self.verticalLayout_3.addWidget(self.main_plaza_door_check)

        self.main_plaza_door_label = QLabel(self.groupBox)
        self.main_plaza_door_label.setObjectName(u"main_plaza_door_label")

        self.verticalLayout_3.addWidget(self.main_plaza_door_label)

        self.backwards_frigate_check = QCheckBox(self.groupBox)
        self.backwards_frigate_check.setObjectName(u"backwards_frigate_check")

        self.verticalLayout_3.addWidget(self.backwards_frigate_check)

        self.backwards_frigate_label = QLabel(self.groupBox)
        self.backwards_frigate_label.setObjectName(u"backwards_frigate_label")

        self.verticalLayout_3.addWidget(self.backwards_frigate_label)

        self.backwards_labs_check = QCheckBox(self.groupBox)
        self.backwards_labs_check.setObjectName(u"backwards_labs_check")

        self.verticalLayout_3.addWidget(self.backwards_labs_check)

        self.backwards_labs_label = QLabel(self.groupBox)
        self.backwards_labs_label.setObjectName(u"backwards_labs_label")

        self.verticalLayout_3.addWidget(self.backwards_labs_label)

        self.backwards_upper_mines_check = QCheckBox(self.groupBox)
        self.backwards_upper_mines_check.setObjectName(u"backwards_upper_mines_check")

        self.verticalLayout_3.addWidget(self.backwards_upper_mines_check)

        self.backwards_upper_mines_label = QLabel(self.groupBox)
        self.backwards_upper_mines_label.setObjectName(u"backwards_upper_mines_label")

        self.verticalLayout_3.addWidget(self.backwards_upper_mines_label)

        self.backwards_lower_mines_check = QCheckBox(self.groupBox)
        self.backwards_lower_mines_check.setObjectName(u"backwards_lower_mines_check")

        self.verticalLayout_3.addWidget(self.backwards_lower_mines_check)

        self.backwards_lower_mines_label = QLabel(self.groupBox)
        self.backwards_lower_mines_label.setObjectName(u"backwards_lower_mines_label")

        self.verticalLayout_3.addWidget(self.backwards_lower_mines_label)

        self.phazon_elite_without_dynamo_check = QCheckBox(self.groupBox)
        self.phazon_elite_without_dynamo_check.setObjectName(u"phazon_elite_without_dynamo_check")

        self.verticalLayout_3.addWidget(self.phazon_elite_without_dynamo_check)

        self.phazon_elite_without_dynamo_label = QLabel(self.groupBox)
        self.phazon_elite_without_dynamo_label.setObjectName(u"phazon_elite_without_dynamo_label")

        self.verticalLayout_3.addWidget(self.phazon_elite_without_dynamo_label)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.qol_cosmetic_check = QCheckBox(self.qol_group)
        self.qol_cosmetic_check.setObjectName(u"qol_cosmetic_check")
        self.qol_cosmetic_check.setEnabled(False)
        self.qol_cosmetic_check.setChecked(True)

        self.verticalLayout_2.addWidget(self.qol_cosmetic_check)

        self.qol_cosmetic_label = QLabel(self.qol_group)
        self.qol_cosmetic_label.setObjectName(u"qol_cosmetic_label")
        self.qol_cosmetic_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.qol_cosmetic_label)

        self.qol_pickup_scans_check = QCheckBox(self.qol_group)
        self.qol_pickup_scans_check.setObjectName(u"qol_pickup_scans_check")

        self.verticalLayout_2.addWidget(self.qol_pickup_scans_check)

        self.qol_pickup_scans_label = QLabel(self.qol_group)
        self.qol_pickup_scans_label.setObjectName(u"qol_pickup_scans_label")
        self.qol_pickup_scans_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.qol_pickup_scans_label)


        self.scroll_layout.addWidget(self.qol_group)

        self.cutscene_group = QGroupBox(self.scroll_contents)
        self.cutscene_group.setObjectName(u"cutscene_group")
        self.verticalLayout_5 = QVBoxLayout(self.cutscene_group)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.cutscene_combo = QComboBox(self.cutscene_group)
        self.cutscene_combo.addItem("")
        self.cutscene_combo.addItem("")
        self.cutscene_combo.addItem("")
        self.cutscene_combo.addItem("")
        self.cutscene_combo.setObjectName(u"cutscene_combo")

        self.verticalLayout_5.addWidget(self.cutscene_combo)

        self.cutscene_label = QLabel(self.cutscene_group)
        self.cutscene_label.setObjectName(u"cutscene_label")
        self.cutscene_label.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.cutscene_label)


        self.scroll_layout.addWidget(self.cutscene_group)

        self.spring_ball_group = QGroupBox(self.scroll_contents)
        self.spring_ball_group.setObjectName(u"spring_ball_group")
        self.verticalLayout_9 = QVBoxLayout(self.spring_ball_group)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(9, 9, 9, 9)
        self.spring_ball_check = QCheckBox(self.spring_ball_group)
        self.spring_ball_check.setObjectName(u"spring_ball_check")

        self.verticalLayout_9.addWidget(self.spring_ball_check)

        self.spring_ball_label = QLabel(self.spring_ball_group)
        self.spring_ball_label.setObjectName(u"spring_ball_label")

        self.verticalLayout_9.addWidget(self.spring_ball_label)


        self.scroll_layout.addWidget(self.spring_ball_group)

        self.deterministic_idrone_group = QGroupBox(self.scroll_contents)
        self.deterministic_idrone_group.setObjectName(u"deterministic_idrone_group")
        self.verticalLayout_91 = QVBoxLayout(self.deterministic_idrone_group)
        self.verticalLayout_91.setSpacing(6)
        self.verticalLayout_91.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_91.setObjectName(u"verticalLayout_91")
        self.verticalLayout_91.setContentsMargins(9, 9, 9, 9)
        self.deterministic_idrone_check = QCheckBox(self.deterministic_idrone_group)
        self.deterministic_idrone_check.setObjectName(u"deterministic_idrone_check")

        self.verticalLayout_91.addWidget(self.deterministic_idrone_check)

        self.deterministic_idrone_label = QLabel(self.deterministic_idrone_group)
        self.deterministic_idrone_label.setObjectName(u"deterministic_idrone_label")
        self.deterministic_idrone_label.setWordWrap(True)

        self.verticalLayout_91.addWidget(self.deterministic_idrone_label)


        self.scroll_layout.addWidget(self.deterministic_idrone_group)

        self.maze_group = QGroupBox(self.scroll_contents)
        self.maze_group.setObjectName(u"maze_group")
        self.verticalLayout_92 = QVBoxLayout(self.maze_group)
        self.verticalLayout_92.setSpacing(6)
        self.verticalLayout_92.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_92.setObjectName(u"verticalLayout_92")
        self.verticalLayout_92.setContentsMargins(9, 9, 9, 9)
        self.deterministic_maze_check = QCheckBox(self.maze_group)
        self.deterministic_maze_check.setObjectName(u"deterministic_maze_check")

        self.verticalLayout_92.addWidget(self.deterministic_maze_check)

        self.deterministic_maze_label = QLabel(self.maze_group)
        self.deterministic_maze_label.setObjectName(u"deterministic_maze_label")
        self.deterministic_maze_label.setWordWrap(True)

        self.verticalLayout_92.addWidget(self.deterministic_maze_label)


        self.scroll_layout.addWidget(self.maze_group)

        self.shuffle_item_pos_group = QGroupBox(self.scroll_contents)
        self.shuffle_item_pos_group.setObjectName(u"shuffle_item_pos_group")
        self.verticalLayout_4 = QVBoxLayout(self.shuffle_item_pos_group)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.chaos_label = QLabel(self.shuffle_item_pos_group)
        self.chaos_label.setObjectName(u"chaos_label")
        self.chaos_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.chaos_label)

        self.small_samus_check = QCheckBox(self.shuffle_item_pos_group)
        self.small_samus_check.setObjectName(u"small_samus_check")

        self.verticalLayout_4.addWidget(self.small_samus_check)

        self.small_samus_label = QLabel(self.shuffle_item_pos_group)
        self.small_samus_label.setObjectName(u"small_samus_label")
        self.small_samus_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.small_samus_label)

        self.large_samus_check = QCheckBox(self.shuffle_item_pos_group)
        self.large_samus_check.setObjectName(u"large_samus_check")

        self.verticalLayout_4.addWidget(self.large_samus_check)

        self.large_samus_label = QLabel(self.shuffle_item_pos_group)
        self.large_samus_label.setObjectName(u"large_samus_label")
        self.large_samus_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.large_samus_label)

        self.shuffle_item_pos_check = QCheckBox(self.shuffle_item_pos_group)
        self.shuffle_item_pos_check.setObjectName(u"shuffle_item_pos_check")

        self.verticalLayout_4.addWidget(self.shuffle_item_pos_check)

        self.shuffle_item_pos_label = QLabel(self.shuffle_item_pos_group)
        self.shuffle_item_pos_label.setObjectName(u"shuffle_item_pos_label")
        self.shuffle_item_pos_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.shuffle_item_pos_label)

        self.items_every_room_check = QCheckBox(self.shuffle_item_pos_group)
        self.items_every_room_check.setObjectName(u"items_every_room_check")

        self.verticalLayout_4.addWidget(self.items_every_room_check)

        self.items_every_room_label = QLabel(self.shuffle_item_pos_group)
        self.items_every_room_label.setObjectName(u"items_every_room_label")
        self.items_every_room_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.items_every_room_label)

        self.random_boss_sizes_check = QCheckBox(self.shuffle_item_pos_group)
        self.random_boss_sizes_check.setObjectName(u"random_boss_sizes_check")

        self.verticalLayout_4.addWidget(self.random_boss_sizes_check)

        self.random_boss_sizes_label = QLabel(self.shuffle_item_pos_group)
        self.random_boss_sizes_label.setObjectName(u"random_boss_sizes_label")
        self.random_boss_sizes_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.random_boss_sizes_label)

        self.no_doors_check = QCheckBox(self.shuffle_item_pos_group)
        self.no_doors_check.setObjectName(u"no_doors_check")

        self.verticalLayout_4.addWidget(self.no_doors_check)

        self.no_doors_label = QLabel(self.shuffle_item_pos_group)
        self.no_doors_label.setObjectName(u"no_doors_label")
        self.no_doors_label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.no_doors_label)

        self.label = QLabel(self.shuffle_item_pos_group)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label)

        self.superheated_slider_layout = QHBoxLayout()
        self.superheated_slider_layout.setSpacing(6)
        self.superheated_slider_layout.setObjectName(u"superheated_slider_layout")
        self.superheated_slider = QSlider(self.shuffle_item_pos_group)
        self.superheated_slider.setObjectName(u"superheated_slider")
        self.superheated_slider.setMaximum(1000)
        self.superheated_slider.setPageStep(2)
        self.superheated_slider.setOrientation(Qt.Horizontal)
        self.superheated_slider.setTickPosition(QSlider.TicksBelow)

        self.superheated_slider_layout.addWidget(self.superheated_slider)

        self.superheated_slider_label = QLabel(self.shuffle_item_pos_group)
        self.superheated_slider_label.setObjectName(u"superheated_slider_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.superheated_slider_label.sizePolicy().hasHeightForWidth())
        self.superheated_slider_label.setSizePolicy(sizePolicy1)
        self.superheated_slider_label.setMinimumSize(QSize(20, 0))
        self.superheated_slider_label.setAlignment(Qt.AlignCenter)

        self.superheated_slider_layout.addWidget(self.superheated_slider_label)


        self.verticalLayout_4.addLayout(self.superheated_slider_layout)

        self.label1 = QLabel(self.shuffle_item_pos_group)
        self.label1.setObjectName(u"label1")
        self.label1.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label1)

        self.submerged_slider_layout = QHBoxLayout()
        self.submerged_slider_layout.setSpacing(6)
        self.submerged_slider_layout.setObjectName(u"submerged_slider_layout")
        self.submerged_slider = QSlider(self.shuffle_item_pos_group)
        self.submerged_slider.setObjectName(u"submerged_slider")
        self.submerged_slider.setMaximum(1000)
        self.submerged_slider.setPageStep(2)
        self.submerged_slider.setOrientation(Qt.Horizontal)
        self.submerged_slider.setTickPosition(QSlider.TicksBelow)

        self.submerged_slider_layout.addWidget(self.submerged_slider)

        self.submerged_slider_label = QLabel(self.shuffle_item_pos_group)
        self.submerged_slider_label.setObjectName(u"submerged_slider_label")
        sizePolicy1.setHeightForWidth(self.submerged_slider_label.sizePolicy().hasHeightForWidth())
        self.submerged_slider_label.setSizePolicy(sizePolicy1)
        self.submerged_slider_label.setMinimumSize(QSize(20, 0))
        self.submerged_slider_label.setAlignment(Qt.AlignCenter)

        self.submerged_slider_layout.addWidget(self.submerged_slider_label)


        self.verticalLayout_4.addLayout(self.submerged_slider_layout)

        self.room_rando_group = QGroupBox(self.shuffle_item_pos_group)
        self.room_rando_group.setObjectName(u"room_rando_group")
        self.verticalLayout_51 = QVBoxLayout(self.room_rando_group)
        self.verticalLayout_51.setSpacing(6)
        self.verticalLayout_51.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.room_rando_combo = QComboBox(self.room_rando_group)
        self.room_rando_combo.addItem("")
        self.room_rando_combo.addItem("")
        self.room_rando_combo.addItem("")
        self.room_rando_combo.setObjectName(u"room_rando_combo")

        self.verticalLayout_51.addWidget(self.room_rando_combo)

        self.room_rando_label = QLabel(self.room_rando_group)
        self.room_rando_label.setObjectName(u"room_rando_label")
        self.room_rando_label.setWordWrap(True)

        self.verticalLayout_51.addWidget(self.room_rando_label)


        self.verticalLayout_4.addWidget(self.room_rando_group)


        self.scroll_layout.addWidget(self.shuffle_item_pos_group)

        self.scroll_area.setWidget(self.scroll_contents)

        self.verticalLayout.addWidget(self.scroll_area)

        PresetPrimePatches.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetPrimePatches)

        QMetaObject.connectSlotsByName(PresetPrimePatches)
    # setupUi

    def retranslateUi(self, PresetPrimePatches):
        PresetPrimePatches.setWindowTitle(QCoreApplication.translate("PresetPrimePatches", u"Other", None))
        self.warp_to_start_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Warp to Start", None))
        self.warp_to_start_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Add warping to starting location from save stations", None))
        self.warp_to_start_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Refusing to save at any Save Station while holding L+R will warp you to the starting location (by default, Samus' ship in Landing Site).</p></body></html>", None))
        self.qol_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Quality of life", None))
        self.description_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>This section offers various impovements over the base game to better suit it for randomization and frequent playing.</p><p>For an in-depth list of changes, see <a href=\"https://github.com/toasterparty/randomprime/blob/randovania/doc/quality_of_life.md\"><span style=\" text-decoration: underline; color:#0000ff;\">Quality of Life Documentation</span></a>.<br/></p></body></html>", None))
        self.qol_game_breaking_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Game Breaking", None))
        self.qol_game_breaking_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Fixes crashes, soft-locks and other critical game functions that can ruin the randomizer experience. Reverts unwanted fixes made by Retro in versions after NTSC 0-00. Logic always assume this is enabled.<br/><br/>If unsure leave this box checked!</p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Logical changes", None))
        self.main_plaza_door_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Main Plaza Vault Door", None))
        self.main_plaza_door_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Allow access to Vault from Main Plaza", None))
        self.backwards_frigate_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Backwards Frigate", None))
        self.backwards_frigate_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Power door in Main Ventilation Shaft Section B when approached from behind", None))
        self.backwards_labs_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Backwards Labs", None))
        self.backwards_labs_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Scan through barrier of Research Lab Hydra when approached from deep labs", None))
        self.backwards_upper_mines_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Backwards Upper Mines", None))
        self.backwards_upper_mines_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Disable Main Quarry barrier automatically when approached from Mine Security Station", None))
        self.backwards_lower_mines_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Backwards Lower Mines", None))
        self.backwards_lower_mines_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Remove PCA locks and allow passing through lower mines scan barriers from the back", None))
        self.phazon_elite_without_dynamo_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Phazon Elite without Dynamo", None))
        self.phazon_elite_without_dynamo_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Removes the Central Dynamo item requirement for activating the Phazon Elite boss fight", None))
        self.qol_cosmetic_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Cosmetic", None))
        self.qol_cosmetic_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Remove or change things that only affect real time, not in-game time.<br/>This group is controlled by an user preference and changing it does not affect the permalink.</p></body></html>", None))
        self.qol_pickup_scans_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Pickup Scans", None))
        self.qol_pickup_scans_label.setText(QCoreApplication.translate("PresetPrimePatches", u"Enable this option to patch various item locations so that they can be scanned. Only locations whose model is visible in combat visor are affected. Note that the new scan may be near the item, not necessarily on top of it.", None))
        self.cutscene_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Cutscene removal mode", None))
        self.cutscene_combo.setItemText(0, QCoreApplication.translate("PresetPrimePatches", u"Original", None))
        self.cutscene_combo.setItemText(1, QCoreApplication.translate("PresetPrimePatches", u"Competitive", None))
        self.cutscene_combo.setItemText(2, QCoreApplication.translate("PresetPrimePatches", u"Minor", None))
        self.cutscene_combo.setItemText(3, QCoreApplication.translate("PresetPrimePatches", u"Major", None))

        self.cutscene_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p><span style=\" font-weight:600;\">Original</span>: No changes to the cutscenes are made.</p><p><span style=\" font-weight:600;\">Competitive</span>: Similar to minor, but leaves a few rooms alone where skipping cutscenes would be inappropriate for races.</p><p><span style=\" font-weight:600;\">Minor</span>: Removes cutscenes that don't affect the game too much when removed.</p><p><span style=\" font-weight:600;\">Major</span>: Allows you to continue playing the game while cutscenes happen.</p></body></html>", None))
        self.spring_ball_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Spring Ball", None))
        self.spring_ball_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Enable Spring Ball", None))
        self.spring_ball_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Restores the Spring Ball feature from Metroid Prime Trilogy.<br/>Use C-Stick Up while being morphed to use Spring Ball.<br/><br/><span style=\" font-weight:600;\">Warning:</span> You need Morph Ball Bombs to use Spring Ball just like in Metroid Prime Trilogy.</p></body></html>", None))
        self.deterministic_idrone_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Incinerator Drone", None))
        self.deterministic_idrone_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Deterministic Incinerator Drone RNG", None))
        self.deterministic_idrone_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Check this box to randomly generate the Incinerator Drone's RNG values when generating the seed, as opposed to in-game. Makes races more fair.</p></body></html>", None))
        self.maze_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Central Dynamo Maze", None))
        self.deterministic_maze_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Deterministic Maze RNG", None))
        self.deterministic_maze_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Check this box to randomly select a maze when generating the seed, as opposed to in-game. Makes races more fair.</p></body></html>", None))
        self.shuffle_item_pos_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Chaos Options", None))
        self.chaos_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Chaos options are patcher-side only, and thus are not accounted for by the seed generator logic (many seeds will be incompletable). PROCEDE WITH CAUTION.</p><p><span style=\" font-weight:600;\"></span></p></body></html>", None))
        self.small_samus_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Enable Small Samus", None))
        self.small_samus_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>In this mode, Samus is scaled to 30% of her normal size. Expect to be able to fit in many places you weren't before, but also fall down in a lot of holes you didn't before.</p><p><span style=\" font-weight:600;\">Warning:</span> This option has been known to induce motion sickness and nausea in some players. If you are concerned you may suffer from these symptoms, it may be best to avoid playing with this setting enabled.</p></body></html>", None))
        self.large_samus_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Enable Large Samus", None))
        self.large_samus_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>In this mode, Samus is scaled to 175% of her normal size. This adds an extra challenge to otherwise trivial movements throughout rooms. You will not get far if you do not get morph and bombs in your starting room. As such, logic does not respect this game modification.</p></body></html>", None))
        self.shuffle_item_pos_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Shuffle Item Position", None))
        self.shuffle_item_pos_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Item locations are randomized within the rooms they reside in. There is no checking to ensure items are placed inbounds so seeds are not garunteed to be logical or even completable. Item scan points are adjusted in this mode to be larger and can be seen through walls.</p></body></html>", None))
        self.items_every_room_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Items in Every Room", None))
        self.items_every_room_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Like above, but adds 1 additional item spawn locations in each room which normally do not contain an item. Be sure to visit the item pool tab to fill the pool with items to use in the newly added location. Extra item locations are never required to complete the game.</p></body></html>", None))
        self.random_boss_sizes_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Random Boss Sizes", None))
        self.random_boss_sizes_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Makes each of the bosses (and mini-bosses) a random size ranging from \"tiny bug\" to \"barely fits in the room\".</p></body></html>", None))
        self.no_doors_check.setText(QCoreApplication.translate("PresetPrimePatches", u"Remove Doors", None))
        self.no_doors_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p>Completely removes the need to shoot doors to procede through the game. This also means that there is nothing stopping you from entering a room before it has loaded. As such, it is reccomended to play with Dolphin's \"Speed up Disc Transfer Rate\" option in the right-click properties menu.</p></body></html>", None))
        self.label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p><br/>Superheated Probability: Probability that any room is superheated. If non-zero, rooms which are normally superheated will have their superheated state re-rolled. Completely ignores heat-run logic.</p></body></html>", None))
        self.superheated_slider_label.setText(QCoreApplication.translate("PresetPrimePatches", u"0", None))
        self.label1.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body><p><br/>Submerged Probability: Probability that any room is fully submerged in water. Completely ignores underwater movement logic.</p></body></html>", None))
        self.submerged_slider_label.setText(QCoreApplication.translate("PresetPrimePatches", u"0", None))
        self.room_rando_group.setTitle(QCoreApplication.translate("PresetPrimePatches", u"Room Rando", None))
        self.room_rando_combo.setItemText(0, QCoreApplication.translate("PresetPrimePatches", u"None", None))
        self.room_rando_combo.setItemText(1, QCoreApplication.translate("PresetPrimePatches", u"One-way", None))
        self.room_rando_combo.setItemText(2, QCoreApplication.translate("PresetPrimePatches", u"Two-way", None))

        self.room_rando_label.setText(QCoreApplication.translate("PresetPrimePatches", u"<html><head/><body>These options shuffle how rooms within an area are connected completely smashing randovania's delicately balanced logic.<p><span style=\" font-weight:600;\">None</span>: No changes are made.</p><p><span style=\" font-weight:600;\">One-way</span>: Doors are patched to lead to another random door in the same world. That door most likely does not lead back to the previous room. Scan doors to see where they lead.</p><p><span style=\" font-weight:600;\">Two-way</span>: Like One-way, but doors will always lead back to the previous room.</p></body></html>", None))
    # retranslateUi


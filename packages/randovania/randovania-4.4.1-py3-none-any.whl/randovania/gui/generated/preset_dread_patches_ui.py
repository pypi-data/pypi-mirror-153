# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_dread_patches.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetDreadPatches(object):
    def setupUi(self, PresetDreadPatches):
        if not PresetDreadPatches.objectName():
            PresetDreadPatches.setObjectName(u"PresetDreadPatches")
        PresetDreadPatches.resize(498, 323)
        self.centralWidget = QWidget(PresetDreadPatches)
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
        self.scroll_contents.setGeometry(QRect(0, 0, 486, 335))
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.scroll_layout.setObjectName(u"scroll_layout")
        self.scroll_layout.setContentsMargins(0, 2, 0, 0)
        self.top_spacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.scroll_layout.addItem(self.top_spacer)

        self.unlock_group = QGroupBox(self.scroll_contents)
        self.unlock_group.setObjectName(u"unlock_group")
        self.unlock_layout = QVBoxLayout(self.unlock_group)
        self.unlock_layout.setSpacing(6)
        self.unlock_layout.setContentsMargins(11, 11, 11, 11)
        self.unlock_layout.setObjectName(u"unlock_layout")
        self.hanubia_shortcut_no_grapple_check = QCheckBox(self.unlock_group)
        self.hanubia_shortcut_no_grapple_check.setObjectName(u"hanubia_shortcut_no_grapple_check")

        self.unlock_layout.addWidget(self.hanubia_shortcut_no_grapple_check)

        self.hanubia_shortcut_no_grapple_label = QLabel(self.unlock_group)
        self.hanubia_shortcut_no_grapple_label.setObjectName(u"hanubia_shortcut_no_grapple_label")
        self.hanubia_shortcut_no_grapple_label.setWordWrap(True)

        self.unlock_layout.addWidget(self.hanubia_shortcut_no_grapple_label)

        self.hanubia_easier_path_to_itorash_check = QCheckBox(self.unlock_group)
        self.hanubia_easier_path_to_itorash_check.setObjectName(u"hanubia_easier_path_to_itorash_check")

        self.unlock_layout.addWidget(self.hanubia_easier_path_to_itorash_check)

        self.hanubia_easier_path_to_itorash_label = QLabel(self.unlock_group)
        self.hanubia_easier_path_to_itorash_label.setObjectName(u"hanubia_easier_path_to_itorash_label")

        self.unlock_layout.addWidget(self.hanubia_easier_path_to_itorash_label)


        self.scroll_layout.addWidget(self.unlock_group)

        self.bosses_group = QGroupBox(self.scroll_contents)
        self.bosses_group.setObjectName(u"bosses_group")
        self.bosses_layout = QVBoxLayout(self.bosses_group)
        self.bosses_layout.setSpacing(6)
        self.bosses_layout.setContentsMargins(11, 11, 11, 11)
        self.bosses_layout.setObjectName(u"bosses_layout")
        self.bosses_layout.setContentsMargins(9, 9, 9, 9)
        self.extra_pickups_for_bosses_check = QCheckBox(self.bosses_group)
        self.extra_pickups_for_bosses_check.setObjectName(u"extra_pickups_for_bosses_check")

        self.bosses_layout.addWidget(self.extra_pickups_for_bosses_check)

        self.extra_pickups_for_bosses_label = QLabel(self.bosses_group)
        self.extra_pickups_for_bosses_label.setObjectName(u"extra_pickups_for_bosses_label")
        self.extra_pickups_for_bosses_label.setWordWrap(True)

        self.bosses_layout.addWidget(self.extra_pickups_for_bosses_label)


        self.scroll_layout.addWidget(self.bosses_group)

        self.x_group = QGroupBox(self.scroll_contents)
        self.x_group.setObjectName(u"x_group")
        self.verticalLayout_2 = QVBoxLayout(self.x_group)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.x_starts_released_check = QCheckBox(self.x_group)
        self.x_starts_released_check.setObjectName(u"x_starts_released_check")

        self.verticalLayout_2.addWidget(self.x_starts_released_check)

        self.x_starts_released_label = QLabel(self.x_group)
        self.x_starts_released_label.setObjectName(u"x_starts_released_label")
        self.x_starts_released_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.x_starts_released_label)


        self.scroll_layout.addWidget(self.x_group)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scroll_layout.addItem(self.verticalSpacer)

        self.scroll_area.setWidget(self.scroll_contents)

        self.verticalLayout.addWidget(self.scroll_area)

        PresetDreadPatches.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetDreadPatches)

        QMetaObject.connectSlotsByName(PresetDreadPatches)
    # setupUi

    def retranslateUi(self, PresetDreadPatches):
        PresetDreadPatches.setWindowTitle(QCoreApplication.translate("PresetDreadPatches", u"Other", None))
        self.unlock_group.setTitle(QCoreApplication.translate("PresetDreadPatches", u"Unlocking access", None))
        self.hanubia_shortcut_no_grapple_check.setText(QCoreApplication.translate("PresetDreadPatches", u"Remove Grapple Blocks in Hanubia - Ferenia Shortcut", None))
        self.hanubia_shortcut_no_grapple_label.setText(QCoreApplication.translate("PresetDreadPatches", u"<html><head/><body><p>Hanubia - Ferenia Shortcut, the room next to the elevator to Ferenia in Hanubia, has two Grapple Blocks that prevents access to Hanubia from this elevator.</p></body></html>", None))
        self.hanubia_easier_path_to_itorash_check.setText(QCoreApplication.translate("PresetDreadPatches", u"Remove Grapple and Wave locks in path to Itorash", None))
        self.hanubia_easier_path_to_itorash_label.setText(QCoreApplication.translate("PresetDreadPatches", u"Removes the Grapple Blocks and Wave Beam door locks on the top of Hanubia.", None))
        self.bosses_group.setTitle(QCoreApplication.translate("PresetDreadPatches", u"Bosses", None))
        self.extra_pickups_for_bosses_check.setText(QCoreApplication.translate("PresetDreadPatches", u"Add new pickups to bosses (Partly Implemented)", None))
        self.extra_pickups_for_bosses_label.setText(QCoreApplication.translate("PresetDreadPatches", u"<html><head/><body><p>Defeating the following bosses directly gives you a pickup: Kraid, Drogyga, Experiment Z-57 and the Chozo Soldiers.</p></body></html>", None))
        self.x_group.setTitle(QCoreApplication.translate("PresetDreadPatches", u"X Parasites", None))
        self.x_starts_released_check.setText(QCoreApplication.translate("PresetDreadPatches", u"Start game with the X already released", None))
        self.x_starts_released_label.setText(QCoreApplication.translate("PresetDreadPatches", u"The X variant of enemies are stronger, making the game harder. This allows access to Golzuna without having to visit Elun.", None))
    # retranslateUi


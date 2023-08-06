# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dread_cosmetic_patches_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_DreadCosmeticPatchesDialog(object):
    def setupUi(self, DreadCosmeticPatchesDialog):
        if not DreadCosmeticPatchesDialog.objectName():
            DreadCosmeticPatchesDialog.setObjectName(u"DreadCosmeticPatchesDialog")
        DreadCosmeticPatchesDialog.resize(424, 228)
        self.gridLayout = QGridLayout(DreadCosmeticPatchesDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(DreadCosmeticPatchesDialog)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 2, 2, 1, 1)

        self.accept_button = QPushButton(DreadCosmeticPatchesDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 2, 0, 1, 1)

        self.cancel_button = QPushButton(DreadCosmeticPatchesDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 2, 1, 1, 1)

        self.scrollArea = QScrollArea(DreadCosmeticPatchesDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 404, 178))
        self.verticalLayout = QVBoxLayout(self.scroll_area_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.game_changes_box = QGroupBox(self.scroll_area_contents)
        self.game_changes_box.setObjectName(u"game_changes_box")
        self.game_changes_layout = QVBoxLayout(self.game_changes_box)
        self.game_changes_layout.setSpacing(6)
        self.game_changes_layout.setContentsMargins(11, 11, 11, 11)
        self.game_changes_layout.setObjectName(u"game_changes_layout")
        self.show_boss_life = QCheckBox(self.game_changes_box)
        self.show_boss_life.setObjectName(u"show_boss_life")

        self.game_changes_layout.addWidget(self.show_boss_life)

        self.show_enemy_life = QCheckBox(self.game_changes_box)
        self.show_enemy_life.setObjectName(u"show_enemy_life")

        self.game_changes_layout.addWidget(self.show_enemy_life)

        self.show_enemy_damage = QCheckBox(self.game_changes_box)
        self.show_enemy_damage.setObjectName(u"show_enemy_damage")

        self.game_changes_layout.addWidget(self.show_enemy_damage)

        self.show_player_damage = QCheckBox(self.game_changes_box)
        self.show_player_damage.setObjectName(u"show_player_damage")

        self.game_changes_layout.addWidget(self.show_player_damage)


        self.verticalLayout.addWidget(self.game_changes_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scroll_area_contents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)


        self.retranslateUi(DreadCosmeticPatchesDialog)

        QMetaObject.connectSlotsByName(DreadCosmeticPatchesDialog)
    # setupUi

    def retranslateUi(self, DreadCosmeticPatchesDialog):
        DreadCosmeticPatchesDialog.setWindowTitle(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Metroid Dread - Cosmetic Options", None))
        self.reset_button.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Reset to Defaults", None))
        self.accept_button.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Cancel", None))
        self.game_changes_box.setTitle(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Config Options", None))
        self.show_boss_life.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Show boss life bars", None))
        self.show_enemy_life.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Show enemy life bars", None))
        self.show_enemy_damage.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Show enemy damage", None))
        self.show_player_damage.setText(QCoreApplication.translate("DreadCosmeticPatchesDialog", u"Show player damage", None))
    # retranslateUi


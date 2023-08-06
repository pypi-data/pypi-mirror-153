# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'super_cosmetic_patches_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_SuperCosmeticPatchesDialog(object):
    def setupUi(self, SuperCosmeticPatchesDialog):
        if not SuperCosmeticPatchesDialog.objectName():
            SuperCosmeticPatchesDialog.setObjectName(u"SuperCosmeticPatchesDialog")
        SuperCosmeticPatchesDialog.resize(476, 647)
        self.centralWidget = QWidget(SuperCosmeticPatchesDialog)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setGeometry(QRect(0, 0, 481, 591))
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.main_layout = QVBoxLayout(self.centralWidget)
        self.main_layout.setSpacing(6)
        self.main_layout.setContentsMargins(11, 11, 11, 11)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(self.centralWidget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 477, 587))
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area_contents.sizePolicy().hasHeightForWidth())
        self.scroll_area_contents.setSizePolicy(sizePolicy)
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_contents)
        self.scroll_area_layout.setSpacing(6)
        self.scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.scroll_area_layout.setObjectName(u"scroll_area_layout")
        self.scroll_area_layout.setContentsMargins(1, 1, 1, 0)
        self.accessibility_box = QGroupBox(self.scroll_area_contents)
        self.accessibility_box.setObjectName(u"accessibility_box")
        self.gridLayout_8 = QGridLayout(self.accessibility_box)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.colorblind_checkbox = QCheckBox(self.accessibility_box)
        self.colorblind_checkbox.setObjectName(u"colorblind_checkbox")

        self.gridLayout_8.addWidget(self.colorblind_checkbox, 1, 0, 1, 1)

        self.colorblind_label = QLabel(self.accessibility_box)
        self.colorblind_label.setObjectName(u"colorblind_label")
        self.colorblind_label.setWordWrap(True)

        self.gridLayout_8.addWidget(self.colorblind_label, 2, 0, 1, 1)


        self.scroll_area_layout.addWidget(self.accessibility_box)

        self.qol_box = QGroupBox(self.scroll_area_contents)
        self.qol_box.setObjectName(u"qol_box")
        self.gridLayout_4 = QGridLayout(self.qol_box)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.no_demo_checkbox = QCheckBox(self.qol_box)
        self.no_demo_checkbox.setObjectName(u"no_demo_checkbox")
        self.no_demo_checkbox.setChecked(True)

        self.gridLayout_4.addWidget(self.no_demo_checkbox, 12, 0, 1, 1)

        self.max_ammo_display_label = QLabel(self.qol_box)
        self.max_ammo_display_label.setObjectName(u"max_ammo_display_label")

        self.gridLayout_4.addWidget(self.max_ammo_display_label, 4, 0, 1, 1)

        self.no_demo_label = QLabel(self.qol_box)
        self.no_demo_label.setObjectName(u"no_demo_label")

        self.gridLayout_4.addWidget(self.no_demo_label, 13, 0, 1, 1)

        self.max_ammo_display_checkbox = QCheckBox(self.qol_box)
        self.max_ammo_display_checkbox.setObjectName(u"max_ammo_display_checkbox")
        self.max_ammo_display_checkbox.setChecked(True)

        self.gridLayout_4.addWidget(self.max_ammo_display_checkbox, 2, 0, 1, 1)

        self.aim_with_any_button_checkbox = QCheckBox(self.qol_box)
        self.aim_with_any_button_checkbox.setObjectName(u"aim_with_any_button_checkbox")
        self.aim_with_any_button_checkbox.setChecked(True)

        self.gridLayout_4.addWidget(self.aim_with_any_button_checkbox, 6, 0, 1, 1)

        self.aim_with_any_button_label = QLabel(self.qol_box)
        self.aim_with_any_button_label.setObjectName(u"aim_with_any_button_label")

        self.gridLayout_4.addWidget(self.aim_with_any_button_label, 7, 0, 1, 1)


        self.scroll_area_layout.addWidget(self.qol_box)

        self.music_box = QGroupBox(self.scroll_area_contents)
        self.music_box.setObjectName(u"music_box")
        self.gridLayout_6 = QGridLayout(self.music_box)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.no_music_option = QRadioButton(self.music_box)
        self.no_music_option.setObjectName(u"no_music_option")
        self.no_music_option.setChecked(False)

        self.gridLayout_6.addWidget(self.no_music_option, 3, 0, 1, 1)

        self.vanilla_music_option = QRadioButton(self.music_box)
        self.vanilla_music_option.setObjectName(u"vanilla_music_option")
        self.vanilla_music_option.setChecked(True)

        self.gridLayout_6.addWidget(self.vanilla_music_option, 1, 0, 1, 1)

        self.music_label = QLabel(self.music_box)
        self.music_label.setObjectName(u"music_label")
        self.music_label.setWordWrap(True)

        self.gridLayout_6.addWidget(self.music_label, 0, 0, 1, 1)

        self.random_music_option = QRadioButton(self.music_box)
        self.random_music_option.setObjectName(u"random_music_option")
        self.random_music_option.setChecked(False)

        self.gridLayout_6.addWidget(self.random_music_option, 2, 0, 1, 1)


        self.scroll_area_layout.addWidget(self.music_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scroll_area_layout.addItem(self.verticalSpacer)

        self.scroll_area.setWidget(self.scroll_area_contents)

        self.main_layout.addWidget(self.scroll_area)

        self.reset_button = QPushButton(SuperCosmeticPatchesDialog)
        self.reset_button.setObjectName(u"reset_button")
        self.reset_button.setGeometry(QRect(290, 600, 122, 24))
        self.accept_button = QPushButton(SuperCosmeticPatchesDialog)
        self.accept_button.setObjectName(u"accept_button")
        self.accept_button.setGeometry(QRect(34, 600, 122, 24))
        self.cancel_button = QPushButton(SuperCosmeticPatchesDialog)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(162, 600, 122, 24))

        self.retranslateUi(SuperCosmeticPatchesDialog)

        QMetaObject.connectSlotsByName(SuperCosmeticPatchesDialog)
    # setupUi

    def retranslateUi(self, SuperCosmeticPatchesDialog):
        SuperCosmeticPatchesDialog.setWindowTitle(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Game Patches", None))
#if QT_CONFIG(tooltip)
        SuperCosmeticPatchesDialog.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.accessibility_box.setTitle(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Accessibility", None))
#if QT_CONFIG(tooltip)
        self.colorblind_checkbox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.colorblind_checkbox.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Colorblind Mode", None))
        self.colorblind_label.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Changes the colors of some game elements to be more easily distinguishable to players with some types of colorblindness.", None))
        self.qol_box.setTitle(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Quality of Life", None))
#if QT_CONFIG(tooltip)
        self.no_demo_checkbox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.no_demo_checkbox.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"No Demo", None))
        self.max_ammo_display_label.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Displays Samus' maximum ammunition on the HUD.", None))
        self.no_demo_label.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"The gameplay demo no longer plays on the title screen.", None))
#if QT_CONFIG(tooltip)
        self.max_ammo_display_checkbox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.max_ammo_display_checkbox.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Max Ammo Display", None))
#if QT_CONFIG(tooltip)
        self.aim_with_any_button_checkbox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.aim_with_any_button_checkbox.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Rebindable Aim", None))
        self.aim_with_any_button_label.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Allows aiming to be bound to any button, not just the shoulder buttons.", None))
        self.music_box.setTitle(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Music", None))
        self.no_music_option.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Off", None))
        self.vanilla_music_option.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Vanilla", None))
        self.music_label.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Changes the way music triggers behave.\n"
"Randomized music will choose a random song when activating a music trigger. Some music, such as the title theme, is not randomized.\n"
"Off will disable all music for the game.", None))
        self.random_music_option.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Randomized", None))
        self.reset_button.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Reset to Defaults", None))
        self.accept_button.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("SuperCosmeticPatchesDialog", u"Cancel", None))
    # retranslateUi


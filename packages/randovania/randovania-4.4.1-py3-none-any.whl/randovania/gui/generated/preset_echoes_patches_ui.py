# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_echoes_patches.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetEchoesPatches(object):
    def setupUi(self, PresetEchoesPatches):
        if not PresetEchoesPatches.objectName():
            PresetEchoesPatches.setObjectName(u"PresetEchoesPatches")
        PresetEchoesPatches.resize(466, 454)
        self.centralWidget = QWidget(PresetEchoesPatches)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.include_menu_mod_check = QCheckBox(self.centralWidget)
        self.include_menu_mod_check.setObjectName(u"include_menu_mod_check")
        self.include_menu_mod_check.setEnabled(True)

        self.verticalLayout.addWidget(self.include_menu_mod_check)

        self.include_menu_mod_label = QLabel(self.centralWidget)
        self.include_menu_mod_label.setObjectName(u"include_menu_mod_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.include_menu_mod_label.sizePolicy().hasHeightForWidth())
        self.include_menu_mod_label.setSizePolicy(sizePolicy)
        self.include_menu_mod_label.setMaximumSize(QSize(16777215, 60))
        self.include_menu_mod_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.include_menu_mod_label.setWordWrap(True)
        self.include_menu_mod_label.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.include_menu_mod_label)

        self.line_1 = QFrame(self.centralWidget)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.HLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_1)

        self.warp_to_start_check = QCheckBox(self.centralWidget)
        self.warp_to_start_check.setObjectName(u"warp_to_start_check")

        self.verticalLayout.addWidget(self.warp_to_start_check)

        self.warp_to_start_label = QLabel(self.centralWidget)
        self.warp_to_start_label.setObjectName(u"warp_to_start_label")
        sizePolicy.setHeightForWidth(self.warp_to_start_label.sizePolicy().hasHeightForWidth())
        self.warp_to_start_label.setSizePolicy(sizePolicy)
        self.warp_to_start_label.setMaximumSize(QSize(16777215, 70))
        self.warp_to_start_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.warp_to_start_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.warp_to_start_label)

        PresetEchoesPatches.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetEchoesPatches)

        QMetaObject.connectSlotsByName(PresetEchoesPatches)
    # setupUi

    def retranslateUi(self, PresetEchoesPatches):
        PresetEchoesPatches.setWindowTitle(QCoreApplication.translate("PresetEchoesPatches", u"Other", None))
        self.include_menu_mod_check.setText(QCoreApplication.translate("PresetEchoesPatches", u"Include Menu Mod", None))
        self.include_menu_mod_label.setText(QCoreApplication.translate("PresetEchoesPatches", u"<html><head/><body><p>Menu Mod is a practice tool for Echoes, allowing in-game changes to which items you have and warping to all rooms.</p><p>See the <a href=\"https://www.dropbox.com/s/yhqqafaxfo3l4vn/Echoes%20Menu.7z?file_subpath=%2FEchoes+Menu%2Freadme.txt\"><span style=\" text-decoration: underline; color:#0000ff;\">Menu Mod README</span></a> for more details.</p></body></html>", None))
        self.warp_to_start_check.setText(QCoreApplication.translate("PresetEchoesPatches", u"Add warping to starting location from save stations", None))
        self.warp_to_start_label.setText(QCoreApplication.translate("PresetEchoesPatches", u"<html><head/><body><p>Refusing to save at any Save Station will prompt if you want to warp to the starting location (by default, Samus' ship in Landing Site).</p><p><span style=\" color:#005500;\">Usage of the this option is encouraged for all, as it prevents many softlocks that occurs normally in Echoes.</span></p></body></html>", None))
    # retranslateUi


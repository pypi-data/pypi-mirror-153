# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_dread_energy.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetDreadEnergy(object):
    def setupUi(self, PresetDreadEnergy):
        if not PresetDreadEnergy.objectName():
            PresetDreadEnergy.setObjectName(u"PresetDreadEnergy")
        PresetDreadEnergy.resize(442, 277)
        self.centralWidget = QWidget(PresetDreadEnergy)
        self.centralWidget.setObjectName(u"centralWidget")
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
        self.scroll_area_contents.setGeometry(QRect(0, 0, 430, 282))
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
        self.energy_part_box = QGroupBox(self.scroll_area_contents)
        self.energy_part_box.setObjectName(u"energy_part_box")
        self.verticalLayout = QVBoxLayout(self.energy_part_box)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.immediate_energy_parts_check = QCheckBox(self.energy_part_box)
        self.immediate_energy_parts_check.setObjectName(u"immediate_energy_parts_check")

        self.verticalLayout.addWidget(self.immediate_energy_parts_check)

        self.immediate_energy_parts_label = QLabel(self.energy_part_box)
        self.immediate_energy_parts_label.setObjectName(u"immediate_energy_parts_label")
        self.immediate_energy_parts_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.immediate_energy_parts_label)


        self.scroll_area_layout.addWidget(self.energy_part_box)

        self.energy_tank_box = QGroupBox(self.scroll_area_contents)
        self.energy_tank_box.setObjectName(u"energy_tank_box")
        self.gridLayout_2 = QGridLayout(self.energy_tank_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.energy_tank_capacity_spin_box = QSpinBox(self.energy_tank_box)
        self.energy_tank_capacity_spin_box.setObjectName(u"energy_tank_capacity_spin_box")
        self.energy_tank_capacity_spin_box.setMinimum(2)
        self.energy_tank_capacity_spin_box.setMaximum(1000)

        self.gridLayout_2.addWidget(self.energy_tank_capacity_spin_box, 2, 1, 1, 1)

        self.energy_tank_capacity_label = QLabel(self.energy_tank_box)
        self.energy_tank_capacity_label.setObjectName(u"energy_tank_capacity_label")

        self.gridLayout_2.addWidget(self.energy_tank_capacity_label, 2, 0, 1, 1)

        self.energy_tank_capacity_description = QLabel(self.energy_tank_box)
        self.energy_tank_capacity_description.setObjectName(u"energy_tank_capacity_description")
        self.energy_tank_capacity_description.setWordWrap(True)

        self.gridLayout_2.addWidget(self.energy_tank_capacity_description, 0, 0, 1, 2)

        self.energy_tank_capacity_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.energy_tank_capacity_spacer, 1, 0, 1, 2)


        self.scroll_area_layout.addWidget(self.energy_tank_box)

        self.energy_tank_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scroll_area_layout.addItem(self.energy_tank_spacer)

        self.scroll_area.setWidget(self.scroll_area_contents)

        self.main_layout.addWidget(self.scroll_area)

        PresetDreadEnergy.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetDreadEnergy)

        QMetaObject.connectSlotsByName(PresetDreadEnergy)
    # setupUi

    def retranslateUi(self, PresetDreadEnergy):
        PresetDreadEnergy.setWindowTitle(QCoreApplication.translate("PresetDreadEnergy", u"Energy", None))
        self.energy_part_box.setTitle(QCoreApplication.translate("PresetDreadEnergy", u"Energy Part", None))
        self.immediate_energy_parts_check.setText(QCoreApplication.translate("PresetDreadEnergy", u"Immediate Energy Part", None))
        self.immediate_energy_parts_label.setText(QCoreApplication.translate("PresetDreadEnergy", u"When enabled, Energy Fragments immediately increase your maximum energy by 1/4 of the amount an Energy Tank would.", None))
        self.energy_tank_box.setTitle(QCoreApplication.translate("PresetDreadEnergy", u"Energy tank", None))
        self.energy_tank_capacity_spin_box.setSuffix(QCoreApplication.translate("PresetDreadEnergy", u" energy", None))
        self.energy_tank_capacity_label.setText(QCoreApplication.translate("PresetDreadEnergy", u"Energy per tank", None))
        self.energy_tank_capacity_description.setText(QCoreApplication.translate("PresetDreadEnergy", u"<html><head/><body><p>Configure how much energy each Energy Tank you collect will provide. Your base energy is always this quantity, minus 1.</p><p>While logic will respect this value, only the original value (100) has been tested.</p><p><span style=\" text-decoration: underline;\">The value can only be changed when Immediate Energy Part is enabled.</span></p></body></html>", None))
    # retranslateUi


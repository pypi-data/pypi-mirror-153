# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_prime_goal.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetPrimeGoal(object):
    def setupUi(self, PresetPrimeGoal):
        if not PresetPrimeGoal.objectName():
            PresetPrimeGoal.setObjectName(u"PresetPrimeGoal")
        PresetPrimeGoal.resize(383, 329)
        self.centralWidget = QWidget(PresetPrimeGoal)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.goal_layout = QVBoxLayout(self.centralWidget)
        self.goal_layout.setSpacing(6)
        self.goal_layout.setContentsMargins(11, 11, 11, 11)
        self.goal_layout.setObjectName(u"goal_layout")
        self.goal_layout.setContentsMargins(4, 8, 4, 0)
        self.goal_description = QLabel(self.centralWidget)
        self.goal_description.setObjectName(u"goal_description")
        self.goal_description.setWordWrap(True)

        self.goal_layout.addWidget(self.goal_description)

        self.slider_layout = QHBoxLayout()
        self.slider_layout.setSpacing(6)
        self.slider_layout.setObjectName(u"slider_layout")
        self.slider = QSlider(self.centralWidget)
        self.slider.setObjectName(u"slider")
        self.slider.setMaximum(12)
        self.slider.setPageStep(2)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)

        self.slider_layout.addWidget(self.slider)

        self.slider_label = QLabel(self.centralWidget)
        self.slider_label.setObjectName(u"slider_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider_label.sizePolicy().hasHeightForWidth())
        self.slider_label.setSizePolicy(sizePolicy)
        self.slider_label.setMinimumSize(QSize(20, 0))
        self.slider_label.setAlignment(Qt.AlignCenter)

        self.slider_layout.addWidget(self.slider_label)


        self.goal_layout.addLayout(self.slider_layout)

        PresetPrimeGoal.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetPrimeGoal)

        QMetaObject.connectSlotsByName(PresetPrimeGoal)
    # setupUi

    def retranslateUi(self, PresetPrimeGoal):
        PresetPrimeGoal.setWindowTitle(QCoreApplication.translate("PresetPrimeGoal", u"Goal", None))
        self.goal_description.setText(QCoreApplication.translate("PresetPrimeGoal", u"<html><head/><body><p>Controls how many Artifacts will be placed.</p><p>You can always check Artifact Temple for hints where the artifacts were placed.</p></body></html>", None))
        self.slider_label.setText(QCoreApplication.translate("PresetPrimeGoal", u"0", None))
    # retranslateUi


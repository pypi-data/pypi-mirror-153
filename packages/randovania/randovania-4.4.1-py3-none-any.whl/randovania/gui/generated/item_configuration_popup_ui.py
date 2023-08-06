# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'item_configuration_popup.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.lib.scroll_protected import *  # type: ignore

class Ui_ItemConfigurationPopup(object):
    def setupUi(self, ItemConfigurationPopup):
        if not ItemConfigurationPopup.objectName():
            ItemConfigurationPopup.setObjectName(u"ItemConfigurationPopup")
        ItemConfigurationPopup.resize(880, 122)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ItemConfigurationPopup.sizePolicy().hasHeightForWidth())
        ItemConfigurationPopup.setSizePolicy(sizePolicy)
        ItemConfigurationPopup.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(ItemConfigurationPopup)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.separator_line = QFrame(ItemConfigurationPopup)
        self.separator_line.setObjectName(u"separator_line")
        self.separator_line.setFrameShape(QFrame.HLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.separator_line, 0, 0, 1, 5)

        self.warning_label = QLabel(ItemConfigurationPopup)
        self.warning_label.setObjectName(u"warning_label")
        self.warning_label.setWordWrap(True)

        self.gridLayout_2.addWidget(self.warning_label, 4, 0, 1, 4)

        self.vanilla_check = QCheckBox(ItemConfigurationPopup)
        self.vanilla_check.setObjectName(u"vanilla_check")

        self.gridLayout_2.addWidget(self.vanilla_check, 3, 0, 1, 1)

        self.item_name_label = QLabel(ItemConfigurationPopup)
        self.item_name_label.setObjectName(u"item_name_label")
        self.item_name_label.setMinimumSize(QSize(150, 0))
        font = QFont()
        font.setBold(True)
        self.item_name_label.setFont(font)

        self.gridLayout_2.addWidget(self.item_name_label, 1, 0, 1, 1)

        self.starting_check = QCheckBox(ItemConfigurationPopup)
        self.starting_check.setObjectName(u"starting_check")

        self.gridLayout_2.addWidget(self.starting_check, 3, 1, 1, 1)

        self.state_case_combo = ScrollProtectedComboBox(ItemConfigurationPopup)
        self.state_case_combo.setObjectName(u"state_case_combo")

        self.gridLayout_2.addWidget(self.state_case_combo, 1, 4, 1, 1)

        self.provided_ammo_spinbox = ScrollProtectedSpinBox(ItemConfigurationPopup)
        self.provided_ammo_spinbox.setObjectName(u"provided_ammo_spinbox")

        self.gridLayout_2.addWidget(self.provided_ammo_spinbox, 1, 3, 1, 1)

        self.provided_ammo_label = QLabel(ItemConfigurationPopup)
        self.provided_ammo_label.setObjectName(u"provided_ammo_label")
        self.provided_ammo_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.provided_ammo_label.setWordWrap(True)

        self.gridLayout_2.addWidget(self.provided_ammo_label, 1, 1, 1, 2)

        self.shuffled_spinbox = ScrollProtectedSpinBox(ItemConfigurationPopup)
        self.shuffled_spinbox.setObjectName(u"shuffled_spinbox")
        self.shuffled_spinbox.setMinimum(1)
        self.shuffled_spinbox.setMaximum(99)

        self.gridLayout_2.addWidget(self.shuffled_spinbox, 3, 4, 1, 1)

        self.priority_combo = ScrollProtectedComboBox(ItemConfigurationPopup)
        self.priority_combo.setObjectName(u"priority_combo")

        self.gridLayout_2.addWidget(self.priority_combo, 3, 3, 1, 1)

        self.priority_label = QLabel(ItemConfigurationPopup)
        self.priority_label.setObjectName(u"priority_label")

        self.gridLayout_2.addWidget(self.priority_label, 3, 2, 1, 1)


        self.retranslateUi(ItemConfigurationPopup)

        QMetaObject.connectSlotsByName(ItemConfigurationPopup)
    # setupUi

    def retranslateUi(self, ItemConfigurationPopup):
        ItemConfigurationPopup.setWindowTitle(QCoreApplication.translate("ItemConfigurationPopup", u"Item Configuration", None))
        self.warning_label.setText("")
        self.vanilla_check.setText(QCoreApplication.translate("ItemConfigurationPopup", u"In Vanilla", None))
        self.item_name_label.setText(QCoreApplication.translate("ItemConfigurationPopup", u"Unlimited Beam Ammo", None))
        self.starting_check.setText(QCoreApplication.translate("ItemConfigurationPopup", u"As starting", None))
#if QT_CONFIG(tooltip)
        self.provided_ammo_label.setToolTip(QCoreApplication.translate("ItemConfigurationPopup", u"<html><head/><body><p>When this item is collected, it also gives this amount of the given ammos.</p><p>This is included in the calculation of how much each pickup of this ammo gives.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.provided_ammo_label.setText(QCoreApplication.translate("ItemConfigurationPopup", u"<html><head/><body><p>Provided Ammo (XXXX and YYYY)</p></body></html>", None))
        self.shuffled_spinbox.setSuffix(QCoreApplication.translate("ItemConfigurationPopup", u" shuffled copies", None))
        self.priority_label.setText(QCoreApplication.translate("ItemConfigurationPopup", u"Priority for placement", None))
    # retranslateUi


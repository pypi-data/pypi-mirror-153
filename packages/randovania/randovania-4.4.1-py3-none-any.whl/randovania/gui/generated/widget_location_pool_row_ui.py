# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget_location_pool_row.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_LocationPoolRowWidget(object):
    def setupUi(self, LocationPoolRowWidget):
        if not LocationPoolRowWidget.objectName():
            LocationPoolRowWidget.setObjectName(u"LocationPoolRowWidget")
        LocationPoolRowWidget.resize(616, 52)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LocationPoolRowWidget.sizePolicy().hasHeightForWidth())
        LocationPoolRowWidget.setSizePolicy(sizePolicy)
        LocationPoolRowWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(LocationPoolRowWidget)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 2, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_location_name = QLabel(LocationPoolRowWidget)
        self.label_location_name.setObjectName(u"label_location_name")
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.label_location_name.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_location_name)

        self.radio_shuffled = QRadioButton(LocationPoolRowWidget)
        self.radio_shuffled.setObjectName(u"radio_shuffled")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.radio_shuffled.sizePolicy().hasHeightForWidth())
        self.radio_shuffled.setSizePolicy(sizePolicy1)
        self.radio_shuffled.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radio_shuffled)

        self.radio_shuffled_no_progression = QRadioButton(LocationPoolRowWidget)
        self.radio_shuffled_no_progression.setObjectName(u"radio_shuffled_no_progression")
        sizePolicy1.setHeightForWidth(self.radio_shuffled_no_progression.sizePolicy().hasHeightForWidth())
        self.radio_shuffled_no_progression.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.radio_shuffled_no_progression)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.radio_vanilla = QRadioButton(LocationPoolRowWidget)
        self.radio_vanilla.setObjectName(u"radio_vanilla")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.radio_vanilla.sizePolicy().hasHeightForWidth())
        self.radio_vanilla.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.radio_vanilla)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radio_fixed = QRadioButton(LocationPoolRowWidget)
        self.radio_fixed.setObjectName(u"radio_fixed")
        sizePolicy1.setHeightForWidth(self.radio_fixed.sizePolicy().hasHeightForWidth())
        self.radio_fixed.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.radio_fixed)

        self.combo_fixed_item = QComboBox(LocationPoolRowWidget)
        self.combo_fixed_item.addItem("")
        self.combo_fixed_item.setObjectName(u"combo_fixed_item")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.combo_fixed_item.sizePolicy().hasHeightForWidth())
        self.combo_fixed_item.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.combo_fixed_item)


        self.horizontalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LocationPoolRowWidget)

        QMetaObject.connectSlotsByName(LocationPoolRowWidget)
    # setupUi

    def retranslateUi(self, LocationPoolRowWidget):
        LocationPoolRowWidget.setWindowTitle(QCoreApplication.translate("LocationPoolRowWidget", u"\n"
"				Item Configuration\n"
"			", None))
        self.label_location_name.setText(QCoreApplication.translate("LocationPoolRowWidget", u"Location name", None))
#if QT_CONFIG(tooltip)
        self.radio_shuffled.setToolTip(QCoreApplication.translate("LocationPoolRowWidget", u"This location is shuffled normally", None))
#endif // QT_CONFIG(tooltip)
        self.radio_shuffled.setText(QCoreApplication.translate("LocationPoolRowWidget", u"Shuffled", None))
#if QT_CONFIG(tooltip)
        self.radio_shuffled_no_progression.setToolTip(QCoreApplication.translate("LocationPoolRowWidget", u"This location is shuffled, but cannot contain a item required for progression", None))
#endif // QT_CONFIG(tooltip)
        self.radio_shuffled_no_progression.setText(QCoreApplication.translate("LocationPoolRowWidget", u"Shuffled (no progression)", None))
#if QT_CONFIG(tooltip)
        self.radio_vanilla.setToolTip(QCoreApplication.translate("LocationPoolRowWidget", u"This location is unchanged and will contain the same item as in the base game", None))
#endif // QT_CONFIG(tooltip)
        self.radio_vanilla.setText(QCoreApplication.translate("LocationPoolRowWidget", u"Vanilla", None))
#if QT_CONFIG(tooltip)
        self.radio_fixed.setToolTip(QCoreApplication.translate("LocationPoolRowWidget", u"This location contains a fixed item of your choosing", None))
#endif // QT_CONFIG(tooltip)
        self.radio_fixed.setText(QCoreApplication.translate("LocationPoolRowWidget", u"Fixed			", None))
        self.combo_fixed_item.setItemText(0, QCoreApplication.translate("LocationPoolRowWidget", u"No item", None))

        self.combo_fixed_item.setCurrentText(QCoreApplication.translate("LocationPoolRowWidget", u"No item", None))
    # retranslateUi


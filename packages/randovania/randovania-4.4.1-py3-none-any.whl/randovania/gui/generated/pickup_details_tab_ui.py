# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pickup_details_tab.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PickupDetailsTab(object):
    def setupUi(self, PickupDetailsTab):
        if not PickupDetailsTab.objectName():
            PickupDetailsTab.setObjectName(u"PickupDetailsTab")
        PickupDetailsTab.resize(624, 471)
        self.spoiler_pickup_layout = QGridLayout(PickupDetailsTab)
        self.spoiler_pickup_layout.setSpacing(6)
        self.spoiler_pickup_layout.setContentsMargins(11, 11, 11, 11)
        self.spoiler_pickup_layout.setObjectName(u"spoiler_pickup_layout")
        self.spoiler_pickup_layout.setContentsMargins(4, 8, 0, 0)
        self.pickup_spoiler_pickup_combobox = QComboBox(PickupDetailsTab)
        self.pickup_spoiler_pickup_combobox.addItem("")
        self.pickup_spoiler_pickup_combobox.setObjectName(u"pickup_spoiler_pickup_combobox")

        self.spoiler_pickup_layout.addWidget(self.pickup_spoiler_pickup_combobox, 2, 2, 1, 1)

        self.pickup_spoiler_label = QLabel(PickupDetailsTab)
        self.pickup_spoiler_label.setObjectName(u"pickup_spoiler_label")

        self.spoiler_pickup_layout.addWidget(self.pickup_spoiler_label, 2, 0, 1, 1)

        self.pickup_spoiler_show_all_button = QPushButton(PickupDetailsTab)
        self.pickup_spoiler_show_all_button.setObjectName(u"pickup_spoiler_show_all_button")

        self.spoiler_pickup_layout.addWidget(self.pickup_spoiler_show_all_button, 2, 1, 1, 1)

        self.pickup_spoiler_scroll_area = QScrollArea(PickupDetailsTab)
        self.pickup_spoiler_scroll_area.setObjectName(u"pickup_spoiler_scroll_area")
        self.pickup_spoiler_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.pickup_spoiler_scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.pickup_spoiler_scroll_area.setWidgetResizable(True)
        self.pickup_spoiler_scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.pickup_spoiler_scroll_contents = QWidget()
        self.pickup_spoiler_scroll_contents.setObjectName(u"pickup_spoiler_scroll_contents")
        self.pickup_spoiler_scroll_contents.setGeometry(QRect(0, 0, 332, 139))
        self.verticalLayout_3 = QVBoxLayout(self.pickup_spoiler_scroll_contents)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(3, 0, 3, -1)
        self.pickup_spoiler_scroll_content_layout = QVBoxLayout()
        self.pickup_spoiler_scroll_content_layout.setSpacing(6)
        self.pickup_spoiler_scroll_content_layout.setObjectName(u"pickup_spoiler_scroll_content_layout")

        self.verticalLayout_3.addLayout(self.pickup_spoiler_scroll_content_layout)

        self.pickup_spoiler_scroll_area.setWidget(self.pickup_spoiler_scroll_contents)

        self.spoiler_pickup_layout.addWidget(self.pickup_spoiler_scroll_area, 4, 0, 1, 3)

        self.spoiler_starting_location_label = QLabel(PickupDetailsTab)
        self.spoiler_starting_location_label.setObjectName(u"spoiler_starting_location_label")

        self.spoiler_pickup_layout.addWidget(self.spoiler_starting_location_label, 0, 0, 1, 3)

        self.spoiler_starting_items_label = QLabel(PickupDetailsTab)
        self.spoiler_starting_items_label.setObjectName(u"spoiler_starting_items_label")

        self.spoiler_pickup_layout.addWidget(self.spoiler_starting_items_label, 1, 0, 1, 3)


        self.retranslateUi(PickupDetailsTab)

        QMetaObject.connectSlotsByName(PickupDetailsTab)
    # setupUi

    def retranslateUi(self, PickupDetailsTab):
        self.pickup_spoiler_pickup_combobox.setItemText(0, QCoreApplication.translate("PickupDetailsTab", u"None", None))

#if QT_CONFIG(tooltip)
        self.pickup_spoiler_label.setToolTip(QCoreApplication.translate("PickupDetailsTab", u"Enter text to the right to filter the list below", None))
#endif // QT_CONFIG(tooltip)
        self.pickup_spoiler_label.setText(QCoreApplication.translate("PickupDetailsTab", u"Search Pickup", None))
        self.pickup_spoiler_show_all_button.setText(QCoreApplication.translate("PickupDetailsTab", u"Show All", None))
        self.spoiler_starting_location_label.setText(QCoreApplication.translate("PickupDetailsTab", u"Starting Location", None))
        self.spoiler_starting_items_label.setText(QCoreApplication.translate("PickupDetailsTab", u"Starting Items", None))
        pass
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games_help_supermetroid_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_SuperMetroidHelpWidget(object):
    def setupUi(self, SuperMetroidHelpWidget):
        if not SuperMetroidHelpWidget.objectName():
            SuperMetroidHelpWidget.setObjectName(u"SuperMetroidHelpWidget")
        SuperMetroidHelpWidget.resize(438, 393)
        self.faq_tab = QWidget()
        self.faq_tab.setObjectName(u"faq_tab")
        self.faq_layout = QGridLayout(self.faq_tab)
        self.faq_layout.setSpacing(6)
        self.faq_layout.setContentsMargins(11, 11, 11, 11)
        self.faq_layout.setObjectName(u"faq_layout")
        self.faq_layout.setContentsMargins(0, 0, 0, 0)
        self.faq_scroll_area = QScrollArea(self.faq_tab)
        self.faq_scroll_area.setObjectName(u"faq_scroll_area")
        self.faq_scroll_area.setWidgetResizable(True)
        self.faq_scroll_area_contents = QWidget()
        self.faq_scroll_area_contents.setObjectName(u"faq_scroll_area_contents")
        self.faq_scroll_area_contents.setGeometry(QRect(0, 0, 432, 361))
        self.gridLayout_10 = QGridLayout(self.faq_scroll_area_contents)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.faq_label = QLabel(self.faq_scroll_area_contents)
        self.faq_label.setObjectName(u"faq_label")
        self.faq_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.faq_label.setWordWrap(True)

        self.gridLayout_10.addWidget(self.faq_label, 0, 0, 1, 1)

        self.faq_scroll_area.setWidget(self.faq_scroll_area_contents)

        self.faq_layout.addWidget(self.faq_scroll_area, 0, 0, 1, 1)

        SuperMetroidHelpWidget.addTab(self.faq_tab, "")

        self.retranslateUi(SuperMetroidHelpWidget)

        SuperMetroidHelpWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SuperMetroidHelpWidget)
    # setupUi

    def retranslateUi(self, SuperMetroidHelpWidget):
        self.faq_label.setText(QCoreApplication.translate("SuperMetroidHelpWidget", u"# updated from code", None))
        SuperMetroidHelpWidget.setTabText(SuperMetroidHelpWidget.indexOf(self.faq_tab), QCoreApplication.translate("SuperMetroidHelpWidget", u"FAQ", None))
        pass
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games_help_prime_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PrimeHelpWidget(object):
    def setupUi(self, PrimeHelpWidget):
        if not PrimeHelpWidget.objectName():
            PrimeHelpWidget.setObjectName(u"PrimeHelpWidget")
        PrimeHelpWidget.resize(438, 393)
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

        PrimeHelpWidget.addTab(self.faq_tab, "")
        self.hints_tab = QWidget()
        self.hints_tab.setObjectName(u"hints_tab")
        self.hints_tab_layout_4 = QVBoxLayout(self.hints_tab)
        self.hints_tab_layout_4.setSpacing(0)
        self.hints_tab_layout_4.setContentsMargins(11, 11, 11, 11)
        self.hints_tab_layout_4.setObjectName(u"hints_tab_layout_4")
        self.hints_tab_layout_4.setContentsMargins(0, 0, 0, 0)
        self.hints_scroll_area = QScrollArea(self.hints_tab)
        self.hints_scroll_area.setObjectName(u"hints_scroll_area")
        self.hints_scroll_area.setWidgetResizable(True)
        self.hints_scroll_area_contents = QWidget()
        self.hints_scroll_area_contents.setObjectName(u"hints_scroll_area_contents")
        self.hints_scroll_area_contents.setGeometry(QRect(0, 0, 432, 361))
        self.hints_scroll_layout_4 = QVBoxLayout(self.hints_scroll_area_contents)
        self.hints_scroll_layout_4.setSpacing(6)
        self.hints_scroll_layout_4.setContentsMargins(11, 11, 11, 11)
        self.hints_scroll_layout_4.setObjectName(u"hints_scroll_layout_4")
        self.hints_label = QLabel(self.hints_scroll_area_contents)
        self.hints_label.setObjectName(u"hints_label")
        self.hints_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hints_label.setWordWrap(True)

        self.hints_scroll_layout_4.addWidget(self.hints_label)

        self.hints_scroll_area.setWidget(self.hints_scroll_area_contents)

        self.hints_tab_layout_4.addWidget(self.hints_scroll_area)

        PrimeHelpWidget.addTab(self.hints_tab, "")
        self.hint_item_names_tab = QWidget()
        self.hint_item_names_tab.setObjectName(u"hint_item_names_tab")
        self.hint_item_names_layout_4 = QVBoxLayout(self.hint_item_names_tab)
        self.hint_item_names_layout_4.setSpacing(0)
        self.hint_item_names_layout_4.setContentsMargins(11, 11, 11, 11)
        self.hint_item_names_layout_4.setObjectName(u"hint_item_names_layout_4")
        self.hint_item_names_layout_4.setContentsMargins(0, 0, 0, 0)
        self.hint_item_names_scroll_area = QScrollArea(self.hint_item_names_tab)
        self.hint_item_names_scroll_area.setObjectName(u"hint_item_names_scroll_area")
        self.hint_item_names_scroll_area.setWidgetResizable(True)
        self.hint_item_names_scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hint_item_names_scroll_contents = QWidget()
        self.hint_item_names_scroll_contents.setObjectName(u"hint_item_names_scroll_contents")
        self.hint_item_names_scroll_contents.setGeometry(QRect(0, 0, 432, 361))
        self.hint_item_names_scroll_layout_4 = QVBoxLayout(self.hint_item_names_scroll_contents)
        self.hint_item_names_scroll_layout_4.setSpacing(6)
        self.hint_item_names_scroll_layout_4.setContentsMargins(11, 11, 11, 11)
        self.hint_item_names_scroll_layout_4.setObjectName(u"hint_item_names_scroll_layout_4")
        self.hint_item_names_label = QLabel(self.hint_item_names_scroll_contents)
        self.hint_item_names_label.setObjectName(u"hint_item_names_label")
        self.hint_item_names_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hint_item_names_label.setWordWrap(True)

        self.hint_item_names_scroll_layout_4.addWidget(self.hint_item_names_label)

        self.hint_item_names_tree_widget = QTableWidget(self.hint_item_names_scroll_contents)
        if (self.hint_item_names_tree_widget.columnCount() < 4):
            self.hint_item_names_tree_widget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.hint_item_names_tree_widget.setObjectName(u"hint_item_names_tree_widget")
        self.hint_item_names_tree_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hint_item_names_tree_widget.setSortingEnabled(True)

        self.hint_item_names_scroll_layout_4.addWidget(self.hint_item_names_tree_widget)

        self.hint_item_names_scroll_area.setWidget(self.hint_item_names_scroll_contents)

        self.hint_item_names_layout_4.addWidget(self.hint_item_names_scroll_area)

        PrimeHelpWidget.addTab(self.hint_item_names_tab, "")

        self.retranslateUi(PrimeHelpWidget)

        PrimeHelpWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PrimeHelpWidget)
    # setupUi

    def retranslateUi(self, PrimeHelpWidget):
        self.faq_label.setText(QCoreApplication.translate("PrimeHelpWidget", u"# updated from code", None))
        PrimeHelpWidget.setTabText(PrimeHelpWidget.indexOf(self.faq_tab), QCoreApplication.translate("PrimeHelpWidget", u"FAQ", None))
        self.hints_label.setText(QCoreApplication.translate("PrimeHelpWidget", u"<html><head/><body><p align=\"justify\">In\n"
"                                                Metroid Prime, you can find hints from the following\n"
"                                                sources:</p><p align=\"justify\"><span\n"
"                                                style=\" font-weight:600;\">Artifact Temple</span>:\n"
"                                                Hints for where each of your 12 Artifacts are located.\n"
"                                                In a Multiworld, describes which player has the\n"
"                                                artifacts as well.</p></body></html>\n"
"                                            ", None))
        PrimeHelpWidget.setTabText(PrimeHelpWidget.indexOf(self.hints_tab), QCoreApplication.translate("PrimeHelpWidget", u"Hints", None))
        self.hint_item_names_label.setText(QCoreApplication.translate("PrimeHelpWidget", u"<html><head/><body><p>When\n"
"                                                items are referenced in a hint, multiple names can be\n"
"                                                used depending on how precise the hint is. The names\n"
"                                                each item can use are the following:</p></body></html>\n"
"                                            ", None))
        ___qtablewidgetitem = self.hint_item_names_tree_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PrimeHelpWidget", u"Item", None));
        ___qtablewidgetitem1 = self.hint_item_names_tree_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PrimeHelpWidget", u"Precise Category", None));
        ___qtablewidgetitem2 = self.hint_item_names_tree_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PrimeHelpWidget", u"General Category", None));
        ___qtablewidgetitem3 = self.hint_item_names_tree_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PrimeHelpWidget", u"Broad Category", None));
        PrimeHelpWidget.setTabText(PrimeHelpWidget.indexOf(self.hint_item_names_tab), QCoreApplication.translate("PrimeHelpWidget", u"Hint Item Names", None))
        pass
    # retranslateUi


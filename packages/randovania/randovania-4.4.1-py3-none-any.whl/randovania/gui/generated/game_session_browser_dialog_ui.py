# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_session_browser_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_GameSessionBrowserDialog(object):
    def setupUi(self, GameSessionBrowserDialog):
        if not GameSessionBrowserDialog.objectName():
            GameSessionBrowserDialog.setObjectName(u"GameSessionBrowserDialog")
        GameSessionBrowserDialog.resize(694, 455)
        self.verticalLayout = QVBoxLayout(GameSessionBrowserDialog)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.menu_bar = QMenuBar(GameSessionBrowserDialog)
        self.menu_bar.setObjectName(u"menu_bar")

        self.verticalLayout.addWidget(self.menu_bar)

        self.table_widget = QTableWidget(GameSessionBrowserDialog)
        if (self.table_widget.columnCount() < 6):
            self.table_widget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.table_widget.setObjectName(u"table_widget")
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setTabKeyNavigation(False)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSortingEnabled(True)
        self.table_widget.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.table_widget)

        self.filter_group = QGroupBox(GameSessionBrowserDialog)
        self.filter_group.setObjectName(u"filter_group")
        self.gridLayout = QGridLayout(self.filter_group)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.has_password_yes_check = QCheckBox(self.filter_group)
        self.has_password_yes_check.setObjectName(u"has_password_yes_check")
        self.has_password_yes_check.setChecked(True)

        self.gridLayout.addWidget(self.has_password_yes_check, 2, 1, 1, 1)

        self.state_inprogress_check = QCheckBox(self.filter_group)
        self.state_inprogress_check.setObjectName(u"state_inprogress_check")
        self.state_inprogress_check.setChecked(True)

        self.gridLayout.addWidget(self.state_inprogress_check, 3, 2, 1, 1)

        self.has_password_no_check = QCheckBox(self.filter_group)
        self.has_password_no_check.setObjectName(u"has_password_no_check")
        self.has_password_no_check.setChecked(True)

        self.gridLayout.addWidget(self.has_password_no_check, 2, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 4, 1, 1)

        self.filter_name_edit = QLineEdit(self.filter_group)
        self.filter_name_edit.setObjectName(u"filter_name_edit")

        self.gridLayout.addWidget(self.filter_name_edit, 0, 1, 1, 4)

        self.state_filter_label = QLabel(self.filter_group)
        self.state_filter_label.setObjectName(u"state_filter_label")

        self.gridLayout.addWidget(self.state_filter_label, 3, 0, 1, 1)

        self.state_finished_check = QCheckBox(self.filter_group)
        self.state_finished_check.setObjectName(u"state_finished_check")

        self.gridLayout.addWidget(self.state_finished_check, 3, 3, 1, 1)

        self.state_setup_check = QCheckBox(self.filter_group)
        self.state_setup_check.setObjectName(u"state_setup_check")
        self.state_setup_check.setChecked(True)

        self.gridLayout.addWidget(self.state_setup_check, 3, 1, 1, 1)

        self.filter_name_label = QLabel(self.filter_group)
        self.filter_name_label.setObjectName(u"filter_name_label")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_name_label.sizePolicy().hasHeightForWidth())
        self.filter_name_label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.filter_name_label, 0, 0, 1, 1)

        self.has_password_label = QLabel(self.filter_group)
        self.has_password_label.setObjectName(u"has_password_label")

        self.gridLayout.addWidget(self.has_password_label, 2, 0, 1, 1)

        self.filter_age_label = QLabel(self.filter_group)
        self.filter_age_label.setObjectName(u"filter_age_label")

        self.gridLayout.addWidget(self.filter_age_label, 4, 0, 1, 1)

        self.filter_age_check = QCheckBox(self.filter_group)
        self.filter_age_check.setObjectName(u"filter_age_check")
        self.filter_age_check.setChecked(True)

        self.gridLayout.addWidget(self.filter_age_check, 4, 1, 1, 1)

        self.filter_age_spin = QSpinBox(self.filter_group)
        self.filter_age_spin.setObjectName(u"filter_age_spin")
        self.filter_age_spin.setMaximum(365)
        self.filter_age_spin.setValue(14)

        self.gridLayout.addWidget(self.filter_age_spin, 4, 2, 1, 2)


        self.verticalLayout.addWidget(self.filter_group)

        self.label_layout = QHBoxLayout()
        self.label_layout.setSpacing(6)
        self.label_layout.setObjectName(u"label_layout")
        self.status_label = QLabel(GameSessionBrowserDialog)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setWordWrap(True)

        self.label_layout.addWidget(self.status_label)

        self.server_connection_label = QLabel(GameSessionBrowserDialog)
        self.server_connection_label.setObjectName(u"server_connection_label")
        self.server_connection_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.label_layout.addWidget(self.server_connection_label)


        self.verticalLayout.addLayout(self.label_layout)

        self.button_box = QDialogButtonBox(GameSessionBrowserDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setMinimumSize(QSize(500, 0))
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(GameSessionBrowserDialog)

        QMetaObject.connectSlotsByName(GameSessionBrowserDialog)
    # setupUi

    def retranslateUi(self, GameSessionBrowserDialog):
        GameSessionBrowserDialog.setWindowTitle(QCoreApplication.translate("GameSessionBrowserDialog", u"Session Browser", None))
        ___qtablewidgetitem = self.table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Name", None));
        ___qtablewidgetitem1 = self.table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"State", None));
        ___qtablewidgetitem2 = self.table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Players", None));
        ___qtablewidgetitem3 = self.table_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Password?", None));
        ___qtablewidgetitem4 = self.table_widget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Creator", None));
        ___qtablewidgetitem5 = self.table_widget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Creation Date", None));
        self.filter_group.setTitle(QCoreApplication.translate("GameSessionBrowserDialog", u"Filters", None))
        self.has_password_yes_check.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Yes", None))
        self.state_inprogress_check.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"In-Progress", None))
        self.has_password_no_check.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"No", None))
        self.state_filter_label.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"State:", None))
        self.state_finished_check.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Finished", None))
        self.state_setup_check.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Setup", None))
        self.filter_name_label.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Name", None))
        self.has_password_label.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Has Password?", None))
        self.filter_age_label.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Age:", None))
        self.filter_age_check.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Limit to", None))
        self.filter_age_spin.setSuffix(QCoreApplication.translate("GameSessionBrowserDialog", u" days", None))
        self.status_label.setText("")
        self.server_connection_label.setText(QCoreApplication.translate("GameSessionBrowserDialog", u"Server: Disconnected", None))
    # retranslateUi


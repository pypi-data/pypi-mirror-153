# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cs_game_export_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_CSGameExportDialog(object):
    def setupUi(self, CSGameExportDialog):
        if not CSGameExportDialog.objectName():
            CSGameExportDialog.setObjectName(u"CSGameExportDialog")
        CSGameExportDialog.resize(508, 270)
        self.gridLayout = QGridLayout(CSGameExportDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cancel_button = QPushButton(CSGameExportDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 6, 2, 1, 1)

        self.output_file_button = QPushButton(CSGameExportDialog)
        self.output_file_button.setObjectName(u"output_file_button")
        self.output_file_button.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.output_file_button, 3, 2, 1, 1)

        self.accept_button = QPushButton(CSGameExportDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 6, 0, 1, 1)

        self.auto_save_spoiler_check = QCheckBox(CSGameExportDialog)
        self.auto_save_spoiler_check.setObjectName(u"auto_save_spoiler_check")

        self.gridLayout.addWidget(self.auto_save_spoiler_check, 5, 0, 1, 1)

        self.description_label = QLabel(CSGameExportDialog)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.gridLayout.addWidget(self.description_label, 0, 0, 1, 3)

        self.output_file_edit = QLineEdit(CSGameExportDialog)
        self.output_file_edit.setObjectName(u"output_file_edit")

        self.gridLayout.addWidget(self.output_file_edit, 3, 0, 1, 2)

        self.output_file_label = QLabel(CSGameExportDialog)
        self.output_file_label.setObjectName(u"output_file_label")
        self.output_file_label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.output_file_label, 2, 0, 1, 2)


        self.retranslateUi(CSGameExportDialog)

        QMetaObject.connectSlotsByName(CSGameExportDialog)
    # setupUi

    def retranslateUi(self, CSGameExportDialog):
        CSGameExportDialog.setWindowTitle(QCoreApplication.translate("CSGameExportDialog", u"Game Patching", None))
        self.cancel_button.setText(QCoreApplication.translate("CSGameExportDialog", u"Cancel", None))
        self.output_file_button.setText(QCoreApplication.translate("CSGameExportDialog", u"Select File", None))
        self.accept_button.setText(QCoreApplication.translate("CSGameExportDialog", u"Accept", None))
        self.auto_save_spoiler_check.setText(QCoreApplication.translate("CSGameExportDialog", u"Include a spoiler log on same directory", None))
        self.description_label.setText(QCoreApplication.translate("CSGameExportDialog", u"<html><head/><body><p>A copy of Cave Story is included, so no input is needed.</p></body></html>", None))
        self.output_file_edit.setPlaceholderText(QCoreApplication.translate("CSGameExportDialog", u"Path where to place randomized game", None))
        self.output_file_label.setText(QCoreApplication.translate("CSGameExportDialog", u"Output Path", None))
    # retranslateUi


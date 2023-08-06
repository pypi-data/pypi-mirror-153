# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_item_pool.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.lib.scroll_protected import *  # type: ignore

class Ui_PresetItemPool(object):
    def setupUi(self, PresetItemPool):
        if not PresetItemPool.objectName():
            PresetItemPool.setObjectName(u"PresetItemPool")
        PresetItemPool.resize(566, 227)
        PresetItemPool.setMaximumSize(QSize(16777215, 16777215))
        self.centralWidget = QWidget(PresetItemPool)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.item_pool_count_label = QLabel(self.centralWidget)
        self.item_pool_count_label.setObjectName(u"item_pool_count_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.item_pool_count_label.sizePolicy().hasHeightForWidth())
        self.item_pool_count_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.item_pool_count_label.setFont(font)
        self.item_pool_count_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.item_pool_count_label)

        self.verticalSpacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scroll_area = QScrollArea(self.centralWidget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 556, 183))
        self.item_pool_layout = QVBoxLayout(self.scroll_area_contents)
        self.item_pool_layout.setSpacing(6)
        self.item_pool_layout.setContentsMargins(11, 11, 11, 11)
        self.item_pool_layout.setObjectName(u"item_pool_layout")
        self.item_pool_layout.setContentsMargins(0, 6, 0, 0)
        self.random_starting_box = QGroupBox(self.scroll_area_contents)
        self.random_starting_box.setObjectName(u"random_starting_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.random_starting_box.sizePolicy().hasHeightForWidth())
        self.random_starting_box.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.random_starting_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.minimum_starting_spinbox = ScrollProtectedSpinBox(self.random_starting_box)
        self.minimum_starting_spinbox.setObjectName(u"minimum_starting_spinbox")
        self.minimum_starting_spinbox.setMaximum(30)

        self.gridLayout_2.addWidget(self.minimum_starting_spinbox, 1, 1, 1, 1)

        self.minimum_starting_label = QLabel(self.random_starting_box)
        self.minimum_starting_label.setObjectName(u"minimum_starting_label")
        self.minimum_starting_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.minimum_starting_label, 1, 0, 1, 1)

        self.random_starting_label = QLabel(self.random_starting_box)
        self.random_starting_label.setObjectName(u"random_starting_label")
        self.random_starting_label.setFrameShape(QFrame.NoFrame)
        self.random_starting_label.setFrameShadow(QFrame.Plain)
        self.random_starting_label.setWordWrap(True)

        self.gridLayout_2.addWidget(self.random_starting_label, 0, 0, 1, 2)

        self.maximum_starting_spinbox = ScrollProtectedSpinBox(self.random_starting_box)
        self.maximum_starting_spinbox.setObjectName(u"maximum_starting_spinbox")
        self.maximum_starting_spinbox.setMaximum(30)

        self.gridLayout_2.addWidget(self.maximum_starting_spinbox, 2, 1, 1, 1)

        self.maximum_starting_label = QLabel(self.random_starting_box)
        self.maximum_starting_label.setObjectName(u"maximum_starting_label")

        self.gridLayout_2.addWidget(self.maximum_starting_label, 2, 0, 1, 1)


        self.item_pool_layout.addWidget(self.random_starting_box)

        self.scroll_area.setWidget(self.scroll_area_contents)

        self.verticalLayout.addWidget(self.scroll_area)

        PresetItemPool.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetItemPool)

        QMetaObject.connectSlotsByName(PresetItemPool)
    # setupUi

    def retranslateUi(self, PresetItemPool):
        PresetItemPool.setWindowTitle(QCoreApplication.translate("PresetItemPool", u"Item Pool", None))
#if QT_CONFIG(tooltip)
        self.item_pool_count_label.setToolTip(QCoreApplication.translate("PresetItemPool", u"If there are fewer than 119 items, the rest of the item locations will contain Energy Transfer Modules.", None))
#endif // QT_CONFIG(tooltip)
        self.item_pool_count_label.setText(QCoreApplication.translate("PresetItemPool", u"Items in pool: #/119", None))
        self.random_starting_box.setTitle(QCoreApplication.translate("PresetItemPool", u"Random Starting Items", None))
        self.minimum_starting_label.setText(QCoreApplication.translate("PresetItemPool", u"Start with at least this many items:", None))
        self.random_starting_label.setText(QCoreApplication.translate("PresetItemPool", u"<html><head/><body><p>Randovania will add additional starting items if necessary to make the seed possible.<br/>The first value controls how many items are always added.<br/>The second value controls how many items the seed can have before it fails to generate.</p></body></html>", None))
        self.maximum_starting_label.setText(QCoreApplication.translate("PresetItemPool", u"Start with at most this many items:", None))
    # retranslateUi


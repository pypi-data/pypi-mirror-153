# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randovania_help_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_RandovaniaHelpWidget(object):
    def setupUi(self, RandovaniaHelpWidget):
        if not RandovaniaHelpWidget.objectName():
            RandovaniaHelpWidget.setObjectName(u"RandovaniaHelpWidget")
        RandovaniaHelpWidget.resize(428, 587)
        self.tab_multiworld = QWidget()
        self.tab_multiworld.setObjectName(u"tab_multiworld")
        self.verticalLayout = QVBoxLayout(self.tab_multiworld)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.multiworld_scroll_area = QScrollArea(self.tab_multiworld)
        self.multiworld_scroll_area.setObjectName(u"multiworld_scroll_area")
        self.multiworld_scroll_area.setWidgetResizable(True)
        self.multiworld_scroll_area_contents = QWidget()
        self.multiworld_scroll_area_contents.setObjectName(u"multiworld_scroll_area_contents")
        self.multiworld_scroll_area_contents.setGeometry(QRect(0, -544, 408, 1098))
        self.multiworld_scroll_contents_layout = QGridLayout(self.multiworld_scroll_area_contents)
        self.multiworld_scroll_contents_layout.setSpacing(6)
        self.multiworld_scroll_contents_layout.setContentsMargins(11, 11, 11, 11)
        self.multiworld_scroll_contents_layout.setObjectName(u"multiworld_scroll_contents_layout")
        self.multiworld_label = QLabel(self.multiworld_scroll_area_contents)
        self.multiworld_label.setObjectName(u"multiworld_label")
        self.multiworld_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.multiworld_label.setWordWrap(True)

        self.multiworld_scroll_contents_layout.addWidget(self.multiworld_label, 0, 0, 1, 1)

        self.multiworld_scroll_area.setWidget(self.multiworld_scroll_area_contents)

        self.verticalLayout.addWidget(self.multiworld_scroll_area)

        RandovaniaHelpWidget.addTab(self.tab_multiworld, "")
        self.tab_tracker = QWidget()
        self.tab_tracker.setObjectName(u"tab_tracker")
        self.tracker_tab_layout = QVBoxLayout(self.tab_tracker)
        self.tracker_tab_layout.setSpacing(6)
        self.tracker_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.tracker_tab_layout.setObjectName(u"tracker_tab_layout")
        self.tracker_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tracker_scroll_area = QScrollArea(self.tab_tracker)
        self.tracker_scroll_area.setObjectName(u"tracker_scroll_area")
        self.tracker_scroll_area.setWidgetResizable(True)
        self.tracker_scroll_area_contents = QWidget()
        self.tracker_scroll_area_contents.setObjectName(u"tracker_scroll_area_contents")
        self.tracker_scroll_area_contents.setGeometry(QRect(0, 0, 422, 554))
        self.tracker_scroll_area_layout = QVBoxLayout(self.tracker_scroll_area_contents)
        self.tracker_scroll_area_layout.setSpacing(6)
        self.tracker_scroll_area_layout.setContentsMargins(11, 11, 11, 11)
        self.tracker_scroll_area_layout.setObjectName(u"tracker_scroll_area_layout")
        self.tracker_label = QLabel(self.tracker_scroll_area_contents)
        self.tracker_label.setObjectName(u"tracker_label")
        self.tracker_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.tracker_label.setWordWrap(True)

        self.tracker_scroll_area_layout.addWidget(self.tracker_label)

        self.tracker_scroll_area.setWidget(self.tracker_scroll_area_contents)

        self.tracker_tab_layout.addWidget(self.tracker_scroll_area)

        RandovaniaHelpWidget.addTab(self.tab_tracker, "")
        self.database_viewer_tab = QWidget()
        self.database_viewer_tab.setObjectName(u"database_viewer_tab")
        self.verticalLayout_3 = QVBoxLayout(self.database_viewer_tab)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.database_viewer_scroll_area = QScrollArea(self.database_viewer_tab)
        self.database_viewer_scroll_area.setObjectName(u"database_viewer_scroll_area")
        self.database_viewer_scroll_area.setWidgetResizable(True)
        self.database_viewer_scroll_area_contents = QWidget()
        self.database_viewer_scroll_area_contents.setObjectName(u"database_viewer_scroll_area_contents")
        self.database_viewer_scroll_area_contents.setGeometry(QRect(0, -302, 408, 1030))
        self.verticalLayout_2 = QVBoxLayout(self.database_viewer_scroll_area_contents)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(9, -1, -1, -1)
        self.database_viewer_label = QLabel(self.database_viewer_scroll_area_contents)
        self.database_viewer_label.setObjectName(u"database_viewer_label")
        self.database_viewer_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.database_viewer_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.database_viewer_label)

        self.database_viewer_scroll_area.setWidget(self.database_viewer_scroll_area_contents)

        self.verticalLayout_3.addWidget(self.database_viewer_scroll_area)

        RandovaniaHelpWidget.addTab(self.database_viewer_tab, "")

        self.retranslateUi(RandovaniaHelpWidget)

        RandovaniaHelpWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RandovaniaHelpWidget)
    # setupUi

    def retranslateUi(self, RandovaniaHelpWidget):
        self.multiworld_label.setText(QCoreApplication.translate("RandovaniaHelpWidget", u"<html><head/><body><p>Multiworld is a co-op multiplayer game mode for the randomizer.</p><p>In a multiworld game, each player has their own unique world filled with items destined for an specific player. When you collect an item, it is instantly delivered to the owner.</p><p><span style=\" font-weight:600;\">How do I play multiworld?</span></p><p>In the Play tab, either join a session or host a new one. Create one row for each player, customize their presets and then generate a game. Double check if the presets are correct and then start the session.</p><p>Each player exports their own ISO and opens it in Dolphin or Nintendont and keeps Randovania open.</p><p><span style=\" font-weight:600;\">How do I send an item to someone else?</span></p><p>Certain items in your game will belong to some other player. After collected, you receive an alert that it was sent to someone else.</p><p>You must make sure that Randovania is connected to the game and the game session window is open. The History tab in the session can "
                        "be used to confirm the item was detected and sent correctly.</p><p>WARNING: Collecting multiple items for other players in quick succession (less than 5s) will prevent Randovania from detecting either item, causing both to be lost until you reload a save file. Using Infinite Speed to collect multiple items at once will hit this limitation.</p><p><span style=\" font-weight:600;\">What happens if I die, reload a save or crash?</span></p><p>All received items you've lost are automatically re-delivered. Collecting some item you've already sent someone else has no effect and is perfectly safe.</p><p><span style=\" font-weight:600;\">What happens if I disconnect from the server?</span></p><p>Randovania keeps track of everything you've collected and will send to the server as soon as it regains connection, even if restarted.</p><p><span style=\" font-weight:600;\">What happens if Randovania disconnects from the game?</span></p><p>Do <span style=\" font-style:italic;\">not</span> collect any item if Randovania is not "
                        "connected to your game (closed, error in connection) as it will be lost forever. </p><p><span style=\" font-weight:600;\">Do all players have to play at the same time?</span></p><p>No. All comunication between players is managed by Randovania's server.</p><p><span style=\" font-weight:600;\">Can I play on a Wii?</span></p><p>Yes. Connect your Wii to the same Wifi as your computer and open Homebrew Channel. Press the &quot;Upload Nintendont to Homebrew Channel&quot; button found in the <span style=\" font-style:italic;\">Configure backend</span> menu of the Game Session window.</p><p><span style=\" font-weight:600;\">Can different games be mixed in a session?</span></p><p>Yes. Items for another game will be appear using an equivalent model for your game, or the generic model (Nothing for Prime 1, Energy Transfer Module for Prime 2). </p><p>You can also provide a copy of the other game during the game export process to use the correct models from the other game.  Currently, this has some caveats:</p><ul style=\""
                        "margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Non-vanilla item models aren't converted. This includes light and dark ammo expansions and translators in Echoes, and the Phazon Suit in Prime.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When loading a room with a Prime 1 item in Echoes, there may be a slight stutter in gameplay</li></ul><p><span style=\" font-weight:600;\">How many players can play at the same time?</span></p><p>While there are no hard limits, only up to 30 players have been confirmed to work.<br/>If planning a bigger session, contact Darkszero in the community Discord.</p></body></html>", None))
        RandovaniaHelpWidget.setTabText(RandovaniaHelpWidget.indexOf(self.tab_multiworld), QCoreApplication.translate("RandovaniaHelpWidget", u"Multiworld", None))
        self.tracker_label.setText(QCoreApplication.translate("RandovaniaHelpWidget", u"<html><head/><body><p>Randovania includes a simple &quot;map&quot; tracker.</p><p>To open, click the <span style=\" font-weight:600;\">Generate Game</span> tab and right-click the preset under the game you will use to generate a seed.</p><p><img src=\"data/gui_assets/tracker-open.png\"/></p><p>The tracker uses the logic and game modifications configuration from the selected preset. It shows where you can go depending on where you are in the game, as well as which items you've picked up and events you've triggered.</p><p>To use the tracker, simply select the items on the left that you have. This will open up new locations on the right side. Click events and pickups as you progress for more locations to show up. If you make a mistake, click the <span style=\" font-weight:600;\">Actions</span> tab to undo the latest action you made.</p><p>If you randomized the elevators, click the <span style=\" font-weight:600;\">Elevators</span> tab to configure how the elevators are setup. If you shuffled the translator gates "
                        "in Prime 2, you can configure those as well via the <span style=\" font-weight:600;\">Translator Gate</span> tab.</p><p>Random starting location is also accounted for if enabled for your settings, so make sure you set the correct starting room when opening the tracker.</p></body></html>", None))
        RandovaniaHelpWidget.setTabText(RandovaniaHelpWidget.indexOf(self.tab_tracker), QCoreApplication.translate("RandovaniaHelpWidget", u"Tracker", None))
        self.database_viewer_label.setText(QCoreApplication.translate("RandovaniaHelpWidget", u"<html><head/><body><p>Randovania has an extensive database with many tricks and paths that are configurable in a given preset. This is where all the logic is stored and determines what is required of a player in a seed given certain trick difficulties.</p><p>To open the database, click the <span style=\" font-weight:600;\">Open</span> menu and select a game from the dropdown. From here you can view each individual trick or click the <span style=\" font-weight:600;\">Data Visualizer</span> option.</p><p><img src=\"data/gui_assets/database-open.png\"/></p><p>Using the database might take some time to get used to, but it is highly recommended to get familiar with it in case you need to figure out what tricks you might want to play with and how to get from point A to point B.</p><p><span style=\" font-weight:600;\">How to Read the Database</span></p><p><img src=\"data/gui_assets/database-example.png\"/></p><p>The left dropdown lists the areas for the respective game, and the right dropdown is the list of rooms in "
                        "the area selected.</p><p>Once you have a room selected, click a Node from the <span style=\" font-style:italic;\">Nodes</span> box. This is your starting point.</p><p>In the <span style=\" font-style:italic;\">Connections</span> box, select a node from the dropdown menu. These are your destinations. This is where you can view what tricks are required on a path from node to node. </p><p>Nodes that are bolded have a path to the selected node.</p><p><span style=\" font-weight:600;\">List of Nodes</span></p><p>These are the relevant locations in a room. These include:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Doors</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Blast Shields</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; "
                        "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Elevators (Prime 1/2)</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Teleporters (Prime 3)</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Portals (Prime 2)</li><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pickups</li></ul><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Events</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Helper Nodes: general nodes that other nodes link up for database simplification)</li></ul><p><span style=\" font-weight:600;\">Node Info<"
                        "/span></p><p>This box tells important information about a specific node.</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Door/Blast Shield/Portal: Mentions what is needed to open it and what room it connects to.</li></ul><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Elevator/Telporter: Mentions what room it connects to.</li></ul><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pickup: Mentions what number it is and if it's a major item or not.</li><li style=\" marg"
                        "in-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Events: Specific one-time events that must be completed in order to progress on certain paths.</li></ul></body></html>", None))
        RandovaniaHelpWidget.setTabText(RandovaniaHelpWidget.indexOf(self.database_viewer_tab), QCoreApplication.translate("RandovaniaHelpWidget", u"Database Viewer", None))
        pass
    # retranslateUi


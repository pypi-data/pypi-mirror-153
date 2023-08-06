# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'echoes_cosmetic_patches_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_EchoesCosmeticPatchesDialog(object):
    def setupUi(self, EchoesCosmeticPatchesDialog):
        if not EchoesCosmeticPatchesDialog.objectName():
            EchoesCosmeticPatchesDialog.setObjectName(u"EchoesCosmeticPatchesDialog")
        EchoesCosmeticPatchesDialog.resize(424, 450)
        self.gridLayout = QGridLayout(EchoesCosmeticPatchesDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(EchoesCosmeticPatchesDialog)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 2, 2, 1, 1)

        self.accept_button = QPushButton(EchoesCosmeticPatchesDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 2, 0, 1, 1)

        self.cancel_button = QPushButton(EchoesCosmeticPatchesDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 2, 1, 1, 1)

        self.scrollArea = QScrollArea(EchoesCosmeticPatchesDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 390, 779))
        self.verticalLayout = QVBoxLayout(self.scroll_area_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.description_label = QLabel(self.scroll_area_contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.game_changes_box = QGroupBox(self.scroll_area_contents)
        self.game_changes_box.setObjectName(u"game_changes_box")
        self.game_changes_layout = QVBoxLayout(self.game_changes_box)
        self.game_changes_layout.setSpacing(6)
        self.game_changes_layout.setContentsMargins(11, 11, 11, 11)
        self.game_changes_layout.setObjectName(u"game_changes_layout")
        self.hud_color_layout = QHBoxLayout()
        self.hud_color_layout.setSpacing(6)
        self.hud_color_layout.setObjectName(u"hud_color_layout")
        self.custom_hud_color = QCheckBox(self.game_changes_box)
        self.custom_hud_color.setObjectName(u"custom_hud_color")

        self.hud_color_layout.addWidget(self.custom_hud_color)

        self.custom_hud_color_button = QPushButton(self.game_changes_box)
        self.custom_hud_color_button.setObjectName(u"custom_hud_color_button")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.custom_hud_color_button.sizePolicy().hasHeightForWidth())
        self.custom_hud_color_button.setSizePolicy(sizePolicy)

        self.hud_color_layout.addWidget(self.custom_hud_color_button)

        self.custom_hud_color_square = QFrame(self.game_changes_box)
        self.custom_hud_color_square.setObjectName(u"custom_hud_color_square")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.custom_hud_color_square.sizePolicy().hasHeightForWidth())
        self.custom_hud_color_square.setSizePolicy(sizePolicy1)
        self.custom_hud_color_square.setMinimumSize(QSize(22, 22))
        self.custom_hud_color_square.setAutoFillBackground(False)
        self.custom_hud_color_square.setFrameShape(QFrame.StyledPanel)
        self.custom_hud_color_square.setFrameShadow(QFrame.Raised)
        self.custom_hud_color_square.setLineWidth(1)

        self.hud_color_layout.addWidget(self.custom_hud_color_square)


        self.game_changes_layout.addLayout(self.hud_color_layout)

        self.faster_credits_check = QCheckBox(self.game_changes_box)
        self.faster_credits_check.setObjectName(u"faster_credits_check")

        self.game_changes_layout.addWidget(self.faster_credits_check)

        self.remove_hud_popup_check = QCheckBox(self.game_changes_box)
        self.remove_hud_popup_check.setObjectName(u"remove_hud_popup_check")

        self.game_changes_layout.addWidget(self.remove_hud_popup_check)

        self.pickup_markers_check = QCheckBox(self.game_changes_box)
        self.pickup_markers_check.setObjectName(u"pickup_markers_check")

        self.game_changes_layout.addWidget(self.pickup_markers_check)

        self.open_map_check = QCheckBox(self.game_changes_box)
        self.open_map_check.setObjectName(u"open_map_check")

        self.game_changes_layout.addWidget(self.open_map_check)

        self.unvisited_room_names_check = QCheckBox(self.game_changes_box)
        self.unvisited_room_names_check.setObjectName(u"unvisited_room_names_check")

        self.game_changes_layout.addWidget(self.unvisited_room_names_check)

        self.elevator_sound_check = QCheckBox(self.game_changes_box)
        self.elevator_sound_check.setObjectName(u"elevator_sound_check")

        self.game_changes_layout.addWidget(self.elevator_sound_check)


        self.verticalLayout.addWidget(self.game_changes_box)

        self.visor_box = QGroupBox(self.scroll_area_contents)
        self.visor_box.setObjectName(u"visor_box")
        self.visor_layout = QGridLayout(self.visor_box)
        self.visor_layout.setSpacing(6)
        self.visor_layout.setContentsMargins(11, 11, 11, 11)
        self.visor_layout.setObjectName(u"visor_layout")
        self.hud_lag_check = QCheckBox(self.visor_box)
        self.hud_lag_check.setObjectName(u"hud_lag_check")

        self.visor_layout.addWidget(self.hud_lag_check, 3, 0, 1, 2)

        self.hud_alpha_label = QLabel(self.visor_box)
        self.hud_alpha_label.setObjectName(u"hud_alpha_label")

        self.visor_layout.addWidget(self.hud_alpha_label, 0, 0, 1, 1)

        self.helmet_alpha_slider = QSlider(self.visor_box)
        self.helmet_alpha_slider.setObjectName(u"helmet_alpha_slider")
        self.helmet_alpha_slider.setOrientation(Qt.Horizontal)
        self.helmet_alpha_slider.setTickPosition(QSlider.TicksBelow)

        self.visor_layout.addWidget(self.helmet_alpha_slider, 1, 1, 1, 1)

        self.hud_alpha_value_label = QLabel(self.visor_box)
        self.hud_alpha_value_label.setObjectName(u"hud_alpha_value_label")

        self.visor_layout.addWidget(self.hud_alpha_value_label, 0, 2, 1, 1)

        self.helmet_alpha_label = QLabel(self.visor_box)
        self.helmet_alpha_label.setObjectName(u"helmet_alpha_label")

        self.visor_layout.addWidget(self.helmet_alpha_label, 1, 0, 1, 1)

        self.helmet_alpha_value_label = QLabel(self.visor_box)
        self.helmet_alpha_value_label.setObjectName(u"helmet_alpha_value_label")

        self.visor_layout.addWidget(self.helmet_alpha_value_label, 1, 2, 1, 1)

        self.hud_alpha_slider = QSlider(self.visor_box)
        self.hud_alpha_slider.setObjectName(u"hud_alpha_slider")
        self.hud_alpha_slider.setOrientation(Qt.Horizontal)
        self.hud_alpha_slider.setTickPosition(QSlider.TicksBelow)

        self.visor_layout.addWidget(self.hud_alpha_slider, 0, 1, 1, 1)

        self.checkBox = QCheckBox(self.visor_box)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setEnabled(False)

        self.visor_layout.addWidget(self.checkBox, 4, 0, 1, 2)


        self.verticalLayout.addWidget(self.visor_box)

        self.controls_box = QGroupBox(self.scroll_area_contents)
        self.controls_box.setObjectName(u"controls_box")
        self.controls_layout = QGridLayout(self.controls_box)
        self.controls_layout.setSpacing(6)
        self.controls_layout.setContentsMargins(11, 11, 11, 11)
        self.controls_layout.setObjectName(u"controls_layout")
        self.invert_y_axis_check = QCheckBox(self.controls_box)
        self.invert_y_axis_check.setObjectName(u"invert_y_axis_check")

        self.controls_layout.addWidget(self.invert_y_axis_check, 0, 0, 1, 1)

        self.rumble_check = QCheckBox(self.controls_box)
        self.rumble_check.setObjectName(u"rumble_check")

        self.controls_layout.addWidget(self.rumble_check, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.controls_box)

        self.audio_box = QGroupBox(self.scroll_area_contents)
        self.audio_box.setObjectName(u"audio_box")
        self.audio_layout = QGridLayout(self.audio_box)
        self.audio_layout.setSpacing(6)
        self.audio_layout.setContentsMargins(11, 11, 11, 11)
        self.audio_layout.setObjectName(u"audio_layout")
        self.sound_mode_label = QLabel(self.audio_box)
        self.sound_mode_label.setObjectName(u"sound_mode_label")
        self.sound_mode_label.setMaximumSize(QSize(16777215, 20))

        self.audio_layout.addWidget(self.sound_mode_label, 0, 0, 1, 1)

        self.sfx_volume_label = QLabel(self.audio_box)
        self.sfx_volume_label.setObjectName(u"sfx_volume_label")

        self.audio_layout.addWidget(self.sfx_volume_label, 1, 0, 1, 1)

        self.music_volume_label = QLabel(self.audio_box)
        self.music_volume_label.setObjectName(u"music_volume_label")

        self.audio_layout.addWidget(self.music_volume_label, 2, 0, 1, 1)

        self.sound_mode_combo = QComboBox(self.audio_box)
        self.sound_mode_combo.setObjectName(u"sound_mode_combo")

        self.audio_layout.addWidget(self.sound_mode_combo, 0, 1, 1, 1)

        self.sfx_volume_slider = QSlider(self.audio_box)
        self.sfx_volume_slider.setObjectName(u"sfx_volume_slider")
        self.sfx_volume_slider.setOrientation(Qt.Horizontal)
        self.sfx_volume_slider.setTickPosition(QSlider.TicksBelow)

        self.audio_layout.addWidget(self.sfx_volume_slider, 1, 1, 1, 1)

        self.music_volume_slider = QSlider(self.audio_box)
        self.music_volume_slider.setObjectName(u"music_volume_slider")
        self.music_volume_slider.setOrientation(Qt.Horizontal)
        self.music_volume_slider.setTickPosition(QSlider.TicksBelow)

        self.audio_layout.addWidget(self.music_volume_slider, 2, 1, 1, 1)

        self.sfx_volume_value_label = QLabel(self.audio_box)
        self.sfx_volume_value_label.setObjectName(u"sfx_volume_value_label")

        self.audio_layout.addWidget(self.sfx_volume_value_label, 1, 2, 1, 1)

        self.music_volume_value_label = QLabel(self.audio_box)
        self.music_volume_value_label.setObjectName(u"music_volume_value_label")

        self.audio_layout.addWidget(self.music_volume_value_label, 2, 2, 1, 1)


        self.verticalLayout.addWidget(self.audio_box)

        self.screen_box = QGroupBox(self.scroll_area_contents)
        self.screen_box.setObjectName(u"screen_box")
        self.screen_layout = QGridLayout(self.screen_box)
        self.screen_layout.setSpacing(6)
        self.screen_layout.setContentsMargins(11, 11, 11, 11)
        self.screen_layout.setObjectName(u"screen_layout")
        self.screen_brightness_label = QLabel(self.screen_box)
        self.screen_brightness_label.setObjectName(u"screen_brightness_label")

        self.screen_layout.addWidget(self.screen_brightness_label, 0, 0, 1, 1)

        self.screen_x_offset_label = QLabel(self.screen_box)
        self.screen_x_offset_label.setObjectName(u"screen_x_offset_label")

        self.screen_layout.addWidget(self.screen_x_offset_label, 1, 0, 1, 1)

        self.screen_brightness_slider = QSlider(self.screen_box)
        self.screen_brightness_slider.setObjectName(u"screen_brightness_slider")
        self.screen_brightness_slider.setOrientation(Qt.Horizontal)
        self.screen_brightness_slider.setTickPosition(QSlider.TicksBelow)

        self.screen_layout.addWidget(self.screen_brightness_slider, 0, 1, 1, 1)

        self.screen_y_offset_slider = QSlider(self.screen_box)
        self.screen_y_offset_slider.setObjectName(u"screen_y_offset_slider")
        self.screen_y_offset_slider.setOrientation(Qt.Horizontal)
        self.screen_y_offset_slider.setTickPosition(QSlider.TicksBelow)

        self.screen_layout.addWidget(self.screen_y_offset_slider, 2, 1, 1, 1)

        self.screen_stretch_label = QLabel(self.screen_box)
        self.screen_stretch_label.setObjectName(u"screen_stretch_label")

        self.screen_layout.addWidget(self.screen_stretch_label, 3, 0, 1, 1)

        self.screen_x_offset_slider = QSlider(self.screen_box)
        self.screen_x_offset_slider.setObjectName(u"screen_x_offset_slider")
        self.screen_x_offset_slider.setOrientation(Qt.Horizontal)
        self.screen_x_offset_slider.setTickPosition(QSlider.TicksBelow)

        self.screen_layout.addWidget(self.screen_x_offset_slider, 1, 1, 1, 1)

        self.screen_stretch_slider = QSlider(self.screen_box)
        self.screen_stretch_slider.setObjectName(u"screen_stretch_slider")
        self.screen_stretch_slider.setOrientation(Qt.Horizontal)
        self.screen_stretch_slider.setTickPosition(QSlider.TicksBelow)

        self.screen_layout.addWidget(self.screen_stretch_slider, 3, 1, 1, 1)

        self.screen_y_offset_label = QLabel(self.screen_box)
        self.screen_y_offset_label.setObjectName(u"screen_y_offset_label")

        self.screen_layout.addWidget(self.screen_y_offset_label, 2, 0, 1, 1)

        self.screen_brightness_value_label = QLabel(self.screen_box)
        self.screen_brightness_value_label.setObjectName(u"screen_brightness_value_label")

        self.screen_layout.addWidget(self.screen_brightness_value_label, 0, 2, 1, 1)

        self.screen_x_offset_value_label = QLabel(self.screen_box)
        self.screen_x_offset_value_label.setObjectName(u"screen_x_offset_value_label")

        self.screen_layout.addWidget(self.screen_x_offset_value_label, 1, 2, 1, 1)

        self.screen_y_offset_value_label = QLabel(self.screen_box)
        self.screen_y_offset_value_label.setObjectName(u"screen_y_offset_value_label")

        self.screen_layout.addWidget(self.screen_y_offset_value_label, 2, 2, 1, 1)

        self.screen_stretch_value_label = QLabel(self.screen_box)
        self.screen_stretch_value_label.setObjectName(u"screen_stretch_value_label")

        self.screen_layout.addWidget(self.screen_stretch_value_label, 3, 2, 1, 1)


        self.verticalLayout.addWidget(self.screen_box)

        self.scrollArea.setWidget(self.scroll_area_contents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)


        self.retranslateUi(EchoesCosmeticPatchesDialog)

        QMetaObject.connectSlotsByName(EchoesCosmeticPatchesDialog)
    # setupUi

    def retranslateUi(self, EchoesCosmeticPatchesDialog):
        EchoesCosmeticPatchesDialog.setWindowTitle(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Metroid Prime 2 - Cosmetic Options", None))
        self.reset_button.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Reset to Defaults", None))
        self.accept_button.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Cancel", None))
        self.description_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"<html><head/><body><p>What you choose here will be used as the default values for the in-game options.</p></body></html>", None))
        self.game_changes_box.setTitle(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Game Changes", None))
        self.custom_hud_color.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Use a custom HUD color", None))
        self.custom_hud_color_button.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Set Color...", None))
        self.faster_credits_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Faster Credits", None))
        self.remove_hud_popup_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Skip Item Acquisition Popups", None))
        self.pickup_markers_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Replace Translator icons on map with item icons", None))
        self.open_map_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Open map from start", None))
        self.unvisited_room_names_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Always display room names on map", None))
#if QT_CONFIG(tooltip)
        self.elevator_sound_check.setToolTip(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"<html><head/><body><p>The sound effect is always kept when elevators are vanilla.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.elevator_sound_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Keep Elevator/Teleporter transition sound effect", None))
        self.visor_box.setTitle(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Visor", None))
        self.hud_lag_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Hud Lag", None))
        self.hud_alpha_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Visor Opacity", None))
        self.hud_alpha_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
        self.helmet_alpha_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Helmet Opacity", None))
        self.helmet_alpha_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.checkBox.setToolTip(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"<html><head/><body><p>The in-game Hint System has been removed. The option for it remains, but does nothing.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Hint System", None))
        self.controls_box.setTitle(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Controls", None))
        self.invert_y_axis_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Invert Y Axis", None))
        self.rumble_check.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Rumble", None))
        self.audio_box.setTitle(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Audio", None))
        self.sound_mode_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Sound Mode", None))
        self.sfx_volume_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Sound Volume", None))
        self.music_volume_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Music Volume", None))
        self.sfx_volume_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
        self.music_volume_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
        self.screen_box.setTitle(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Screen", None))
        self.screen_brightness_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Screen Brightness", None))
        self.screen_x_offset_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Screen X Offset", None))
        self.screen_stretch_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Screen Stretch", None))
        self.screen_y_offset_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"Screen Y Offset", None))
        self.screen_brightness_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
        self.screen_x_offset_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
        self.screen_y_offset_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
        self.screen_stretch_value_label.setText(QCoreApplication.translate("EchoesCosmeticPatchesDialog", u"TextLabel", None))
    # retranslateUi


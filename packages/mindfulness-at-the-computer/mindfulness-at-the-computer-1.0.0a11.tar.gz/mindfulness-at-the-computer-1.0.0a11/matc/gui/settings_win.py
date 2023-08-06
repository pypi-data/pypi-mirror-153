import logging
import enum
import sys
import webbrowser
import os.path
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
import matc.constants
import matc.globa
import matc.settings
import matc.gui.intro_dlg
import matc.gui.breathing_dlg
# import matc.gui.breathing_phrase_list_wt

NEW_ROW: int = -1


class SysinfoDialog(QtWidgets.QDialog):
    def __init__(self, i_parent=None):
        super().__init__(i_parent)
        self.setModal(True)

        vbox_l2 = QtWidgets.QVBoxLayout(self)

        self._system_info_str = '\n'.join([
            descr_str + ": " + str(value) for (descr_str, value) in matc.globa.sys_info_telist
        ])

        self.system_info_qll = QtWidgets.QLabel(self._system_info_str)
        vbox_l2.addWidget(self.system_info_qll)

        self.copy_qpb = QtWidgets.QPushButton(self.tr("Copy to clipboard"))
        self.copy_qpb.clicked.connect(self.on_copy_button_clicked)
        vbox_l2.addWidget(self.copy_qpb)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtCore.Qt.Horizontal,
            self
        )
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)

        vbox_l2.addWidget(self.button_box)
        self.button_box.rejected.connect(self.reject)
        # -accepted and rejected are "slots" built into Qt

    def on_copy_button_clicked(self):
        qclipboard = QtGui.QGuiApplication.clipboard()
        qclipboard.setText(self._system_info_str)
        # -this will copy the text to the system clipboard


class FeedbackDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.gui_update_bool = True

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        help_request_str = """<h3>Help Us</h3>
<p>We are grateful for feedback, for example please contact us if you</p>
<ul>
<li>find a bug</li>
<li>have a suggestion for a new feature</li>
<li>have ideas for how to improve the interface</li>
<li>have feedback about what you like about the application and how it helps you when using the computer (we are looking for testimonials!)</li>
</ul>
<p>You can reach us using this email address:</p>"""

        help_request_qll = QtWidgets.QLabel()
        # help_request_qll.setFont(matc.globa.get_font_large())
        help_request_qll.setText(help_request_str)
        help_request_qll.setWordWrap(True)
        vbox_l2.addWidget(help_request_qll)

        email_qll = QtWidgets.QLabel()
        email_qll.setFont(matc.globa.get_font(matc.globa.FontSize.xxlarge))
        email_qll.setText('sunyata.software@gmail.com')
        vbox_l2.addWidget(email_qll)

        emailus_qpb = QtWidgets.QPushButton("Email us!")
        emailus_qpb.clicked.connect(self.on_emailus_clicked)
        vbox_l2.addWidget(emailus_qpb)

        self.show()

    def on_emailus_clicked(self):
        url_string = "mailto:sunyata.software@gmail.com?subject=Feedback"
        webbrowser.open(url_string)
        # Alt: QtGui.QDesktopServices.openUrl(QtCore.QUrl(url_string))


class ToggleSwitchWt(QtWidgets.QWidget):
    toggled_signal = QtCore.Signal(bool)

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.turn_on_off_qcb = QtWidgets.QCheckBox()
        self.turn_on_off_qcb.toggled.connect(self._on_toggled)
        on_off_qhl = QtWidgets.QHBoxLayout()
        on_off_qhl.setContentsMargins(0, 0, 0, 0)
        on_off_qhl.addWidget(QtWidgets.QLabel(self.tr("Turn the dialog and notifications on or off")))
        on_off_qhl.addStretch(1)
        on_off_qhl.addWidget(self.turn_on_off_qcb)
        self.setLayout(on_off_qhl)

    def _on_toggled(self, i_checked: bool):
        if self.updating_gui_bool:
            return
        self.toggled_signal.emit(i_checked)

    def update_gui(self, i_checked: bool):
        self.updating_gui_bool = True

        self.turn_on_off_qcb.setChecked(i_checked)

        self.updating_gui_bool = False


class MoveDirectionEnum(enum.Enum):
    up = 1
    down = 2


class BreathingPhraseEditDialog(QtWidgets.QDialog):
    def __init__(self, i_id: int, i_parent=None):
        super().__init__(parent=i_parent)
        self.setModal(True)
        self.setMinimumWidth(250)
        vbox = QtWidgets.QVBoxLayout(self)

        """
        # If a phrase is not selected, default to phrase with id 1
        if matc.globa.active_phrase_id_it == matc.globa.NO_PHRASE_SELECTED_INT:
            matc.globa.active_phrase_id_it = 1
        """

        bp_obj = matc.settings.get_breathing_phrase(i_id)

        self.breath_title_qle = QtWidgets.QLineEdit(str(bp_obj.id))
        vbox.addWidget(QtWidgets.QLabel(self.tr("ID")))
        vbox.addWidget(self.breath_title_qle)

        vbox.addWidget(QtWidgets.QLabel(self.tr("Phrase")))
        self.in_breath_phrase_qle = QtWidgets.QLineEdit(bp_obj.in_breath)
        vbox.addWidget(self.in_breath_phrase_qle)

        self.out_breath_phrase_qle = QtWidgets.QLineEdit(bp_obj.out_breath)
        vbox.addWidget(self.out_breath_phrase_qle)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

        self.adjustSize()

    @staticmethod
    def start(i_id) -> bool:
        dlg = BreathingPhraseEditDialog(i_id)
        dlg.exec()

        if dlg.result() == QtWidgets.QDialog.Accepted:
            logging.debug("dlg.result() == QtWidgets.QDialog.Accepted")
            bp_obj = matc.settings.get_breathing_phrase(i_id)
            bp_obj.in_breath = dlg.in_breath_phrase_qle.text()
            bp_obj.out_breath = dlg.out_breath_phrase_qle.text()
            return True
        return False


class MyListWidget(QtWidgets.QListWidget):
    drop_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

    def dropEvent(self, QDropEvent):
        super().dropEvent(QDropEvent)
        self.drop_signal.emit()
        # self.update_db_sort_order_for_all_rows()


class SettingsWin(QtWidgets.QMainWindow):
    show_intro_dialog_signal = QtCore.Signal()
    br_timer_change_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 64, 400, 540)
        self.setWindowTitle(f"Settings Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.globa.get_app_icon_path("icon.png")))

        self.updating_gui: bool = True
        self.widget_w1 = QtWidgets.QWidget()
        self.seconds_for_br_timer_action = None

        """
        if matc.globa.testing_bool:
            data_storage_str = "{Testing - data stored in memory}"
        else:
            data_storage_str = "{Live - data stored on hard drive}"
        window_title_str = (
                matc.constants.APPLICATION_PRETTY_NAME
                + " [" + matc.constants.APPLICATION_VERSION + "] "
                + data_storage_str
        )
        self.setWindowTitle(window_title_str)
        """

        self.setStyleSheet(
            "selection-background-color:" + matc.globa.LIGHT_GREEN_COLOR + ";"
            "selection-color:#000000;"
        )

        self.setCentralWidget(self.widget_w1)

        # Setup of Menu
        self.menu_bar = self.menuBar()
        self.update_menu()


        hbox_l2 = QtWidgets.QHBoxLayout()
        self.widget_w1.setLayout(hbox_l2)

        vbox_l2 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(vbox_l2)

        hbox_br_time_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_br_time_l3)
        hbox_br_time_l3.addWidget(QtWidgets.QLabel("Breathing break time"))
        self.breathing_break_time_qsb = QtWidgets.QSpinBox()
        self.breathing_break_time_qsb.setMinimum(1)
        self.breathing_break_time_qsb.setMaximum(1000)
        hbox_br_time_l3.addWidget(self.breathing_break_time_qsb)
        self.breathing_break_time_qsb.valueChanged.connect(self.on_br_time_value_changed)
        hbox_br_time_l3.addWidget(QtWidgets.QLabel("minutes"))

        hbox_volume_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_volume_l3)
        hbox_volume_l3.addWidget(QtWidgets.QLabel("Volume"))
        self.volume_qsr = QtWidgets.QSlider()
        hbox_volume_l3.addWidget(self.volume_qsr)
        self.volume_qsr.valueChanged.connect(self.on_volume_changed)
        self.volume_qsr.setMinimum(0)
        self.volume_qsr.setMaximum(100)
        self.volume_qsr.setOrientation(QtCore.Qt.Horizontal)

        self.phrases_qgb = QtWidgets.QGroupBox("Breathing phrases")
        vbox_l2.addWidget(self.phrases_qgb)
        vbox_l4 = QtWidgets.QVBoxLayout()
        self.phrases_qgb.setLayout(vbox_l4)

        self.edit_bp_qpb = QtWidgets.QPushButton("Edit")

        self.breathing_phrases_qlw = MyListWidget()
        vbox_l4.addWidget(self.breathing_phrases_qlw)
        self.breathing_phrases_qlw.setSpacing(2)
        self.breathing_phrases_qlw.currentRowChanged.connect(self.on_bp_current_row_changed)
        self.breathing_phrases_qlw.itemDoubleClicked.connect(self.on_bp_double_clicked)
        self.breathing_phrases_qlw.drop_signal.connect(self.on_bp_item_dropped)
        self.populate_bp_list()

        hbox_buttons_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_buttons_l5)

        hbox_buttons_l5.addWidget(self.edit_bp_qpb)
        self.edit_bp_qpb.clicked.connect(self.on_edit_bp_clicked)

        self.add_bp_qpb = QtWidgets.QPushButton("Add")
        hbox_buttons_l5.addWidget(self.add_bp_qpb)
        self.add_bp_qpb.clicked.connect(self.on_add_bp_clicked)

        self.del_bp_qpb = QtWidgets.QPushButton("Del")
        hbox_buttons_l5.addWidget(self.del_bp_qpb)
        self.del_bp_qpb.clicked.connect(self.on_del_bp_clicked)

        self.set_active_bp_qpb = QtWidgets.QPushButton("Set Active")
        hbox_buttons_l5.addWidget(self.set_active_bp_qpb)
        self.set_active_bp_qpb.clicked.connect(self.on_set_active_bp_clicked)


        """
        for i in preview_bm_dict:
            bm = preview_bm_dict[i]
            rendered_qll = QtWidgets.QLabel()
            rendered_qll.setPixmap(bm)
            vbox_l2.addWidget(rendered_qll)
        """

        self.visualizations_qgb = QtWidgets.QGroupBox("Breathing visualizations")
        hbox_l2.addWidget(self.visualizations_qgb)
        grid_l4 = QtWidgets.QGridLayout()
        vbox_l4 = QtWidgets.QVBoxLayout()
        self.visualizations_qgb.setLayout(grid_l4)
        self.br_vis_group_qbg = QtWidgets.QButtonGroup()

        preview_bm_dict = matc.gui.breathing_dlg.BreathingGraphicsView.get_preview_bitmaps()
        for item in matc.globa.BreathingVisalization:
            br_vis_bar_qrb = QtWidgets.QRadioButton(item.name.capitalize())
            value = item.value
            self.br_vis_group_qbg.addButton(br_vis_bar_qrb, value)
            new_font=br_vis_bar_qrb.font()
            new_font.setPointSize(new_font.pointSize()+2)
            br_vis_bar_qrb.setFont(new_font)
            preview_qll = Label()
            preview_qll.setPixmap(preview_bm_dict[value])
            preview_qll.mouse_press_signal.connect(br_vis_bar_qrb.click)
            composite_widget = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout()
            composite_widget.setLayout(vbox)
            vbox.addWidget(br_vis_bar_qrb)
            vbox.addWidget(preview_qll)
            grid_l4.addWidget(composite_widget, value // 2, value % 2)

        """
        self.br_vis_bar_qrb = QtWidgets.QRadioButton("Bar")
        self.br_vis_group_qbg.addButton(self.br_vis_bar_qrb, matc.globa.BreathingVisalization.bar.value)
        vbox_l4.addWidget(self.br_vis_bar_qrb)
        self.bar_preview_qll = QtWidgets.QLabel()
        self.bar_preview_qll.setPixmap(preview_bm_dict[matc.globa.BreathingVisalization.bar.value])
        vbox_l4.addWidget(self.bar_preview_qll)

        self.br_vis_circle_qrb = QtWidgets.QRadioButton("Circle")
        self.br_vis_group_qbg.addButton(self.br_vis_circle_qrb, matc.globa.BreathingVisalization.circle.value)
        vbox_l4.addWidget(self.br_vis_circle_qrb)

        self.br_vis_line_qrb = QtWidgets.QRadioButton("Line")
        self.br_vis_group_qbg.addButton(self.br_vis_line_qrb, matc.globa.BreathingVisalization.line.value)
        vbox_l4.addWidget(self.br_vis_line_qrb)

        self.br_vis_cols_qrb = QtWidgets.QRadioButton("Columns (includes history)")
        self.br_vis_group_qbg.addButton(self.br_vis_cols_qrb, matc.globa.BreathingVisalization.columns.value)
        vbox_l4.addWidget(self.br_vis_cols_qrb)
        """
        self.br_vis_group_qbg.idClicked.connect(self.on_br_vis_id_clicked)


        self.move_mouse_cursor_qcb = QtWidgets.QCheckBox("Move mouse cursor to breathing dialog")
        vbox_l2.addWidget(self.move_mouse_cursor_qcb)
        self.move_mouse_cursor_qcb.clicked.connect(self.on_move_mouse_cursor_clicked)
        self.move_mouse_cursor_qcb.setToolTip("Useful if you are using a touchpad")

        ######## self.show_breathing_phrase_qcb = QtWidgets.QCheckBox("Show breahing phrase")
        ######## vbox_l4.addWidget(self.show_breathing_phrase_qcb)
        ######## self.show_breathing_phrase_qcb.toggled.connect(self.on_show_br_phrase_toggled)

        # matc.globa.active_phrase_id_it

        self.update_gui()

    def populate_bp_list(self):
        self.breathing_phrases_qlw.clear()
        phrases: list[matc.settings.BreathingPhrase] = matc.settings.settings[matc.settings.SK_BREATHING_PHRASES]
        for p in phrases:
            self._add_bp_to_gui(p.id)

    def on_bp_item_dropped(self):
        new_order_phrase_list = []
        for item_row in range(self.breathing_phrases_qlw.count()):
            item = self.breathing_phrases_qlw.item(item_row)
            item_id = item.data(QtCore.Qt.UserRole)
            phrase = matc.settings.get_breathing_phrase(item_id)
            new_order_phrase_list.append(phrase)
        matc.settings.settings[matc.settings.SK_BREATHING_PHRASES] = new_order_phrase_list
        # self.populate_bp_list()

    def on_bp_double_clicked(self, i_item: QtWidgets.QListWidgetItem):
        matc.globa.active_phrase_id = i_item.data(QtCore.Qt.UserRole)
        self.update_gui_active_bold()

    def on_move_mouse_cursor_clicked(self, i_checked: bool):
        if self.updating_gui:
            return
        matc.settings.settings[matc.settings.SK_MOVE_MOUSE_CURSOR] = i_checked

    def on_br_vis_id_clicked(self, i_id: int):
        if self.updating_gui:
            return
        matc.settings.settings[matc.settings.SK_BREATHING_VISUALIZATION] = i_id

    def on_bp_current_row_changed(self):
        pass

    def on_show_br_phrase_toggled(self, i_checked: bool):
        logging.debug("on_show_br_phrase_toggled")
        if i_checked:
            top_qlwi = self.breathing_phrases_qlw.item(0)
            matc.globa.active_phrase_id = top_qlwi.data(QtCore.Qt.UserRole)
        else:
            matc.globa.active_phrase_id = matc.globa.BREATHING_PHRASE_NOT_SET
        self.update_gui_active_bold()

    def on_set_active_bp_clicked(self):
        current_qlwi = self.breathing_phrases_qlw.currentItem()
        matc.globa.active_phrase_id = current_qlwi.data(QtCore.Qt.UserRole)
        self.update_gui_active_bold()

    def update_gui_active_bold(self):
        for item_row in range(self.breathing_phrases_qlw.count()):
            item = self.breathing_phrases_qlw.item(item_row)
            item_font = item.font()
            if item.data(QtCore.Qt.UserRole) == matc.globa.active_phrase_id:
                item_font.setBold(True)
                item.setFont(item_font)
            elif item_font.bold():
                item_font.setBold(False)
                item.setFont(item_font)
            """
            self.show_breathing_phrase_qcb.setChecked(
                matc.globa.active_phrase_id != matc.globa.BREATHING_PHRASE_NOT_SHOWN
            )
            """

    def on_volume_changed(self, i_new_value: int):
        if self.updating_gui:
            return
        matc.settings.settings[matc.settings.SK_BREATHING_AUDIO_VOLUME] = i_new_value

    def on_add_bp_clicked(self):
        new_id: int = matc.settings.add_breathing_phrase("ib", "ob")
        result = BreathingPhraseEditDialog.start(new_id)
        if result:
            self._add_bp_to_gui(new_id)

    def _update_bp_in_gui(self, i_id: int, i_row: int):
        phrase = matc.settings.get_breathing_phrase(i_id)
        phrase_text: str = f"{phrase.in_breath}\n{phrase.out_breath}"

        qlwi = QtWidgets.QListWidgetItem(phrase_text)
        self.breathing_phrases_qlw.takeItem(i_row)
        self.breathing_phrases_qlw.insertItem(i_row, qlwi)
        self.breathing_phrases_qlw.setCurrentRow(i_row)

    def _add_bp_to_gui(self, i_id: int, i_row: int = NEW_ROW):
        if i_id == matc.globa.BREATHING_PHRASE_NOT_SET:
            phrase_text: str = "nothing"
            raise Exception("BREATHING_PHRASE_NOT_SET --- this should not be possible")
        else:
            phrase = matc.settings.get_breathing_phrase(i_id)
            phrase_text: str = f"{phrase.in_breath}\n{phrase.out_breath}"
        qlwi = QtWidgets.QListWidgetItem(phrase_text)
        if i_id == matc.globa.BREATHING_PHRASE_NOT_SET:
            new_font = qlwi.font()
            new_font.setItalic(True)
            qlwi.setFont(new_font)
        qlwi.setData(QtCore.Qt.UserRole, i_id)
        if i_row == NEW_ROW:
            self.breathing_phrases_qlw.addItem(qlwi)
            new_row: int = self.breathing_phrases_qlw.count() - 1
            self.breathing_phrases_qlw.setCurrentRow(new_row)
        else:
            self.breathing_phrases_qlw.insertItem(i_row, qlwi)
            self.breathing_phrases_qlw.setCurrentRow(i_row)

    def on_del_bp_clicked(self):
        if self.breathing_phrases_qlw.count() == 0:
            QtWidgets.QMessageBox.information(self, "Cannot remove last item",
               "It's not possible to remove the last item")
            return

        current_item = self.breathing_phrases_qlw.currentItem()
        current_row: int = self.breathing_phrases_qlw.currentRow()
        id_: int = current_item.data(QtCore.Qt.UserRole)

        if matc.globa.active_phrase_id == id_:
            QtWidgets.QMessageBox.information(self, "Cannot remove active item",
               "It's not possible to remove the active item. Please switch to another item before removing this one")
            return

        standard_button = QtWidgets.QMessageBox.question(self, "Removing br phrase",
            f"Are you sure you want to remove this item:\n\n{current_item.text()}")
        if standard_button == QtWidgets.QMessageBox.Yes:
            matc.settings.remove_breathing_phrase(id_)
            self.breathing_phrases_qlw.takeItem(current_row)

    def on_edit_bp_clicked(self):
        # bp_edit_dlg = BreathingPhraseEditDialog()
        # bp_edit_dlg.start()
        current_item = self.breathing_phrases_qlw.currentItem()
        current_row: int = self.breathing_phrases_qlw.currentRow()
        id_: int = current_item.data(QtCore.Qt.UserRole)

        result = BreathingPhraseEditDialog.start(id_)
        if result:
            self._update_bp_in_gui(id_, current_row)

        # qlwi = self.breathing_phrases_qlw.takeItem(current_row)
        # self._add_bp_to_gui(id_, current_row)
        # matc.globa.active_phrase_id_it

    def on_br_time_value_changed(self, i_new_value: int):
        if self.updating_gui:
            return
        matc.settings.settings[matc.settings.SK_BREATHING_BREAK_TIMER_SECS] = 60 * i_new_value
        self.br_timer_change_signal.emit()

    def update_menu(self):
        self.menu_bar.clear()

        file_menu = self.menu_bar.addMenu(self.tr("&File"))
        minimize_to_tray_action = QtGui.QAction(self.tr("Minimize to tray"), self)
        file_menu.addAction(minimize_to_tray_action)
        minimize_to_tray_action.triggered.connect(self.minimize_to_tray)
        save_action = QtGui.QAction(self.tr("Save"), self)
        file_menu.addAction(save_action)
        save_action.triggered.connect(matc.settings.save_settings_to_json_file)
        """
        choose_file_directory_action = QtGui.QAction(self.tr("Choose file directory"), self)
        file_menu.addAction(choose_file_directory_action)
        choose_file_directory_action.triggered.connect(pass)
        """
        quit_action = QtGui.QAction("Quit application", self)
        file_menu.addAction(quit_action)
        quit_action.triggered.connect(self.exit_application)

        close_settings_action = QtGui.QAction("Close settings", self)
        file_menu.addAction(close_settings_action)
        close_settings_action.triggered.connect(self.close)

        debug_menu = self.menu_bar.addMenu("&Debug")
        update_gui_action = QtGui.QAction("Update settings GUI", self)
        debug_menu.addAction(update_gui_action)
        update_gui_action.triggered.connect(self.update_gui)
        self.open_settings_dir_action = QtGui.QAction("Open settings dir", self)
        debug_menu.addAction(self.open_settings_dir_action)
        self.open_settings_dir_action.triggered.connect(self.on_open_settings_dir_triggered)

        help_menu = self.menu_bar.addMenu(self.tr("&Help"))
        show_intro_dialog_action = QtGui.QAction("Show intro wizard", self)
        help_menu.addAction(show_intro_dialog_action)
        show_intro_dialog_action.triggered.connect(self.show_intro_dialog)
        about_action = QtGui.QAction(self.tr("About"), self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.show_about_box)
        online_help_action = QtGui.QAction(self.tr("Online help"), self)
        help_menu.addAction(online_help_action)
        online_help_action.triggered.connect(self.show_online_help)
        feedback_action = QtGui.QAction(self.tr("Give feedback"), self)
        help_menu.addAction(feedback_action)
        feedback_action.triggered.connect(self.show_feedback_dialog)
        sysinfo_action = QtGui.QAction(self.tr("System Information"), self)
        help_menu.addAction(sysinfo_action)
        sysinfo_action.triggered.connect(self.show_sysinfo_box)

    def on_open_settings_dir_triggered(self):
        config_path: str = matc.globa.get_config_path()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(config_path))

    def show_intro_dialog(self):
        self.show_intro_dialog_signal.emit()

    def show_feedback_dialog(self):
        feedback_dlg = FeedbackDialog()
        feedback_dlg.exec_()

    def on_breathing_notification_breathe_clicked(self):
        self.open_breathing_dialog(i_mute_override=True)

    def debug_clear_breathing_phrase_selection(self):
        self.br_phrase_list_wt.list_widget.clearSelection()

    def show_online_help(self):
        url_str = "https://mindfulness-at-the-computer.gitlab.io/user_guide"
        # noinspection PyCallByClass
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url_str))
        # Python: webbrowser.get(url_str) --- doesn't work

    def show_sysinfo_box(self):
        self._sysinfo_dlg = SysinfoDialog()
        self._sysinfo_dlg.show()

    def show_about_box(self):
        founded_by_str = (
            '<p>Project started and maintained by Tord Dellsén - '
            '<a href="https://sunyatazero.gitlab.io/">Website</a></p>'
        )
        designers_str = (
            '<p>Tord Dellsén - <a href="https://sunyatazero.gitlab.io/">Website</a></p>'
            '<p>Shweta Singh Lodhi - <a href="https://www.linkedin.com/in/lodhishweta">LinkedIn</a></p>'
            '<p>We have also been helped by feedback from our users</p>'
        )
        programmers_str = (
            '<p>Programmers: <a href="https://gitlab.com/mindfulness-at-the-computer/mindfulness-at-the-computer/graphs/master">'
            'All contributors</a></p>'
        )
        artists_str = (
            '<p>Photography for application icon by Torgny Dellsén - '
            '<a href="https://torgnydellsen.zenfolio.com">torgnydellsen.zenfolio.com</a></p>'
            '<p>Other icons from Open Iconic - MIT license - <a href="https://useiconic.com">useiconic.com</a></p>'
            '<p>Application logo by Yu Zhou (layout modified by Tord Dellsén)'
            '<p>All audio files used have been released into the public domain (CC0)</p>'
        )
        license_str = (
            '<p>Software License: GPLv3</p>'
        )
        # TODO: Link to LICENSE.txt so the user can view it in a popup dialog
        # Please note that this file may be in different places depending on if we have a pip installation or if we are
        # running from a pyinstaller build
        about_html_str = (
            '<html>'
            + founded_by_str
            + designers_str
            + programmers_str
            + artists_str
            + license_str
            + '</html>'
        )

        # noinspection PyCallByClass
        QtWidgets.QMessageBox.about(self, "About Mindfulness at the Computer", about_html_str)

    # noinspection PyPep8Naming
    def closeEvent(self, i_QCloseEvent):
        matc.settings.save_settings_to_json_file()
        i_QCloseEvent.ignore()
        self.minimize_to_tray()

    def minimize_to_tray(self):
        self.showMinimized()
        self.hide()

    def exit_application(self):
        QtWidgets.QApplication.quit()
        # sys.exit()

    def update_gui(self):
        self.updating_gui = True

        br_time_value: int = matc.settings.settings[matc.settings.SK_BREATHING_BREAK_TIMER_SECS]
        self.breathing_break_time_qsb.setValue(br_time_value // 60)

        volume: int = matc.settings.settings[matc.settings.SK_BREATHING_AUDIO_VOLUME]
        self.volume_qsr.setValue(volume)

        self.update_gui_active_bold()

        active_br_vis_id: int = matc.settings.settings[matc.settings.SK_BREATHING_VISUALIZATION]
        for btn in self.br_vis_group_qbg.buttons():
            if self.br_vis_group_qbg.id(btn) == active_br_vis_id:
                btn.click()

        move_mouse_cursor: bool = matc.settings.settings[matc.settings.SK_MOVE_MOUSE_CURSOR]
        self.move_mouse_cursor_qcb.setChecked(move_mouse_cursor)

        self.updating_gui = False


class Label(QtWidgets.QLabel):
    mouse_press_signal = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.mouse_press_signal.emit()


if __name__ == "__main__":
    matc_qapplication = QtWidgets.QApplication(sys.argv)
    win = SettingsWin()
    win.show()
    sys.exit(matc_qapplication.exec_())

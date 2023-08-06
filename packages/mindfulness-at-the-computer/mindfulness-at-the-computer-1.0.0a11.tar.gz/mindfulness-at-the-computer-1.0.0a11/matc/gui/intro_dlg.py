import logging
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
import matc.gui.breathing_dlg
import matc.globa
import matc.settings
import matc.constants

NEXT = "Next >>"
PREV = "<< Prev"
MARGIN_TOP = 35
WIDGET_SPACING = 10

"""
An alternative to using a custom QDialog can be to use QWizard with QWizardPages
"""


class Label(QtWidgets.QLabel):
    def __init__(self, i_text: str, i_font_size: matc.globa.FontSize = matc.globa.FontSize.medium):
        super().__init__(text=i_text)
        self.setWordWrap(True)
        self.setFont(matc.globa.get_font(i_font_size))
        self.setTextFormat(QtCore.Qt.MarkdownText)
        self.setOpenExternalLinks(True)
        # text_qll.setAlignment(QtCore.Qt.AlignHCenter)


class IconImage(QtWidgets.QLabel):
    def __init__(self, i_file_name: str):
        super().__init__()
        # text_qll.setAlignment(QtCore.Qt.AlignHCenter)
        self.setPixmap(QtGui.QPixmap(matc.globa.get_app_icon_path(i_file_name)))
        # self.setAlignment(QtCore.Qt.AlignHCenter)


class IntroDlg(QtWidgets.QDialog):
    """
    The introduction wizard with examples of dialogs and functionality to adjust initial settings
    """
    close_signal = QtCore.Signal(bool)
    # -the boolean indicates whether we want the breathing dialog to open

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Intro Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.globa.get_app_icon_path("icon.png")))

        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        self.prev_qpb = QtWidgets.QPushButton(PREV)
        self.prev_qpb.setFont(matc.globa.get_font(matc.globa.FontSize.medium))
        self.next_qpb = QtWidgets.QPushButton(NEXT)
        self.next_qpb.setFont(matc.globa.get_font(matc.globa.FontSize.medium))

        self.prev_qpb.clicked.connect(self.on_prev_clicked)
        self.next_qpb.clicked.connect(self.on_next_clicked)

        hbox_l3 = QtWidgets.QHBoxLayout()
        hbox_l3.addStretch(1)
        hbox_l3.addWidget(self.prev_qpb, stretch=1)
        hbox_l3.addWidget(self.next_qpb, stretch=1)
        hbox_l3.addStretch(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        vbox_l2.addWidget(self.wizard_qsw_w3)
        vbox_l2.addLayout(hbox_l3)

        welcome_description_markdown_ll = Label(
            """Welcome to Mindfulness at the Computer!

This introduction will help you understand how to use the application

Mindfulness at the Computer is an application that helps you stay **mindful** while using the computer by reminding you to take **breathing** breaks. These breaks are **interactive** to help you focus on your breathing. There are also **breathing phrases** that can be used while following the breath, to stay mindful of your body, or other aspects of your experience

The main parts of the application:
* The system tray icon
  * The system tray menu
* The breathing dialog
* The settings window

These parts will now be discussed on the following pages. Please click *next* to continue"""
        )
        welcome_page = IntroPage("Welcome", welcome_description_markdown_ll)
        self.wizard_qsw_w3.addWidget(welcome_page)

        systray_description_markdown_ll = Label(
            """When you run Mindfulness at the Computer it is accessible via the system tray.
From the menu that opens when clicking on this icon you can:
* Open the settings window
* Invoke a breathing session
* Invoke a breathing session with a specified phrase
* Exit the application"""
        )

        icon_image = IconImage("icon.png")
        notification_description_markdown_ll = Label(
            f"""**The breathing notification**

This notification is shown at certain intervals to remind you to take a breathing break. You can adjust how often you would like to get this notification."""
        )

        icon_br_image = IconImage("icon-b.png")

        systray_icon_page = IntroPage("The system tray icon", systray_description_markdown_ll, icon_image,
            notification_description_markdown_ll, icon_br_image)
        self.wizard_qsw_w3.addWidget(systray_icon_page)

        tray_menu_descr_markdown_ll = Label("""You can access the tray menu by clicking or right clicking on the systray icon.

The following options are available from the systray menu:
* **Opening the breathing dialog**
* Switching to a different breathing phrase (through the "Phrases" sub-menu)
* Opening the settings dialog
* Enabling/disabling application notifications
* Exiting the application""")
        systray_image = IconImage("systray-menu.png")
        systray_menu_page = IntroPage("The system tray menu", tray_menu_descr_markdown_ll, systray_image)
        self.wizard_qsw_w3.addWidget(systray_menu_page)

        br_dlg_description_ll = Label(
            """This dialog helps you to relax and return to your breathing. Try it out, it's interactive!"""
        )
        self.breathing_dlg = matc.gui.breathing_dlg.BreathingGraphicsView(i_can_be_closed=False)
        self.breathing_dlg.initiate_breathing_gv()
        # self.breathing_dlg.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.breathing_dlg.updateGeometry()
        br_dlg_details_ll = Label(
            """There are two ways to interact with the breathing dialog:
* Using the mouse cursor to hover over the light green area in the middle while breathing in, and leaving the mouse cursor outside the light green area while breathing out
* Using the (right or left) shift key on the keyboard: Pressing down and holding while breathing in, and letting it be while breathing out"""
        )
        self.br_dlg_page = IntroPage("The breathing dialog", br_dlg_description_ll,
            self.breathing_dlg, br_dlg_details_ll)
        self.wizard_qsw_w3.addWidget(self.br_dlg_page)

        settings_description_ll = Label(
            """The settings dialog can be reached by opening the systray menu and selecting "Settings" from there. (Please open it now if you want to follow along in the description below)"""
        )
        settings_details_ll = Label(
            f"""Some of the settings that can be changed:
* Amount of time before a breathing notification is shown --- You may want to adjust this setting now (the default is {matc.settings.BREATHING_BREAK_TIMER_DEFAULT_SECS // 60} minutes)
* Volume of the audio (bells)
* Breathing phrases (displayed at the bottom of the breathing dialog) --- It is possible to add new phrases and reorder them
* Whether or not the application will automatically move the mouse cursor into the breathing dialog (useful if you are using a touchpad)"""
        )
        settings_page = IntroPage("Settings", settings_description_ll, settings_details_ll)
        self.wizard_qsw_w3.addWidget(settings_page)

        """
        usage_overview_description_ll = Label(
            """"""
        )
        settings_page = IntroPage("Settings", settings_description_ll, settings_details_ll)
        self.wizard_qsw_w3.addWidget(settings_page)
        """

        additional_setup_ll = Label(
            """Now that you have started the application you may want to do some *additional setup*. Please find the instructions for your OS on this page: https://mindfulness-at-the-computer.gitlab.io/installation/"""
        )

        relaunch_wizard_ll = Label(
            """You can start this wizard again by choosing "Help" -> "Show intro wizard" in the settings window (available from the system tray icon menu)"""
        )
        other_help_ll = Label(
            """Other ways to get help:
* The gitter chat: https://gitter.im/mindfulness-at-the-computer/community
* Email: [sunyata.software@gmail.com](mailto:sunyata.software@gmail.com)"""
        )
        # more: feedback
        feedback_ll = Label(
            """We are grateful for any feedback you can give us. Please use the email address above to contact us with gratitudes or suggestions for improvements"""
        )
        finish_text_ll = Label(
            """When you click on finish and exit this wizard a breathing dialog will be shown."""
        )

        finish_page = IntroPage("Finish", additional_setup_ll, relaunch_wizard_ll, other_help_ll,
            feedback_ll, finish_text_ll)
        self.wizard_qsw_w3.addWidget(finish_page)

        self.move(150, 100)  # , 680, 300)
        self.update_gui()
        self.show()

    def on_next_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int >= self.wizard_qsw_w3.count() - 1:
            self.close_signal.emit(True)
            self.close()

        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int + 1)
        self.update_gui()

    def on_prev_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int <= 0:
            return
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int - 1)
        self.update_gui()

    def update_gui(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.prev_qpb.setDisabled(current_index_int == 0)

        if current_index_int == self.wizard_qsw_w3.count() - 1:
            self.next_qpb.setText("Finish")  # "open breathing dialog"
        else:
            self.next_qpb.setText(NEXT)

        if self.wizard_qsw_w3.currentWidget() == self.br_dlg_page:
            self.breathing_dlg.setFocus()


class IntroPage(QtWidgets.QWidget):
    def __init__(self, i_title: str, *i_widgets):
        super().__init__()
        """
        self.setSizePolicy(
            self.sizePolicy().horizontalPolicy(),
            QtWidgets.QSizePolicy.Maximum
        )
        """

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        (cm_left, cm_top, cm_right, cm_bottom) = self.vbox_l2.getContentsMargins()
        self.vbox_l2.setContentsMargins(40, cm_top, 20, cm_bottom)
        self.setLayout(self.vbox_l2)
        self.vbox_l2.addSpacing(MARGIN_TOP)
        self.title_qll = QtWidgets.QLabel(i_title)
        # self.title_qll.setTextFormat
        # self.title_qll.setAlignment(QtCore.Qt.AlignHCenter)
        self.title_qll.setFont(matc.globa.get_font(matc.globa.FontSize.xlarge))
        self.vbox_l2.addWidget(self.title_qll)
        self.vbox_l2.addSpacing(WIDGET_SPACING)

        for widget in i_widgets:
            self.vbox_l2.addWidget(widget)
            self.vbox_l2.addSpacing(WIDGET_SPACING)

        self.vbox_l2.addSpacing(WIDGET_SPACING)
        self.vbox_l2.addStretch(1)

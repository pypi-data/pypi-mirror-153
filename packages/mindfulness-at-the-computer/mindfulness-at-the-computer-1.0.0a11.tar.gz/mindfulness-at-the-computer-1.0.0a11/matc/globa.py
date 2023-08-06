import os
import enum
from string import Template
from PySide6 import QtGui
from PySide6 import QtCore
import matc.constants

#############################################
# This file contains
# * global application state which is not stored on disk
# * global functions, for example:
#   * relating to file names/paths
#   * relating to font
# * enums
# * potentially other global functions
#############################################

NO_PHRASE_SELECTED_INT = -1

GRID_VERTICAL_SPACING_LINUX = 15
BUTTON_BAR_HORIZONTAL_SPACING_LINUX = 2

JSON_SETTINGS_FILE_NAME = "settings.json"
APPLICATION_ICON_NAME_STR = "icon.png"
README_FILE_STR = "README.md"

USER_FILES_DIR = "user_files"
IMAGES_DIR = "images"
ICONS_DIR = "icons"
OPEN_ICONIC_ICONS_DIR = "open_iconic"
AUDIO_DIR = "audio"
RES_DIR = "res"

BIG_BELL_FILENAME = "big_bell[cc0]_fade_out.wav"
SMALL_BELL_SHORT_FILENAME = "small_bell_short[cc0].wav"
BREATHING_PHRASE_NOT_SET: int = -1

LIGHT_GREEN_COLOR = "#bfef7f"
DARK_GREEN_COLOR = "#7fcc19"
DARKER_GREEN_COLOR = "#548811"
WHITE_COLOR = "#ffffff"
BLACK_COLOR = "#1C1C1C"

active_phrase_id = BREATHING_PHRASE_NOT_SET
testing_bool = False
sys_info_telist = []
is_breathing_reminder_shown: bool = False
settings_file_path = ""


class BreathingVisalization(enum.Enum):
    bar = 0
    circle = 1
    line = 2
    columns = 3


class FontSize(enum.Enum):
    # Standard font size is (on almost all systems) 12
    small = 9
    medium = 12
    large = 14
    xlarge = 16
    xxlarge = 24


class PhraseSetup(enum.Enum):
    Long = 0
    Switch = 1
    Short = 2


class NotificationType(enum.Enum):
    Both = 0
    Visual = 1
    Audio = 2


class PhraseSelection(enum.Enum):
    same = 0
    random = 1
    ordered = 2


class MoveDirectionEnum(enum.Enum):
    up = 1
    down = 2


def settings_file_exists() -> bool:
    return os.path.isfile(settings_file_path)


def get_config_path(*args) -> str:
    # application_dir_str = os.path.dirname(os.path.dirname(__file__))
    config_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    # logging.debug("QStandardPaths.ConfigLocation = " + config_dir)

    # There is a bug in Qt:
    # For Windows, the application name is included in QStandardPaths.ConfigLocation
    # For Linux, it's not included
    if matc.constants.APPLICATION_NAME not in config_dir:
        config_dir = os.path.join(config_dir, matc.constants.APPLICATION_NAME)
    full_path_str = config_dir
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    os.makedirs(os.path.dirname(full_path_str), exist_ok=True)
    return full_path_str


def get_settings_file_path(i_date_text: str = ""):
    config_path = get_config_path()
    json_file_name: str = JSON_SETTINGS_FILE_NAME
    if i_date_text:
        json_file_name = json_file_name + "_" + i_date_text
    json_file_path = os.path.join(config_path, json_file_name)
    return json_file_path


def get_module_path() -> str:
    module_dir_str: str = os.path.dirname(os.path.abspath(__file__))
    # base_dir_str: str = os.path.dirname(module_dir_str)
    # base_dir_str = os.getcwd()
    # -__file__ is the file that was started, in other words mindfulness-at-the-computer.py
    return module_dir_str


def get_user_audio_path(i_file_name: str = "") -> str:
    if i_file_name:
        user_audio_path_str = os.path.join(get_module_path(), RES_DIR, AUDIO_DIR, i_file_name)
    else:
        user_audio_path_str = os.path.join(get_module_path(), RES_DIR, AUDIO_DIR)
    return user_audio_path_str


def get_app_icon_path(i_file_name: str) -> str:
    ret_icon_path_str = os.path.join(get_module_path(), RES_DIR, ICONS_DIR, i_file_name)
    return ret_icon_path_str


def get_icon_path(i_file_name: str) -> str:
    ret_icon_path_str = os.path.join(get_module_path(), RES_DIR, ICONS_DIR, "open_iconic", i_file_name)
    return ret_icon_path_str


def get_font(i_size, i_bold: bool = False) -> QtGui.QFont:
    font = QtGui.QFont()
    font.setPointSize(i_size.value)
    font.setBold(i_bold)
    return font


def get_html(i_text: str, i_focus: bool = False, i_margin: int=0) -> str:
    html_template_base = """<p 
    style="text-align:center;
    padding:0px;margin:${margin}px;font-size:18px;${bold}">
    ${text}
    </p>"""
    html_template = Template(html_template_base)
    bold_html = ""
    if i_focus:
        bold_html = "font-weight:bold;"
    ret_html = html_template.substitute(margin=i_margin, bold=bold_html, text=i_text)
    return ret_html


def clear_widget_and_layout_children(qlayout_or_qwidget) -> None:
    if qlayout_or_qwidget.widget():
        qlayout_or_qwidget.widget().deleteLater()
    elif qlayout_or_qwidget.layout():
        while qlayout_or_qwidget.layout().count():
            child_qlayoutitem = qlayout_or_qwidget.takeAt(0)
            clear_widget_and_layout_children(child_qlayoutitem)  # Recursive call

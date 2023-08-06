import logging
import logging.handlers
import os
import sys
import argparse
from PySide6 import QtCore
from PySide6 import QtWidgets
import matc.constants
import matc.globa
import matc.settings
import matc.main_object

# The following import looks like it isn't used, but it is necessary for importing the images.
import matc.matc_rc  # pylint: disable=unused-import

LOG_FILE_NAME_STR = "matc.log"


def on_about_to_quit():
    logging.debug("on_about_to_quit --- saving settings to json file (in the user config dir)")
    matc.settings.save_settings_to_json_file()


def main():
    # db_filepath: str = matc.globa.get_database_path()
    # matc.globa.db_file_exists_at_application_startup_bl = os.path.isfile(db_filepath)
    # -settings this variable before the file has been created

    logger = logging.getLogger()
    # -if we set a name here for the logger the file handler will no longer work, unknown why
    logger.handlers = []  # -removing the default stream handler first
    # logger.propagate = False
    log_path_str = matc.globa.get_config_path(LOG_FILE_NAME_STR)
    rfile_handler = logging.handlers.RotatingFileHandler(log_path_str, maxBytes=8192, backupCount=2)
    rfile_handler.setLevel(logging.WARNING)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    rfile_handler.setFormatter(formatter)
    logger.addHandler(rfile_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Handling of (otherwise) uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.excepthook(exc_type, exc_value, exc_traceback)
        if issubclass(exc_type, Exception):
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        else:
            sys.excepthook(exc_type, exc_value, exc_traceback)
        """
    sys.excepthook = handle_exception
    # -can be tested with: raise RuntimeError("RuntimeError")

    default_settings_file_path = matc.globa.get_settings_file_path()
    argument_parser = argparse.ArgumentParser(prog=matc.constants.APPLICATION_PRETTY_NAME,
        description=matc.constants.SHORT_DESCR_STR)
    argument_parser.add_argument("--settings-file", "-s", default=default_settings_file_path,
        help="Path to a settings file (json format). If only a file name is given, the default directory will be used")
    parsed_args = argument_parser.parse_args()
    dir_ = os.path.dirname(parsed_args.settings_file)
    if dir_ and os.path.isdir(dir_):
        matc.globa.settings_file_path = parsed_args.settings_file
    else:
        default_dir = os.path.dirname(default_settings_file_path)
        matc.globa.settings_file_path = os.path.join(default_dir, parsed_args.settings_file)
    matc.settings.update_settings_dict_with_json_data(matc.settings.settings, matc.globa.settings_file_path)

    matc_qapplication = QtWidgets.QApplication(sys.argv)

    # Application information
    matc.globa.sys_info_telist.append(("Application name", matc.constants.APPLICATION_NAME))
    matc.globa.sys_info_telist.append(("Application version", matc.constants.APPLICATION_VERSION))
    matc.globa.sys_info_telist.append(("Config path", matc.globa.get_config_path()))
    matc.globa.sys_info_telist.append(("Module path", matc.globa.get_module_path()))
    matc.globa.sys_info_telist.append(("Python version", sys.version))
    matc.globa.sys_info_telist.append(("Qt version", QtCore.qVersion()))
    # matc.globa.sys_info_telist.append(("Pyside version"))
    sys_info = QtCore.QSysInfo()
    matc.globa.sys_info_telist.append(("OS name and version", sys_info.prettyProductName()))
    matc.globa.sys_info_telist.append(
        ("Kernel type and version", sys_info.kernelType() + " " + sys_info.kernelVersion()))
    matc.globa.sys_info_telist.append(("buildCpuArchitecture", sys_info.buildCpuArchitecture()))
    matc.globa.sys_info_telist.append(("currentCpuArchitecture", sys_info.currentCpuArchitecture()))

    # set stylesheet
    stream = QtCore.QFile(os.path.join(matc.globa.get_module_path(), "matc.qss"))
    stream.open(QtCore.QIODevice.ReadOnly)
    matc_qapplication.setStyleSheet(QtCore.QTextStream(stream).readAll())

    # desktop_widget = matc_qapplication.desktop()
    # matc.globa.sys_info_telist.append(("Virtual desktop", str(desktop_widget.isVirtualDesktop())))
    # matc.globa.sys_info_telist.append(("Screen count", str(desktop_widget.screenCount())))
    # matc.globa.sys_info_telist.append(("Primary screen", str(desktop_widget.primaryScreen())))

    system_locale = QtCore.QLocale.system().name()
    logging.info('System Localization: ' + system_locale)
    matc_qapplication.setQuitOnLastWindowClosed(False)
    matc_qapplication.aboutToQuit.connect(on_about_to_quit)

    matc_main_object = matc.main_object.MainObject()
    sys.exit(matc_qapplication.exec())

if __name__ == "__main__":
    main()

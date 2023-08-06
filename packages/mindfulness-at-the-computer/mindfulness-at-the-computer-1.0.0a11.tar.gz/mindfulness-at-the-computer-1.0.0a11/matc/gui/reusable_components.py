from PySide6 import QtWidgets, QtCore
from matc import globa


class H1(QtWidgets.QLabel):
    """
    Heading 1
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class H2(QtWidgets.QLabel):
    """
    Heading 2
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class HorizontalLine(QtWidgets.QFrame):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFrameShape(self.HLine)


class RadioButtonLeft(QtWidgets.QRadioButton):
    """
    The left button of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class RadioButtonMiddle(QtWidgets.QRadioButton):
    """
    One of the middle buttons of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class RadioButtonRight(QtWidgets.QRadioButton):
    """
    The right button of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class PushButton(QtWidgets.QPushButton):
    """
    A rectangular button
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class PhrasesList(QtWidgets.QListWidget):
    def __init__(self, *__args):
        super().__init__(*__args)


class PageGrid(QtWidgets.QGridLayout):
    def __init__(self, *__args):
        super().__init__(*__args)
        if QtCore.QSysInfo.kernelType() != "darwin":
            self.setVerticalSpacing(globa.GRID_VERTICAL_SPACING_LINUX)


class ButtonGrid(QtWidgets.QGridLayout):
    def __init__(self, *__args):
        super().__init__(*__args)
        if QtCore.QSysInfo.kernelType() != "darwin":
            self.setHorizontalSpacing(globa.BUTTON_BAR_HORIZONTAL_SPACING_LINUX)

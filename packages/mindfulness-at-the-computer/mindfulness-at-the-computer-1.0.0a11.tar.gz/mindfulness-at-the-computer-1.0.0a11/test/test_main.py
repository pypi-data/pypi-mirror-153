import sys
import unittest
from PySide6 import QtTest
from PySide6 import QtCore
from PySide6 import QtWidgets
import matc.main_object
import matc.globa


test_app = QtWidgets.QApplication(sys.argv)
# -has to be set here (rather than in __main__) to avoid an error


# https://doc.qt.io/qt-5/qpluginloader.html

# https://doc.qt.io/qt-5/qlibraryinfo.html
plugins_path: str = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath)
print(f"{plugins_path=}")


class MainTest(unittest.TestCase):
    """
    "@unittest.skip" can be used to skip a test
    """

    @classmethod
    def setUpClass(cls):
        matc.globa.testing_bool = True

    def setUp(self):
        pass

    def test_main_object(self):
        i = 0


if __name__ == "__main__":
    unittest.main()

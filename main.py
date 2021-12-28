import sys
from PySide6 import QtWidgets
import myMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

if __name__ == '__main__':
    app = 0
    if QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    browser = QWebEngineView()
    window = myMainWindow.myMainWindow(browser)
    window.show()
    sys.exit(app.exec())

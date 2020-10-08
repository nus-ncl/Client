import sys
from PySide2 import QtWidgets
import myMainWindow2 as myMainWindow

if __name__ == '__main__':
	app = 0
	if QtWidgets.QApplication.instance():
		app = QtWidgets.QApplication.instance()
	else:
		app = QtWidgets.QApplication(sys.argv)

	window = myMainWindow.myMainWindow()
	window.show()
	sys.exit(app.exec_())

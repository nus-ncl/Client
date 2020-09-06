import os
import subprocess
import Port
import ProcessTag
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog
from ScrollUI import Ui_MainWindow

from IOXML import *


class myMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
	def __init__(self):
		super(myMainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.Node_QTreeWidgetItem=[]
		self.Populate(self.Node_QTreeWidgetItem)

	def updateQTreeWidgetItem(self):
		TagName = "VM"
		Attributes = ["name", "Node", "ExperimentName", "TeamName"]
		try:
			output = ProcessTag.processTagName(self.document, TagName, Attributes)
			print(output)
		except ValueError as e:
			print("Failed to import: {0}".format(e))


		self.Machine = output[0]
		Node = output[1]
		Exp = output[2]
		Team = output[3]

		# print([Machine[0],Exp[0],Team[0]])
		Node_set = list(set(Node))
		Node_set.sort()

		self.Node_QTreeWidgetItem = []
		for i in range(len(Node_set)):
			self.Node_QTreeWidgetItem.append(QtWidgets.QTreeWidgetItem(Node_set[i:i + 1]))

		for i in range(len(self.Machine)):
			Node_Belong_To = Node_set.index(Node[i])
			child = QtWidgets.QTreeWidgetItem([self.Machine[i], Exp[i], Team[i]])
			self.Node_QTreeWidgetItem[Node_Belong_To].addChild(child)

		# clear previous treeWidget items and populate the new
		self.ui.treeWidget.clear()
		self.Populate(self.Node_QTreeWidgetItem)

	def click(self):
		print("You click!")


	def doubleclick(self,item,col):
		self.TagName = "VRDEProperties"
		self.Attributes = ["name", "value"]
		self.vrde_port = {}
		try:
			self.output = ProcessTag.processTagName(self.document, self.TagName, self.Attributes)
			for i in range(len(self.Machine)):
				self.vrde_port[self.Machine[i]] = self.output[1][2 * i + 1]
			print(self.vrde_port)

		except ValueError as e:
			print("Failed to import: {0}".format(e))

		username = self.ui.lineEdit.text()
		local_addr='127.0.0.1'
		local_port = 12345
		while(Port.is_port_used(local_addr,local_port)):
			local_port += 1
		node = item.parent().text(0)
		exp = item.text(1)
		team = item.text(2)
		machine = item.text(0)
		ssh_cmd = "ssh -fNT -L " + str(local_port) + ":" + node + "." + exp + "." + team + ".ncl.sg:" + self.vrde_port[machine] + " " + username + "@users.ncl.sg"
		print(ssh_cmd)
		# pro1 is NOT the ssh tunnel pid, it's the pid of a process which invokes background ssh tunnel
		# so this pro1 terminates when Popen returns. But the background ssh tunnel pid is still there
		pro1 = subprocess.Popen(ssh_cmd.split())
		# self.tunnel_pid = pro1.pid
		# print(self.tunnel_pid)
		# print("done")
		# time.sleep(10)
		# print("You doubleclick! {},{},{},{},{}".format(item.text(0),item.parent().text(0),item.text(1),item.text(2),col))
		# subprocess.run(("rdesktop -a 16 localhost:" + str(local_port)).split())
		# subprocess.run(("kill -9 " + str(self.tunnel_pid)).split())

	def Populate(self, Node_QTreeWidgetItem):
		self.ui.treeWidget.resize(600, 400)
		self.ui.treeWidget.setColumnCount(3)
		self.ui.treeWidget.setHeaderLabels(["Node Name", "Experiment Name", "Team Name"])
		self.ui.treeWidget.addTopLevelItems(Node_QTreeWidgetItem)

	def openFile(self,filePath):
		if os.path.exists(filePath):
			path = QFileDialog.getOpenFileName(self,"Open File Dialog",filePath,"XML files(*.xml)")
		else:
			path = QFileDialog.getOpenFileName(self,"Open File Dialog","/","XML files(*.xml)")
		print(path)
		self.document = importXmlDOM(str(path[0]))
		self.updateQTreeWidgetItem()
		# self.fileLineEdit.setText(str(path[0]))
import os
import subprocess
import Port
import ProcessTag2 as ProcessTag
import IOXML
import My_SSH
import threading
import time
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog
from ScrollUI import Ui_MainWindow


class myThread(threading.Thread):
	def __init__(self, local_port, node, exp, team, ssh_port, username):
		threading.Thread.__init__(self)
		self.local_port = local_port
		self.node = node
		self.exp = exp
		self.team = team
		self.ssh_port = ssh_port
		self.username = username

	def run(self):
		print("port forwarding started!")
		My_SSH.port_forwarding(self.local_port, f"{self.node}.{self.exp}.{self.team}.ncl.sg", int(self.ssh_port),
		                       "users.ncl.sg", 22, self.username,
		                       "/Users/hkwany/.ssh/id_rsa")
		# My_SSH.port_forwarding(12345, "n2.Enterprise.NCLSecurity.ncl.sg", 22345, "users.ncl.sg", 22, "khuang96",
		#                        "/Users/hkwany/.ssh/id_rsa")


class myMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(myMainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.Node_QTreeWidgetItem = []
		self.Populate(self.Node_QTreeWidgetItem)
		self.platform = ''
		self.connection_function = ''

	def updateQTreeWidgetItem(self):
		TagName = "Machine"

		self.Machine = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'name')
		Node = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'Node')
		Exp = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'ExperimentName')
		Team = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'TeamName')

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

	def rbclicked(self):
		sender = self.sender()
		# print(sender)
		if sender == self.ui.bg1:
			if self.ui.bg1.checkedId() == 1:
				self.platform = 'Linux'
			elif self.ui.bg1.checkedId() == 2:
				self.platform = 'Win'
			elif self.ui.bg1.checkedId() == 3:
				self.platform = 'MacOS'
			else:
				self.platform = ''
		else:
			if self.ui.bg2.checkedId() == 4:
				self.connection_function = 'RDP'
			elif self.ui.bg2.checkedId() == 5:
				self.connection_function = 'SSH'
			elif self.ui.bg2.checkedId() == 6:
				self.connection_function = 'VNC'
			else:
				self.connection_function = ''

	# print(self.info1)
	# print(self.info2)

	def click(self):
		print("You click!")

	def doubleclick(self, item, col):
		# self.TagName = "VRDEProperties"
		# self.Attributes = ["name", "value"]
		# self.TagName = "vrdeport"
		# self.Attributes = "value"
		# self.vrde_port = {}
		username = self.ui.lineEdit.text()
		local_addr = '127.0.0.1'
		local_port = 12345
		while (Port.is_port_used(local_addr, local_port)):
			local_port += 1
		node = item.parent().text(0)
		exp = item.text(1)
		team = item.text(2)
		machine = item.text(0)

		# vrde
		if (self.platform == 'Linux'):
			if (self.connection_function == 'RDP'):
				# RDP
				rdp_port = 0
				NodeName = "VRDEProperties"
				TagName = "vrdeport"
				Attributes = ["value"]
				try:
					output_dict = ProcessTag.getGlobalNodeTagAttributes(self.document, NodeName, TagName, Attributes)
				# print(output_dict)
				# for i in range(len(self.Machine)):
				# 	vrde_port[self.Machine[i]] = output[i]

				except ValueError as e:
					print("Failed to import: {0}".format(e))

				rdp_port = output_dict[machine][0]['value']

				'''
				-f: Go to background
				-N: Do not execute a remote command. This is useful for just forwarding ports
				-T: Disable pseudo-tty allocation
				'''
				ssh_local_forward_cmd = "ssh -fNT -L " + str(
					local_port) + ":" + node + "." + exp + "." + team + ".ncl.sg:" + rdp_port + " " + username + "@users.ncl.sg"
				print(ssh_local_forward_cmd)
				thread1 = myThread(local_port, node, exp, team, ssh_port, username).start()
				# pro1 = subprocess.Popen(ssh_local_forward_cmd.split())
				# pro1.wait()
				# print(pro1.pid)
				# self.tunnel_pid = pro1.pid
				# print(self.tunnel_pid)

				time.sleep(2)
				rdesktop_cmd = "rdesktop -a 16 localhost:" + str(local_port)
				print(rdesktop_cmd)
				subprocess.run(rdesktop_cmd.split())

			if (self.connection_function == 'SSH'):
				# SSH
				ssh_port = 0
				NodeName = "Port_Forwarding"
				TagName = "Forwarding"
				Attributes = ["hostip", "hostport", "guestport"]
				try:
					output_dict = ProcessTag.getGlobalNodeTagAttributes(self.document, NodeName, TagName, Attributes)
				except ValueError as e:
					print("Failed to import: {0}".format(e))

				for port_forwarding in output_dict[machine]:
					if port_forwarding['guestport'] == '22':
						ssh_port = port_forwarding['hostport']
				if ssh_port == 0:
					print("This VM's SSH port hasn't been port forwarded!")
				else:
					ssh_local_forward_cmd = f"ssh -fNT -L {str(local_port)}:{node}.{exp}.{team}.ncl.sg:{ssh_port} {username}@users.ncl.sg"
					print(ssh_local_forward_cmd)
					thread2 = myThread(local_port, node, exp, team, ssh_port, username).start()

					# My_SSH.port_forwarding(local_port, f"{node}.{exp}.{team}.ncl.sg", int(ssh_port), "users.ncl.sg", 22,
					#                        username, "/Users/hkwany/.ssh/id_rsa")
					# port_forwarding(12345,"n2.Enterprise.NCLSecurity.ncl.sg",22345,"users.ncl.sg",22,"khuang96","/Users/hkwany/.ssh/id_rsa")

					# pro1 = subprocess.Popen(ssh_local_forward_cmd.split())
					# pro1.wait()
					# print(pro1.pid)
					time.sleep(2)
					ssh_cmd = "ssh -p " + str(local_port) + " vagrant@localhost"
					print(ssh_cmd)
					subprocess.run(ssh_cmd.split())

			if (self.connection_function == 'VNC'):
				pass

	# print("You doubleclick! {},{},{},{},{}".format(item.text(0),item.parent().text(0),item.text(1),item.text(2),col))
	# subprocess.run(("rdesktop -a 16 localhost:" + str(local_port)).split())
	# subprocess.run(("ssh -p " + str(local_port) + " vagrant@localhost").split())
	# subprocess.run(("kill -9 " + str(self.tunnel_pid)).split())

	def Populate(self, Node_QTreeWidgetItem):
		self.ui.treeWidget.resize(600, 400)
		self.ui.treeWidget.setColumnCount(3)
		self.ui.treeWidget.setHeaderLabels(["Node Name", "Experiment Name", "Team Name"])
		self.ui.treeWidget.addTopLevelItems(Node_QTreeWidgetItem)

	def openFile(self, filePath):
		if os.path.exists(filePath):
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", filePath, "XML files(*.xml)")
		else:
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", "/", "XML files(*.xml)")
		print(path)
		self.document = IOXML.importXmlDOM(str(path[0]))
		self.updateQTreeWidgetItem()
# self.fileLineEdit.setText(str(path[0]))

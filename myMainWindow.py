import os
import subprocess
import Port
import ProcessTag
import IOXML
import My_SSH
import threading
import time
from pathlib import Path
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog
from ScrollUI import Ui_MainWindow


class TunnelThread(threading.Thread):
	def __init__(self, local_port, node, exp, team, ssh_port, username):
		threading.Thread.__init__(self)
		self.local_port = local_port
		self.node = node
		self.exp = exp
		self.team = team
		self.ssh_port = ssh_port
		self.username = username

	def run(self):
		home = str(Path.home())
		My_SSH.port_forwarding(self.local_port, f"{self.node}.{self.exp}.{self.team}.ncl.sg", int(self.ssh_port),
		                       "users.ncl.sg", 22, self.username,
		                       f"{home}/.ssh/id_rsa")
		# My_SSH.port_forwarding(12345, "n2.Enterprise.NCLSecurity.ncl.sg", 22345, "users.ncl.sg", 22, "khuang96",
		#                        "/Users/hkwany/.ssh/id_rsa")
		print("port forwarding started!")


class CheckPortThread(threading.Thread):
	def __init__(self, local_port):
		threading.Thread.__init__(self)
		self.local_port = local_port

	def run(self):
		while not Port.is_port_used('127.0.0.1', self.local_port):
			print("SSH tunnel has not been set up, please wait.")
			time.sleep(1)
		print("SSH tunnel has been set up successfully")

class myMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super(myMainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.Node_QTreeWidgetItem = []
		self.Populate(self.Node_QTreeWidgetItem)
		self.platform = None
		self.connection_function = None

	def updateQTreeWidgetItem(self):
		TagName = "Machine"

		Machine = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'name')
		Node = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'Node')
		Exp = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'ExperimentName')
		Team = ProcessTag.getGlobalMachineAttribute(self.document, TagName, 'TeamName')

		Node_set = list(set(Node))
		Node_set.sort()

		self.Node_QTreeWidgetItem = []
		for i in range(len(Node_set)):
			self.Node_QTreeWidgetItem.append(QtWidgets.QTreeWidgetItem(Node_set[i:i + 1]))

		for i in range(len(Machine)):
			node_Belong_To = Node_set.index(Node[i])
			child = QtWidgets.QTreeWidgetItem([Machine[i], Exp[i], Team[i]])
			self.Node_QTreeWidgetItem[node_Belong_To].addChild(child)

		# clear previous treeWidget items and populate the new
		self.ui.treeWidget.clear()
		self.Populate(self.Node_QTreeWidgetItem)

	def platform_Connection_Clicked(self):
		sender = self.sender()
		if sender == self.ui.bg1:
			if self.ui.bg1.checkedId() == 1:
				self.platform = 'Linux'
			elif self.ui.bg1.checkedId() == 2:
				self.platform = 'Win'
			elif self.ui.bg1.checkedId() == 3:
				self.platform = 'MacOS'
			else:
				self.platform = None
		else:
			if self.ui.bg2.checkedId() == 4:
				self.connection_function = 'RDP'
			elif self.ui.bg2.checkedId() == 5:
				self.connection_function = 'SSH'
			elif self.ui.bg2.checkedId() == 6:
				self.connection_function = 'VNC'
			else:
				self.connection_function = None

	def click(self):
		print("Plz double click!")

	def doubleclick(self, item, col):
		username = self.ui.lineEdit.text()
		local_addr = '127.0.0.1'
		local_port = 12345
		while Port.is_port_used(local_addr, local_port):
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
				except ValueError as e:
					print("Failed to import: {0}".format(e))
				print(output_dict)
				if (not output_dict[machine]) or (output_dict[machine][0]['value'] == ''):
					pass
				else:
					rdp_port = output_dict[machine][0]['value']
				if rdp_port == 0:
					print("This VM's rdesktop port hasn't been set!")
				else:
					'''
					-f: Go to background
					-N: Do not execute a remote command. This is useful for just forwarding ports
					-T: Disable pseudo-tty allocation
					'''
					ssh_local_forward_cmd = "ssh -o StrictHostKeyChecking=no -fNT -L " + str(
						local_port) + ":" + node + "." + exp + "." + team + ".ncl.sg:" + rdp_port + " " + username + "@users.ncl.sg"
					print(ssh_local_forward_cmd)
					ssh_thread = TunnelThread(local_port, node, exp, team, rdp_port, username)
					ssh_thread.start()
					check_port_thread = CheckPortThread(local_port)
					check_port_thread.start()
					check_port_thread.join()
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
					ssh_local_forward_cmd = f"ssh -o StrictHostKeyChecking=no -fNT -L {str(local_port)}:{node}.{exp}.{team}.ncl.sg:{ssh_port} {username}@users.ncl.sg"
					print(ssh_local_forward_cmd)
					ssh_thread = TunnelThread(local_port, node, exp, team, ssh_port, username)
					ssh_thread.start()
					check_port_thread = CheckPortThread(local_port)
					check_port_thread.start()
					check_port_thread.join()
					ssh_cmd = "ssh -p " + str(local_port) + " -o StrictHostKeyChecking=no" + " vagrant@localhost"
					print(ssh_cmd)
					subprocess.run(ssh_cmd.split())

			if (self.connection_function == 'VNC'):
				pass


	def Populate(self, Node_QTreeWidgetItem):
		self.ui.treeWidget.resize(600, 400)
		self.ui.treeWidget.setColumnCount(3)
		self.ui.treeWidget.setHeaderLabels(["Node Name", "Experiment Name", "Team Name"])
		self.ui.treeWidget.addTopLevelItems(Node_QTreeWidgetItem)

	def openFile(self, file_path):
		if os.path.exists(file_path):
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", file_path, "XML files(*.xml)")
		else:
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", "/", "XML files(*.xml)")
		print(path)
		self.document = IOXML.importXmlDOM(str(path[0]))
		self.updateQTreeWidgetItem()

import os
import subprocess
import Port
import ProcessTag
import IOXML
import My_SSH
import threading
import time
import webbrowser
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
		self.vm_connection_method = None
		self.node_connection_method = None

	def updateQTreeWidgetItem(self):
		Machine = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
		Node = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'Node')
		Exp = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'ExperimentName')
		Team = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'TeamName')

		Node_set = list(set(Node))
		Node_set.sort()

		self.Node_QTreeWidgetItem = []
		for i in range(len(Node_set)):
			self.Node_QTreeWidgetItem.append(QtWidgets.QTreeWidgetItem(Node_set[i:i + 1]))

		for i in range(len(Machine)):
			node_Belong_To = Node_set.index(Node[i])
			machine = QtWidgets.QTreeWidgetItem([Machine[i], Exp[i], Team[i]])
			self.Node_QTreeWidgetItem[node_Belong_To].addChild(machine)

		# clear previous treeWidget items and populate the new
		self.ui.treeWidget.clear()
		self.Populate(self.Node_QTreeWidgetItem)

	# self.Populate(root_QTreeWidgetItem)

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
		elif sender == self.ui.bg2:
			if self.ui.bg2.checkedId() == 4:
				self.vm_connection_method = 'Console'
			elif self.ui.bg2.checkedId() == 5:
				self.vm_connection_method = 'SSH'
			else:
				self.vm_connection_method = None
		else:
			# bg3
			if self.ui.bg3.checkedId() == 6:
				self.node_connection_method = 'VNC'
			elif self.ui.bg3.checkedId() == 7:
				self.node_connection_method = 'SSH'
			else:
				self.node_connection_method = None

	def click(self):
		print("Plz double click!")

	def doubleclick(self, item):
		username = self.ui.lineEdit.text()
		local_addr = '127.0.0.1'
		local_port = 12345
		while Port.is_port_used(local_addr, local_port):
			local_port += 1
		# print(item.parent())
		if item.parent():
			# machine doubleclick
			node = item.parent().text(0)
			machine_name = item.text(0)
			exp_name = item.text(1)
			team_name = item.text(2)
			# vrde
			if (self.platform == 'Linux'):
				if (self.vm_connection_method == 'Console'):
					# VRDE Console
					remoteDisplayEnabled = ProcessTag.getTagAttributeValue(self.document, 'RemoteDisplay', 'enabled')
					remoteDisplayPort = ProcessTag.getTagAttributeValueWithCondition(self.document, 'Property', 'value',
					                                                                 'name', 'TCP/Ports')
					for index, enabled in enumerate(remoteDisplayEnabled):
						if enabled == 'false':
							remoteDisplayPort.insert(index, None)
					machine_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
					for index, name in enumerate(machine_name_list):
						if name == machine_name:
							rdp_port = remoteDisplayPort[index]
							break

					if not rdp_port:
						print("This VM's rdesktop port hasn't been set!")
					else:
						'''
						-f: Go to background
						-N: Do not execute a remote command. This is useful for just forwarding ports
						-T: Disable pseudo-tty allocation
						'''
						# ssh_local_forward_cmd = "ssh -o StrictHostKeyChecking=no -fNT -L " + str(
						# 	local_port) + ":" + node + "." + exp_name + "." + team_name + ".ncl.sg:" + rdp_port + " " + username + "@users.ncl.sg"
						# print(ssh_local_forward_cmd)
						ssh_thread = TunnelThread(local_port, node, exp_name, team_name, rdp_port, username)
						ssh_thread.start()
						check_port_thread = CheckPortThread(local_port)
						check_port_thread.start()
						check_port_thread.join()
						rdesktop_cmd = "rdesktop -a 16 localhost:" + str(local_port)
						print(rdesktop_cmd)
						subprocess.run(rdesktop_cmd.split())

				if (self.vm_connection_method == 'SSH'):
					# SSH
					hostport = None
					guestport = None
					NATNode = ProcessTag.getTagAttributeValue(self.document, 'NAT', 'enabled')
					ForwardingNum = ProcessTag.getTextNodeValue(self.document, 'ForwardingNum')
					# print(ForwardingNode)
					for index, value in enumerate(NATNode):
						if value == 'false':
							ForwardingNum.insert(index, None)

					ForwardingName = ProcessTag.getTagAttributeValue(self.document, 'Forwarding', 'name')
					Forwardinghostport = ProcessTag.getTagAttributeValue(self.document, 'Forwarding', 'hostport')
					Forwardingguestport = ProcessTag.getTagAttributeValue(self.document, 'Forwarding', 'guestport')
					AllForwardings = []
					for index in range(len(ForwardingName)):
						AllForwardings.append(
							(ForwardingName[index], Forwardinghostport[index], Forwardingguestport[index]))

					Forwarding = []
					start = 0
					end = 0
					for num in ForwardingNum:
						if num:
							end = end + int(num)
							Forwarding.append(AllForwardings[start:end])
							start = end
						else:
							Forwarding.append([])

					machine_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
					for index, name in enumerate(machine_name_list):
						if name == machine_name:
							for forwarding_entry in Forwarding[index]:
								if forwarding_entry[0] == 'ssh':
									hostport = forwarding_entry[1]
									guestport = forwarding_entry[2]
									break
							break

					if not hostport or not guestport:
						print("This VM's SSH port hasn't been port forwarded!")
					else:
						# ssh_local_forward_cmd = f"ssh -o StrictHostKeyChecking=no -fNT -L {str(local_port)}:{node}.{exp_name}.{team_name}.ncl.sg:{hostport} {username}@users.ncl.sg"
						# print(ssh_local_forward_cmd)
						ssh_thread = TunnelThread(local_port, node, exp_name, team_name, hostport, username)
						ssh_thread.start()
						check_port_thread = CheckPortThread(local_port)
						check_port_thread.start()
						check_port_thread.join()
						ssh_cmd = "ssh -p " + str(local_port) + " -o StrictHostKeyChecking=no" + " vagrant@localhost"
						print(ssh_cmd)
						subprocess.run(ssh_cmd.split())
		else:
			# node doubleclick
			node_name = item.text(0)
			NodeList = ProcessTag.getTagAttributeValue(self.document,'Node','name')
			VNCAddressList = ProcessTag.getTextNodeValue(self.document,'VNCAddress')
			if (self.node_connection_method == 'VNC'):
				# node VNC
				# web browser
				for index, value in enumerate(NodeList):
					if value == node_name:
						VNCAddress = VNCAddressList[index]
						break
				webbrowser.open(VNCAddress)

			elif (self.node_connection_method == 'SSH'):
				# node SSH
				# SSH
				guestport = 22
				node_name_list = ProcessTag.getTagAttributeValue(self.document,'Node','name')
				exp_name_list = ProcessTag.getTagAttributeValue(self.document,'Node','ExperimentName')
				team_name_list = ProcessTag.getTagAttributeValue(self.document,'Node','TeamName')

				for index, value in enumerate(node_name_list):
					if value == node_name:
						exp_name = exp_name_list[index]
						team_name = team_name_list[index]
						break

				# ssh_local_forward_cmd = f"ssh -o StrictHostKeyChecking=no -fNT -L {str(local_port)}:{node_name}.{exp_name}.{team_name}.ncl.sg:{guestport} {username}@users.ncl.sg"
				# print(ssh_local_forward_cmd)
				ssh_thread = TunnelThread(local_port, node_name, exp_name, team_name, guestport, username)
				ssh_thread.start()
				check_port_thread = CheckPortThread(local_port)
				check_port_thread.start()
				check_port_thread.join()
				ssh_cmd = "ssh -p " + str(local_port) + " -o StrictHostKeyChecking=no " + username + "@localhost"
				print(ssh_cmd)
				subprocess.run(ssh_cmd.split())

	def Populate(self, Node_QTreeWidgetItem):
		self.ui.treeWidget.resize(600, 400)
		self.ui.treeWidget.setColumnCount(3)
		self.ui.treeWidget.setHeaderLabels(["Machine Name", "Experiment Name", "Team Name"])
		self.ui.treeWidget.addTopLevelItems(Node_QTreeWidgetItem)

	def openFile(self, file_path):
		if os.path.exists(file_path):
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", file_path, "XML files(*.xml)")
		else:
			path = QFileDialog.getOpenFileName(self, "Open File Dialog", "/", "XML files(*.xml)")
		print(path)
		self.document = IOXML.parseXML(str(path[0]))
		self.updateQTreeWidgetItem()

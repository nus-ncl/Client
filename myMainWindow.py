import os
import platform
import base64
import stat
import subprocess
import Port
import ProcessTag
import IOXML
import My_SSH
import threading
import time
import webbrowser
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from ScrollUI import Ui_MainWindow
from PySide6.QtCore import QUrl
from config import default

CLIENT_PATH = os.path.dirname(os.path.abspath(__file__))
PRIVATE_KEY_DIRECTORY_PATH = f"{CLIENT_PATH}/private_key"


class DeterTunnelThread(threading.Thread):
    def __init__(self, local_port, node, exp, team, ssh_port, username):
        threading.Thread.__init__(self)
        self.local_port = local_port
        self.node = node
        self.exp = exp
        self.team = team
        self.ssh_port = ssh_port
        self.username = username

    def run(self):
        permission = oct(os.stat(f"{PRIVATE_KEY_DIRECTORY_PATH}/{self.username}.pem")[stat.ST_MODE])[-3:]
        if platform.system() == 'Windows' or permission == '400':
            My_SSH.port_forwarding(self.local_port, f"{self.node}.{self.exp}.{self.team}.ncl.sg", int(self.ssh_port),
                                   "users.ncl.sg", 22, self.username,
                                   f"{PRIVATE_KEY_DIRECTORY_PATH}/{self.username}.pem")
        else:
            print(f"Please run 'chmod 400 {PRIVATE_KEY_DIRECTORY_PATH}/{self.username}.pem'")


class OpenStackTunnelThread(threading.Thread):
    def __init__(self, local_port, remote_host, remote_port, username):
        threading.Thread.__init__(self)
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.username = username

    def run(self):
        permission = oct(os.stat(f"{PRIVATE_KEY_DIRECTORY_PATH}/{self.username}.pem")[stat.ST_MODE])[-3:]
        if platform.system() == 'Windows' or permission == '400':
            My_SSH.port_forwarding(self.local_port, self.remote_host, int(self.remote_port),
                                   "gateway.ncl.sg", 22, self.username,
                                   f"{PRIVATE_KEY_DIRECTORY_PATH}/{self.username}.pem")
        else:
            print(f"Please run 'chmod 400 {PRIVATE_KEY_DIRECTORY_PATH}/{self.username}.pem'")


class CheckPortThread(threading.Thread):
    def __init__(self, local_port):
        threading.Thread.__init__(self)
        self.local_port = local_port
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while self._running and (not Port.is_port_used('127.0.0.1', self.local_port)):
            print("SSH tunnel has not been set up, please wait.")
            time.sleep(1)
        if self._running:
            print("SSH tunnel has been set up successfully")
        else:
            print("SSH tunnel has been set up unsuccessfully")


class WSSH_Thread(threading.Thread):
    def __init__(self, wssh_port):
        threading.Thread.__init__(self)
        self.wssh_port = wssh_port

    def run(self):
        wssh_cmd = "wssh --port=" + str(self.wssh_port) + " &"
        print(wssh_cmd)
        subprocess.Popen(wssh_cmd.split())


class myMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, browser):
        super(myMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Node_QTreeWidgetItem = []
        self.platform = None
        # self.CVE = None
        self.target_platform = None
        self.url = None
        self.connection = None
        # self.vm_connection_method = None
        # self.node_connection_method = None
        self.Populate(self.Node_QTreeWidgetItem)
        self.browser = browser
        self.instance_selected = None

    def updateQTreeWidgetItem(self):
        if self.target_platform == 'deter':
            Node = ProcessTag.getTagAttributeValue(self.document, 'Node', 'name')
            Machine = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
            MachineOnNode = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'Node')
            Exp = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'ExperimentName')
            Team = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'TeamName')

            Node_set = list(set(Node))
            Node_set.sort()

            self.Node_QTreeWidgetItem = []
            for i in range(len(Node_set)):
                self.Node_QTreeWidgetItem.append(QtWidgets.QTreeWidgetItem(Node_set[i:i + 1]))

            for i in range(len(Machine)):
                # node_belong_to = Node_set.index(Node[i])
                node_belong_to = Node_set.index(MachineOnNode[i])
                entry = QtWidgets.QTreeWidgetItem([Machine[i], Exp[i], Team[i]])
                self.Node_QTreeWidgetItem[node_belong_to].addChild(entry)
        elif self.target_platform == 'openstack':
            Project = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'Project')
            Instance = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
            # Exp = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'Project')
            Domain = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'Domain')
            Project_set = list(set(Project))
            Project_set.sort()
            self.Node_QTreeWidgetItem = []
            for i in range(len(Project_set)):
                self.Node_QTreeWidgetItem.append(QtWidgets.QTreeWidgetItem(Project_set[i:i + 1]))

            for i in range(len(Instance)):
                project_belong_to = Project_set.index(Project[i])
                entry = QtWidgets.QTreeWidgetItem([Instance[i], Project[i], Domain[i]])
                self.Node_QTreeWidgetItem[project_belong_to].addChild(entry)

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
        elif sender == self.ui.bg2:
            if self.ui.bg2.checkedId() == 4:
                self.connection = 'Console'
            elif self.ui.bg2.checkedId() == 5:
                self.connection = 'SSH'
            else:
                self.connection = None
        # elif sender == self.ui.bg2:
        #     if self.ui.bg2.checkedId() == 4:
        #         self.vm_connection_method = 'Console'
        #     elif self.ui.bg2.checkedId() == 5:
        #         self.vm_connection_method = 'SSH'
        #     else:
        #         self.vm_connection_method = None
        # else:
        #     # bg3
        #     if self.ui.bg3.checkedId() == 6:
        #         self.node_connection_method = 'VNC'
        #     elif self.ui.bg3.checkedId() == 7:
        #         self.node_connection_method = 'SSH'
        #     else:
        #         self.node_connection_method = None

    def click(self, item):
        self.instance_selected = item.text(0)
        print(f"You've selected the machine: {self.instance_selected}")

    def doubleclick(self, item):
        username = self.ui.lineEdit.text()
        local_addr = '127.0.0.1'
        local_port = 12345
        while Port.is_port_used(local_addr, local_port):
            local_port += 1
        # self.target_platform = ProcessTag.getRootElementAttributeValue(self.document, 'platform')
        # deter
        if self.target_platform == 'deter':
            # machine doubleclick
            if item.parent():
                print('You double-click the Machine')
                node_name = item.parent().text(0)
                machine_name = item.text(0)
                exp_name = item.text(1)
                team_name = item.text(2)
                if (self.connection == 'Console'):
                    # VM VRDE Console
                    remoteDisplayEnabled = ProcessTag.getTagAttributeValue(self.document, 'RemoteDisplay',
                                                                           'enabled')
                    remoteDisplayPort = ProcessTag.getTagAttributeValueWithCondition(self.document, 'Property',
                                                                                     'value',
                                                                                     'name', 'TCP/Ports')

                    for index, enabled in enumerate(remoteDisplayEnabled):
                        if enabled == 'false':
                            remoteDisplayPort[index] = None
                    machine_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')

                    for index, name in enumerate(machine_name_list):
                        if name == machine_name:
                            rdp_port = remoteDisplayPort[index]
                            break
                    if not rdp_port:
                        print("This Machine's rdesktop port hasn't been set!")
                    else:
                        '''
                        -f: Go to background
                        -N: Do not execute a remote command. This is useful for just forwarding ports
                        -T: Disable pseudo-tty allocation
                        '''
                        ssh_thread = DeterTunnelThread(local_port, node_name, exp_name, team_name, rdp_port, username)
                        ssh_thread.start()
                        check_port_thread = CheckPortThread(local_port)
                        check_port_thread.start()
                        check_port_thread.join(timeout=5)
                        check_port_thread.terminate()
                        if self.platform == 'MacOS':
                            rdesktop_cmd = "open rdp://127.0.0.1:" + str(local_port)
                        elif self.platform == 'Linux':
                            rdesktop_cmd = "rdesktop -a 16 127.0.0.1:" + str(local_port)
                        elif self.platform == 'Win':
                            rdesktop_cmd = "rdesktop -a 16 127.0.0.1:" + str(local_port)
                        subprocess.run(rdesktop_cmd.split())
                if (self.connection == 'SSH'):
                    # VM SSH
                    hostport = None
                    guestport = None
                    # NATNode = ProcessTag.getTagAttributeValue(self.document, 'NAT', 'enabled')
                    ForwardingNum = ProcessTag.getTextNodeValue(self.document, 'ForwardingNum')

                    # for index, value in enumerate(NATNode):
                    #     if value == 'false':
                    #         ForwardingNum[index] = 0

                    # ForwardingName = ProcessTag.getTagAttributeValue(self.document, 'Forwarding', 'name')
                    Forwardinghostport = ProcessTag.getTagAttributeValue(self.document, 'Forwarding', 'hostport')
                    Forwardingguestport = ProcessTag.getTagAttributeValue(self.document, 'Forwarding', 'guestport')
                    print(ForwardingNum)
                    # print(ForwardingName)
                    print(Forwardinghostport)
                    print(Forwardingguestport)
                    AllForwardings = []
                    for index in range(len(Forwardinghostport)):
                        AllForwardings.append((Forwardinghostport[index], Forwardingguestport[index]))
                    print(AllForwardings)
                    Forwarding = []
                    start = 0
                    end = 0
                    for num in ForwardingNum:
                        if num != 0:
                            end = end + int(num)
                            Forwarding.append(AllForwardings[start:end])
                            start = end
                        else:
                            Forwarding.append([])
                    print(Forwarding)
                    machine_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
                    usernameList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'username')
                    passwordList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'password')
                    for index, name in enumerate(machine_name_list):
                        if name == machine_name:
                            for forwarding_entry in Forwarding[index]:
                                if forwarding_entry[1] == '22':
                                    hostport = forwarding_entry[0]
                                    guestport = forwarding_entry[1]
                                    break
                            break
                    if not hostport or not guestport:
                        print("This VM's SSH port hasn't been port forwarded!")
                    else:
                        ssh_thread = DeterTunnelThread(local_port, node_name, exp_name, team_name, hostport, username)
                        ssh_thread.start()
                        check_port_thread = CheckPortThread(local_port)
                        check_port_thread.start()
                        check_port_thread.join(timeout=5)
                        check_port_thread.terminate()
                        ssh_user = usernameList[index]
                        ssh_password = passwordList[index]
                        ssh_password_bytes = ssh_password.encode('utf-8')
                        ssh_password_base64_bytes = base64.b64encode(ssh_password_bytes)
                        ssh_password_base64 = ssh_password_base64_bytes.decode('utf')
                        wssh_port = 8001
                        while Port.is_port_used(local_addr, wssh_port):
                            wssh_port += 1
                        wssh_thread = WSSH_Thread(wssh_port)
                        wssh_thread.start()
                        check_port_thread = CheckPortThread(wssh_port)
                        check_port_thread.start()
                        check_port_thread.join(timeout=5)
                        check_port_thread.terminate()
                        print(
                            f"http://localhost:{wssh_port}/?hostname=localhost&port={local_port}&username={ssh_user}&password={ssh_password_base64}")
                        webbrowser.open(
                            f"http://localhost:{wssh_port}/?hostname=localhost&port={local_port}&username={ssh_user}&password={ssh_password_base64}")

            # node doubleclick
            else:
                print('You double-click the Node')
                node_name = item.text(0)
                if (self.connection == 'Console'):
                    # node VNC
                    if self.platform is None:
                        print("Please select your running platform")
                    else:
                        node_name_list = ProcessTag.getTagAttributeValue(self.document, 'Node', 'name')
                        VNCEnableList = ProcessTag.getTagAttributeValue(self.document, 'VNC', 'enabled')
                        VNCPortList = ProcessTag.getTextNodeValue(self.document, 'VNCPort')
                        exp_name_list = ProcessTag.getTagAttributeValue(self.document, 'Node', 'ExperimentName')
                        team_name_list = ProcessTag.getTagAttributeValue(self.document, 'Node', 'TeamName')

                        for index, value in enumerate(node_name_list):
                            if value == node_name:
                                exp_name = exp_name_list[index]
                                team_name = team_name_list[index]
                                if VNCEnableList[index] == "false":
                                    print('VNC or VNCPort has not been set for this node')
                                    break
                                else:
                                    vnc_port = VNCPortList[index]

                                    ssh_thread = DeterTunnelThread(local_port, node_name, exp_name, team_name, vnc_port,
                                                                   username)
                                    ssh_thread.start()
                                    check_port_thread = CheckPortThread(local_port)
                                    check_port_thread.start()
                                    check_port_thread.join(timeout=5)
                                    check_port_thread.terminate()
                                    if self.platform == 'MacOS':
                                        vnc_cmd = "open vnc://127.0.0.1:" + str(local_port)
                                    elif self.platform == 'Linux':
                                        vnc_cmd = "vncviewer 127.0.0.1:" + str(local_port)
                                    elif self.platform == 'Win':
                                        vnc_cmd = "vncviewer 127.0.0.1:" + str(local_port)
                                    subprocess.run(vnc_cmd.split())
                                    break
                elif (self.connection == 'SSH'):
                    # node SSH
                    # node_user = 'localuser'
                    node_password_bytes = default.DETER_NODE_PASSWORD.encode('utf-8')
                    node_password_base64_bytes = base64.b64encode(node_password_bytes)
                    node_password_base64 = node_password_base64_bytes.decode('utf')
                    guestport = 22
                    node_name_list = ProcessTag.getTagAttributeValue(self.document, 'Node', 'name')
                    exp_name_list = ProcessTag.getTagAttributeValue(self.document, 'Node', 'ExperimentName')
                    team_name_list = ProcessTag.getTagAttributeValue(self.document, 'Node', 'TeamName')

                    # node_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'Node')
                    # exp_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'ExperimentName')
                    # team_name_list = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'TeamName')

                    for index, value in enumerate(node_name_list):
                        if value == node_name:
                            exp_name = exp_name_list[index]
                            team_name = team_name_list[index]
                            break

                    ssh_thread = DeterTunnelThread(local_port, node_name, exp_name, team_name, guestport, username)
                    ssh_thread.start()
                    check_port_thread = CheckPortThread(local_port)
                    check_port_thread.start()
                    check_port_thread.join(timeout=5)
                    check_port_thread.terminate()
                    wssh_port = 8001
                    while Port.is_port_used(local_addr, wssh_port):
                        wssh_port += 1
                    wssh_thread = WSSH_Thread(wssh_port)
                    wssh_thread.start()
                    check_port_thread = CheckPortThread(wssh_port)
                    check_port_thread.start()
                    check_port_thread.join(timeout=5)
                    check_port_thread.terminate()
                    # print("http://localhost:" + str(wssh_port) + "/?hostname=localhost&port=" + str(
                    #     local_port) + "&username=" + default.DETER_NODE_USERNAME + "&password=" + node_password_base64)
                    webbrowser.open("http://localhost:" + str(wssh_port) + "/?hostname=localhost&port=" + str(
                        local_port) + "&username=" + default.DETER_NODE_USERNAME + "&password=" + node_password_base64)
        elif self.target_platform == 'openstack':
            if item.parent():
                # machine doubleclick
                # node_name = item.parent().text(0)
                instance_name = item.text(0)
                project_name = item.text(1)
                domain_name = item.text(2)
                # if (self.platform == 'Linux' or self.platform == 'MacOS'):
                if (self.connection == 'Console'):
                    # VNC
                    if self.platform is None:
                        print("Please select your local running platform")
                    else:
                        InstanceNameList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
                        VNCEnableList = ProcessTag.getTagAttributeValue(self.document, 'VNC', 'enabled')
                        VNCPortList = ProcessTag.getTextNodeValue(self.document, 'VNCPort')
                        ProviderIPList = ProcessTag.getTagAttributeValueWithCondition(self.document, 'Adapter', 'IP',
                                                                                      'name', 'provider')
                        for index, value in enumerate(InstanceNameList):
                            if value == instance_name:
                                if VNCEnableList[index] == "false":
                                    print('VNC or VNCPort has not been set for this node')
                                    break
                                else:
                                    vnc_port = VNCPortList[index]
                                    provider_ip = ProviderIPList[index]
                                    ssh_thread = OpenStackTunnelThread(local_port, provider_ip, vnc_port, username)
                                    ssh_thread.start()
                                    check_port_thread = CheckPortThread(local_port)
                                    check_port_thread.start()
                                    check_port_thread.join(timeout=5)
                                    check_port_thread.terminate()
                                    if self.platform == 'MacOS':
                                        vnc_cmd = "open vnc://127.0.0.1:" + str(local_port)
                                    elif self.platform == 'Linux':
                                        vnc_cmd = "vncviewer 127.0.0.1:" + str(local_port)
                                    elif self.platform == 'Win':
                                        vnc_cmd = "vncviewer 127.0.0.1:" + str(local_port)
                                    # print(vnc_cmd)
                                    subprocess.run(vnc_cmd.split())
                                    break
                if (self.connection == 'SSH'):
                    # SSH
                    if self.platform is None:
                        print("Please select your local running platform")
                    else:
                        InstanceNameList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
                        usernameList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'username')
                        passwordList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'password')
                        ProviderIPList = ProcessTag.getTagAttributeValueWithCondition(self.document, 'Adapter', 'IP',
                                                                                      'name', 'provider')
                        for index, value in enumerate(InstanceNameList):
                            if value == instance_name:
                                provider_ip = ProviderIPList[index]
                                ssh_thread = OpenStackTunnelThread(local_port, provider_ip, 22, username)
                                ssh_thread.start()
                                check_port_thread = CheckPortThread(local_port)
                                check_port_thread.start()
                                check_port_thread.join(timeout=5)
                                check_port_thread.terminate()
                                # web ssh
                                ssh_user = usernameList[index]
                                ssh_password = passwordList[index]
                                ssh_password_bytes = ssh_password.encode('utf-8')
                                ssh_password_base64_bytes = base64.b64encode(ssh_password_bytes)
                                ssh_password_base64 = ssh_password_base64_bytes.decode('utf')
                                wssh_port = 8001
                                while Port.is_port_used(local_addr, wssh_port):
                                    wssh_port += 1
                                wssh_thread = WSSH_Thread(wssh_port)
                                wssh_thread.start()
                                check_port_thread = CheckPortThread(wssh_port)
                                check_port_thread.start()
                                check_port_thread.join(timeout=5)
                                check_port_thread.terminate()
                                print("http://localhost:" + str(wssh_port) + "/?hostname=localhost&port=" + str(
                                    local_port) + "&username=" + ssh_user + "&password=" + ssh_password_base64)
                                webbrowser.open(
                                    "http://localhost:" + str(wssh_port) + "/?hostname=localhost&port=" + str(
                                        local_port) + "&username=" + ssh_user + "&password=" + ssh_password_base64)

                                # cmd ssh
                                # ssh_cmd = "ssh -p " + str(
                                #     local_port)  + " log4shell@localhost"
                                # print(ssh_cmd)
                                # subprocess.run(ssh_cmd.split())
                                break
            else:
                # project doubleclick
                print(f"You've double click the project")
    def Populate(self, Node_QTreeWidgetItem):
        HeaderLabels = {'deter': ["Machine Name", "Experiment Name", "Team Name"],
                        'openstack': ["Instance Name", "Project Name", "Domain Name"]}
        if self.target_platform is None:
            self.ui.treeWidget.setHeaderLabels(["", "", ""])
        else:
            self.ui.treeWidget.setHeaderLabels(HeaderLabels[self.target_platform])
        self.ui.treeWidget.resize(600, 400)
        self.ui.treeWidget.setColumnCount(3)
        self.ui.treeWidget.addTopLevelItems(Node_QTreeWidgetItem)

    def openFile(self, file_path):
        if os.path.exists(file_path):
            path = QFileDialog.getOpenFileName(self, "Open File Dialog", file_path, "XML files(*.xml)")
        else:
            path = QFileDialog.getOpenFileName(self, "Open File Dialog", "/", "XML files(*.xml)")
        print(path)
        self.document = IOXML.parseXML(str(path[0]))
        self.target_platform = ProcessTag.getRootElementAttributeValue(self.document, 'platform')
        # self.CVE = ProcessTag.getRootElementAttributeValue(self.document, 'CVE')
        self.url = ProcessTag.getRootElementAttributeValue(self.document, 'url')
        # self.updateQTreeWidgetItem()
        # self.browser.load(QUrl(self.url))
        # self.browser.show()

    def confirm(self, file_path):
        print('Confirm Clicked!')
        self.updateQTreeWidgetItem()
        # print(f"Currently: {self.CVE}")

    def tutorial(self, file_path):
        print('Tutorial Clicked!')
        self.browser.load(QUrl(self.url))
        self.browser.show()

    def reset(self, file_path):
        # vncserver -localhost no :1
        # vncserver -kill :1
        # vncserver -list
        print('ResetVNC Clicked!')
        username = self.ui.lineEdit.text()
        local_addr = '127.0.0.1'
        local_port = 12345
        while Port.is_port_used(local_addr, local_port):
            local_port += 1

        # reset_ssh_cmd = f"vncserver -kill :1; vncserver -localhost no :1"
        reset_ssh_cmd = f"vncserver -kill :1; vncserver -localhost no :1"

        if self.target_platform == 'openstack':
            if self.instance_selected is None:
                print("Please select the machine that you want to reset")
            else:
                InstanceNameList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'name')
                usernameList = ProcessTag.getTagAttributeValue(self.document, 'Machine', 'username')
                ProviderIPList = ProcessTag.getTagAttributeValueWithCondition(self.document, 'Adapter', 'IP',
                                                                              'name', 'provider')

                for index, value in enumerate(InstanceNameList):
                    if value == self.instance_selected:
                        provider_ip = ProviderIPList[index]
                        ssh_user = usernameList[index]
                        ssh_thread = OpenStackTunnelThread(local_port, provider_ip, 22, username)
                        ssh_thread.start()
                        check_port_thread = CheckPortThread(local_port)
                        check_port_thread.start()
                        check_port_thread.join(timeout=5)
                        check_port_thread.terminate()
                        ssh_resetvnc_cmd = f"ssh -p {local_port} {ssh_user}@127.0.0.1 {reset_ssh_cmd}"
                        print(ssh_resetvnc_cmd)
                        subprocess.run(ssh_resetvnc_cmd.split())
                        # process = subprocess.Popen(ssh_resetvnc_cmd, shell=True, stdout=subprocess.PIPE)
                        # process.wait()
                        # print(f"return code:{process.returncode}")
                        break
        elif self.target_platform == 'deter':
            pass

    def runscript(self, file_path):
        print('Nothing Happens!')

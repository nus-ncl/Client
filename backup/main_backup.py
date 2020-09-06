import sys
import subprocess
import random
from ProcessTag import *
from Port import *
from IOXML import *
from PySide2 import QtWidgets, QtCore
# from PySide2.QtCore import QFile, QFileInfo, QIODevice,QTextStream
from PySide2.QtXml import (QDomNode)

# from tool_backup import Ui_MainWindow
# from tool import Ui_MainWindow
from backup.ScrollUI_backup import Ui_MainWindow

# class myMainWindow(QtWidgets.QMainWindow,QtWidgets.QWidget,Ui_MainWindow):
class myMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    # tunnel_pid=0
    # local_port=0

    def __init__(self,Node_QTreeWidgetItem,document,Machine):
        super(myMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Populate(Node_QTreeWidgetItem)
        self.TagName = "VRDEProperties"
        self.Attributes = ["name", "value"]
        self.vrde_port={}
        try:
            self.output = processTagName(document, self.TagName, self.Attributes)
            for i in range(len(Machine)):
                self.vrde_port[Machine[i]] = self.output[1][2*i+1]
            print(self.vrde_port)

        except ValueError as e:
            print("Failed to import: {0}".format(e))


    def tunnel(self):
        username=self.ui.lineEdit.text()
        group=self.ui.comboBox_2.currentText()
        self.local_port=self.ui.lineEdit_3.text()
        vm=self.ui.comboBox.currentText()
        vm_relay_port={'Ubuntu1':'11001','Ubuntu2':'11002','Ubuntu3':'11003','Ubuntu4':'11004','Kali1':'11021','Kali2':'11022'}
        ssh_cmd = "ssh -N -L "+ self.local_port + ":n1"+".Exp" + group + ".CS4238-19-01.ncl.sg:"+ vm_relay_port[vm] + " " +username + "@users.ncl.sg"
        print(ssh_cmd)
        pro1 = subprocess.Popen(ssh_cmd.split())
        self.tunnel_pid=pro1.pid
        print(self.tunnel_pid)
        print("done")

    def detunnel(self):
        subprocess.run(("kill -9 "+ str(self.tunnel_pid)).split())
    def rdesktop(self):
        subprocess.run(("rdesktop -a 16 localhost:"+ self.local_port).split())
    def click(self):
        print("You click!")
    def doubleclick(self,item,col):
        username = self.ui.lineEdit.text()
        local_addr='127.0.0.1'
        local_port = 12345
        while(is_port_used(local_addr,local_port)):
            local_port += 1
        node = item.parent().text(0)
        exp = item.text(1)
        team = item.text(2)
        machine = item.text(0)
        ssh_cmd = "ssh -N -L " + str(local_port) + ":" + node + "." + exp + "." + team + ".ncl.sg:" + self.vrde_port[machine] + " " + username + "@users.ncl.sg"
        print(ssh_cmd)
        # pro1 = subprocess.Popen(ssh_cmd.split())
        # self.tunnel_pid = pro1.pid
        # print(self.tunnel_pid)
        # print("done")
        # time.sleep(10)
        # print("You doubleclick! {},{},{},{},{}".format(item.text(0),item.parent().text(0),item.text(1),item.text(2),col))
        # subprocess.run(("rdesktop -a 16 localhost:" + str(local_port)).split())

        # subprocess.run(("kill -9 " + str(self.tunnel_pid)).split())

class TreeWidget(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setWindowTitle('TreeWidget')
        #创建一个Qtree部件
        self.tree = QtWidgets.QTreeWidget()
        #设置部件的列数为2
        self.tree.setColumnCount(2)
        #设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.tree.setHeaderLabels(['Key','Value'])

        #设置root为self.tree的子树，所以root就是跟节点
        root= QtWidgets.QTreeWidgetItem(self.tree)
        #设置根节点的名称
        root.setText(0,'root')

        #为root节点设置子结点
        child1 = QtWidgets.QTreeWidgetItem(root)
        child1.setText(0,'child1')
        child1.setText(1,'name1')
        child2 = QtWidgets.QTreeWidgetItem(root)
        child2.setText(0,'child2')
        child2.setText(1,'name2')
        child3 = QtWidgets.QTreeWidgetItem(root)
        child3.setText(0,'child3')
        child4 = QtWidgets.QTreeWidgetItem(child3)
        child4.setText(0,'child4')
        child4.setText(1,'name4')

        self.tree.addTopLevelItem(root)
        #将tree部件设置为该窗口的核心框架
        self.setCentralWidget(self.tree)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.hello1= ["Hello World", "你好，世界"]
        self.hello2 = ["World Hello", "世界，你好"]
        self.button1 = QtWidgets.QPushButton("Click me!")
        self.button2 = QtWidgets.QPushButton("Click me 2!")
        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button1.clicked.connect(self.magic1)
        self.button2.clicked.connect(self.magic2)

    @QtCore.Slot()
    def magic1(self):
        self.text.setText(random.choice(self.hello1))
    def magic2(self):
        self.text.setText(random.choice(self.hello2))


def populateFromDOM(document):
    # documentElement() returns the root element
    root = document.documentElement()
    if root.tagName() != "VM":
        raise ValueError("not a Movies XML file")
    node = root.firstChild()

    while not node.isNull():
        element = node.toElement()
        if not element.isNull():
            # read specified node
            readNode(element)
        node = node.nextSibling()
    # add new sibling of specified node
    addNode(document, element)
    # print(document.toString())

def getText(node):
    child = node.firstChild()
    text = ""
    while not child.isNull():
        if child.nodeType() == QDomNode.TextNode:
            text += child.toText().data()
        child = child.nextSibling()
    return text.strip()

def readNode(element):
    Name = element.attribute("name")
    OSType = element.attribute("OSType")
    Node_list = element.attribute("Node").split('-')
    if len(Node_list) != 2:
        raise ValueError("invalid Node Index {0}".format(str(element.attribute("Node"))))
    Node = str(element.attribute("Node"))
    # title = notes = None
    # node = element.firstChild()
    # while title is None or notes is None:
    #     if node.isNull():
    #         raise ValueError("missing title or notes")
    #     if node.toElement().tagName() == "TITLE":
    #         title = getText(node)
    #     elif node.toElement().tagName() == "NOTES":
    #         notes = getText(node)
    #     node = node.nextSibling()
    #     print("title={},notes={}".format(title,notes))
    # if not title:
    #     raise ValueError("missing title")
    print(Name,OSType,Node_list,Node)


if __name__ == '__main__':
    TagName = "VM"
    Attributes = ["name","Node","ExperimentName","TeamName"]
    document = importXmlDOM("/Users/hkwany/PycharmProjects/Client/VM_1.xml")
    try:
        output=processTagName(document, TagName, Attributes)
        print(output)
    except ValueError as e:
        print("Failed to import: {0}".format(e))
    app = 0
    if QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    Machine = output[0]
    Node = output[1]
    Exp = output[2]
    Team = output[3]

    # print([Machine[0],Exp[0],Team[0]])
    Node_set = list(set(Node))
    Node_set.sort()

    Node_QTreeWidgetItem = []
    for i in range(len(Node_set)):
        Node_QTreeWidgetItem.append(QtWidgets.QTreeWidgetItem(Node_set[i:i + 1]))

    for i in range(len(Machine)):
        Node_Belong_To = Node_set.index(Node[i])
        child = QtWidgets.QTreeWidgetItem([Machine[i],Exp[i],Team[i]])
        Node_QTreeWidgetItem[Node_Belong_To].addChild(child)
        # l1_child = QtWidgets.QTreeWidgetItem(["Nginx" + str(i)])
        # l1.addChild(l1_child)

    # w = QtWidgets.QWidget()
    # w.resize(400, 200)
    # myTreeWidget = MyTreeWidget(w, Node_QTreeWidgetItem)
    # w.show()
    # sys.exit(app.exec_())


    # movie = Movie()
    # export_xml_file_name="/Users/hkwany/PycharmProjects/Client/export.xml"
    # exportXml(export_xml_file_name,movie)

    # Rdesktop Tool
    # app = QtWidgets.QApplication(sys.argv)
    # print(Machine)
    window = myMainWindow(Node_QTreeWidgetItem,document,Machine)
    window.show()
    sys.exit(app.exec_())


    # unfold root directory
    # app = QtWidgets.QApplication(sys.argv)
    # model = QtWidgets.QDirModel()
    # tree = QtWidgets.QTreeView()
    # tree.setModel(model)
    # tree.setWindowTitle(tree.tr("Dir View"))
    # tree.resize(640, 480)
    # tree.show()
    # sys.exit(app.exec_())


    # Two Buttons
    # app = QtWidgets.QApplication(sys.argv)
    # widget = MyWidget()
    # widget.resize(800, 600)
    # widget.show()
    # sys.exit(app.exec_())


    # 3-column QTreeWidget




from PySide2 import QtWidgets


class MyTreeWidget():
	def __init__(self, Qwidget, Node_QTreeWidgetItem):
		self.tw = QtWidgets.QTreeWidget(Qwidget)
		self.tw.resize(400, 200)
		self.tw.setColumnCount(3)
		self.tw.setHeaderLabels(["Column 1", "Column 2", "Column 3"])
		# L=[l1,l2]
		# tw.addTopLevelItem(l1)
		# tw.addTopLevelItem(l2)
		self.tw.addTopLevelItems(Node_QTreeWidgetItem)
		# self.tw.expandAll()
		self.tw.itemDoubleClicked.connect(self.onItemClicked)

		# self.tw.itemClicked.connect(self.onItemClicked)

	def onItemClicked(self, item):
		# item = QtWidgets.QTreeWidgetItem()
		# item.
		print("You Clicked!")

	# @staticmethod
	# def processTagNameAttributes(document, TagName, Attributes):
	# 	'''
	# 	:param document: QDomDocument()
	# 	:param TagName: <TagName>
	# 	:param Attributes: [attribute_1,attribute_2,...]
	# 		<TagName attribute_1="" attribute_2="" ... />
	# 	'''
	# 	output = []
	# 	for row in range(len(Attributes)):
	# 		output.append([])
	# 	TagName_list = document.elementsByTagName(TagName)
	# 	# print('Machine:')
	# 	for i in range(TagName_list.length()):
	# 		propertyNode = TagName_list.at(i)
	# 		propertyElement = propertyNode.toElement()
	# 		if (propertyElement):
	# 			for row in range(len(Attributes)):
	# 				# print(propertyElement.attribute(Attributes[row]),end='  ')
	# 				output[row].append(propertyElement.attribute(Attributes[row]))
	# 		else:
	# 			for row in range(len(Attributes)):
	# 				output[row].append(None)
	# 	# print()
	# 	# print(output)
	# 	return output

	# @staticmethod
	# def processTagName(document, TagName, Attributes):
	# 	'''
	# 	:param document: QDomDocument()
	# 	:param TagName: <TagName>
	# 	:param Attributes: [attribute_1,attribute_2,...]
	# 	<TagName>
	# 		<ChildTagName attribute_1="" attribute_2="" ... />
	# 	'''
	# 	output = []
	# 	for row in range(len(Attributes)):
	# 		output.append([])
	# 	if (TagName == "VM"):
	# 		output = processTagNameAttributes(document, "Machine", Attributes)
	# 		return output
	# 	else:
	# 		TagName_list = document.elementsByTagName(TagName)
	# 		for i in range(TagName_list.length()):
	# 			propertyNode = TagName_list.at(i).firstChild()
	# 			# print('Machine:{}->'.format(i))
	# 			while not propertyNode.isNull():
	# 				# print("has child!")
	# 				propertyElement = propertyNode.toElement()
	# 				if (propertyElement):
	# 					# print("has tag attribute!")
	# 					for row in range(len(Attributes)):
	# 						# print(propertyElement.attribute(attribute),end='  ')
	# 						output[row].append(propertyElement.attribute(Attributes[row]))
	# 				# print()
	# 				else:
	# 					# print("no tag attribute!")
	# 					for row in range(len(Attributes)):
	# 						output[row].append(None)
	# 				propertyNode = propertyNode.nextSibling()
	# 		return output
	# rootElement = document.documentElement()
	# childNode = rootElement.firstChild()
	# while not (childNode.isNull()):
	#     element = childNode.toElement()
	#     if (element):
	#         print('Machine:{}  OSType:{}  Node:{}'.format(element.attribute("name"),
	#                                                       element.attribute("OSType"),
	#                                                       element.attribute("Node")))
	#
	#         nodeList = element.childNodes()
	#         # Hardware,Software
	#         for i in range(nodeList.count()):
	#             node = nodeList.at(i)
	#             print("{}:".format(node.toElement().tagName()))
	#
	#     childNode = childNode.nextSibling()
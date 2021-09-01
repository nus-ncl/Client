from xml.dom import minidom
import os

# def printDocument(document):
# 	print(document.toString())

# def getGlobalTagAttribute(document, TagName, Attribute):
# 	'''
# 	Traverse all the global document to get the Attribution's value belonging to TagName
# 	:param document:
# 	:param TagName:
# 	:param Attribute:
# 	:return:
# 	'''
#
# 	output=[]
# 	# Return root element of the document <VM>
# 	RootElement = document.documentElement()
# 	# Return first <Machine>
# 	Machine = RootElement.firstChild()
# 	while not Machine.isNull():
# 		# print(Machine.toElement().attribute('name')+':')
# 		# Maybe there're many identical TagName at the same time, so they contruct a list
# 		TagName_list = Machine.toElement().elementsByTagName(TagName)
# 		for i in range(TagName_list.length()):
# 			output.append(TagName_list.at(i).toElement().attribute(Attribute))
# 			# print(TagName_list.at(i).toElement().attribute(Attribute))
# 		Machine = Machine.nextSibling()
# 	return output
#
# def getGlobalNodeTagAttributes(document, NodeName, TagName, Attributes):
# 	'''
# 	Traverse all the global document to get the Attribution's value belonging to TagName
# 	:param document:
# 	:param TagName:
# 	:param Attributes:
# 	:return:
# 	'''
#
# 	# output=[]
# 	output_dict = {}
# 	# Return root element of the document <VM>
# 	RootElement = document.documentElement()
# 	# Return first <Machine>
# 	Machine = RootElement.firstChild()
# 	# print(type(Machine))
# 	while not Machine.isNull():
# 		machine_name = Machine.toElement().attribute("name")
# 		output_dict[machine_name]=[]
# 		# print(Machine.toElement().attribute('name')+':')
# 		# Maybe there're many identical TagName at the same time, so they contruct a list
# 		Node_list = Machine.toElement().elementsByTagName(NodeName)
# 		TagName_list = Node_list.at(0).toElement().elementsByTagName(TagName)
# 		# print(type(TagName_list))
# 		# print(TagName_list.length())
# 		# print(TagName_list)
# 		for i in range(TagName_list.length()):
# 			output = {}
# 			for attribute in Attributes:
# 				# print(attribute)
# 				output[attribute]=TagName_list.at(i).toElement().attribute(attribute)
# 				# print(output)
# 			output_dict[machine_name].append(output)
# 			# print(output_dict)
# 			# print(TagName_list.at(i).toElement().attribute(Attribute))
# 		# print(output)
# 		Machine = Machine.nextSibling()
# 	# print(output_dict)
# 	return output_dict
#
# def getlocalTagNameAttribute(document, TagName, Attribute, specifier):
# 	'''
# 	Traverse all the local part of document to get the Attribution's value belonging to TagName
# 	:param document:
# 	:param TagName:
# 	:param Attribute:
# 	:param specifier: Machine's name attribution
# 	:return:
# 	'''
#
# 	output=[]
# 	# Return root element of the document <VM>
# 	RootElement = document.documentElement()
# 	# Return first <Machine>
# 	Machine = RootElement.firstChild()
# 	while not Machine.isNull():
# 		name = Machine.toElement().attribute('name')
# 		if name == specifier:
# 			# Maybe there're many identical TagName at the same time, so they contruct a list
# 			TagName_list = Machine.toElement().elementsByTagName(TagName)
# 			for i in range(TagName_list.length()):
# 				output.append(TagName_list.at(i).toElement().attribute(Attribute))
# 			break
# 		else:
# 			Machine = Machine.nextSibling()
# 	return output
#
# def getGlobalMachineAttribute(document, TagName, Attribute):
# 	'''
# 	Traverse all the global document to get the Attribution's value belonging to TagName
# 	:param document:
# 	:param TagName:
# 	:param Attribute:
# 	:return:
# 	'''
#
# 	output=[]
# 	# Return root element of the document <VM>
# 	RootElement = document.documentElement()
# 	# Return first <Machine>
# 	Machine = RootElement
# 	if not Machine.isNull():
# 		# print(Machine.toElement().attribute('name')+':')
# 		# Maybe there're many identical TagName at the same time, so they contruct a list
# 		TagName_list = Machine.toElement().elementsByTagName(TagName)
# 		for i in range(TagName_list.length()):
# 			output.append(TagName_list.at(i).toElement().attribute(Attribute))
# 			# print(TagName_list.at(i).toElement().attribute(Attribute))
# 		# Machine = Machine.nextSibling()
# 	return output
#
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
#
#
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
#
# def getText(node):
# 	return node.firstChild.getAttribute('text')
def XML_Parser(document, TagName, Attribute):
	'''
	Traverse all the global document to get the Attribution's value belonging to TagName
	:param document:
	:param TagName:
	:param Attribute:
	:return:
	'''

	output=[]
	# Return root element of the document <VM>
	RootElement = document.documentElement()
	# Return first <Machine>
	Machine = RootElement.firstChild()
	while not Machine.isNull():
		# print(Machine.toElement().attribute('name')+':')
		# Maybe there're many identical TagName at the same time, so they contruct a list
		TagName_list = Machine.toElement().elementsByTagName(TagName)
		for i in range(TagName_list.length()):
			output.append(TagName_list.at(i).toElement().attribute(Attribute))
		# print(TagName_list.at(i).toElement().attribute(Attribute))
		Machine = Machine.nextSibling()
	return output

def getTagAttributeValue(document, tagName, attributeName):
	output = []
	rootElement = document.documentElement
	nodeList = rootElement.getElementsByTagName(tagName)
	for node in nodeList:
		attributeValue = node.getAttribute(attributeName)
		if attributeValue:
			output.append(attributeValue)
		else:
			output.append(None)

	return output

def getTagAttributeValueWithCondition(document, tagName, attributeName, conditionattributeName, conditionattributeValue):
	output = []
	rootElement = document.documentElement
	nodeList = rootElement.getElementsByTagName(tagName)
	for node in nodeList:
		if node.getAttribute(conditionattributeName) == conditionattributeValue:
			attributeValue = node.getAttribute(attributeName)
			if attributeValue:
				output.append(attributeValue)
			else:
				output.append(None)

	return output

def getTextNodeValue(document, tagName):
	output = []
	rootElement = document.documentElement
	nodeList = rootElement.getElementsByTagName(tagName)
	for node in nodeList:
		output.append(node.childNodes[0].nodeValue)

	return output

if __name__ == '__main__':
	xml_file_path=os.path.abspath("client.xml")
	dom_obj=minidom.parse(xml_file_path)
	machines = dom_obj.getElementsByTagName("Machine")
	for machine in machines:
		print(machine.getAttribute('name'))
		port_forwardings = machine.getElementsByTagName("Port_Forwarding")
		port_forwarding = port_forwardings[0]
		# for port_forwarding in port_forwardings:
		forwarding = port_forwarding.getElementsByTagName('Forwarding')
		if len(forwarding) == 0:
			print('Not Exist')
		else:
			for element in forwarding:
				print(f"hostport:{element.getAttribute('hostport')},guestport:{element.getAttribute('guestport')}")
		print('----')



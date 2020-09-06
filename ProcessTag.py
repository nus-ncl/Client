import IOXML

def printDocument(document):
	print(document.toString())

def getGlobalTagNameAttribute(document, TagName, Attribute):
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

def getlocalTagNameAttribute(document, TagName, Attribute, specifier):
	'''
	Traverse all the local part of document to get the Attribution's value belonging to TagName
	:param document:
	:param TagName:
	:param Attribute:
	:param specifier: Machine's name attribution
	:return:
	'''

	output=[]
	# Return root element of the document <VM>
	RootElement = document.documentElement()
	# Return first <Machine>
	Machine = RootElement.firstChild()
	while not Machine.isNull():
		name = Machine.toElement().attribute('name')
		if name == specifier:
			# Maybe there're many identical TagName at the same time, so they contruct a list
			TagName_list = Machine.toElement().elementsByTagName(TagName)
			for i in range(TagName_list.length()):
				output.append(TagName_list.at(i).toElement().attribute(Attribute))
			break
		else:
			Machine = Machine.nextSibling()
	return output

def getGlobalMachineAttribute(document, TagName, Attribute):
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
	Machine = RootElement
	if not Machine.isNull():
		# print(Machine.toElement().attribute('name')+':')
		# Maybe there're many identical TagName at the same time, so they contruct a list
		TagName_list = Machine.toElement().elementsByTagName(TagName)
		for i in range(TagName_list.length()):
			output.append(TagName_list.at(i).toElement().attribute(Attribute))
			# print(TagName_list.at(i).toElement().attribute(Attribute))
		# Machine = Machine.nextSibling()
	return output

def processTagNameAttributes(document, TagName, Attributes):
	'''
	:param document: QDomDocument()
	:param TagName: <TagName>
	:param Attributes: [attribute_1,attribute_2,...]
		<TagName attribute_1="" attribute_2="" ... />
	'''
	output = []
	for row in range(len(Attributes)):
		output.append([])
	TagName_list = document.elementsByTagName(TagName)
	# print('Machine:')
	for i in range(TagName_list.length()):
		propertyNode = TagName_list.at(i)
		propertyElement = propertyNode.toElement()
		if (propertyElement):
			for row in range(len(Attributes)):
				# print(propertyElement.attribute(Attributes[row]),end='  ')
				output[row].append(propertyElement.attribute(Attributes[row]))
		else:
			for row in range(len(Attributes)):
				output[row].append(None)
	# print()
	# print(output)
	return output


def processTagName(document, TagName, Attributes):
	'''
	:param document: QDomDocument()
	:param TagName: <TagName>
	:param Attributes: [attribute_1,attribute_2,...]
	<TagName>
		<ChildTagName attribute_1="" attribute_2="" ... />
	'''
	output = []
	for row in range(len(Attributes)):
		output.append([])
	if (TagName == "VM"):
		output = processTagNameAttributes(document, "Machine", Attributes)
		return output
	else:
		TagName_list = document.elementsByTagName(TagName)
		for i in range(TagName_list.length()):
			propertyNode = TagName_list.at(i).firstChild()
			# print('Machine:{}->'.format(i))
			while not propertyNode.isNull():
				# print("has child!")
				propertyElement = propertyNode.toElement()
				if (propertyElement):
					# print("has tag attribute!")
					for row in range(len(Attributes)):
						# print(propertyElement.attribute(attribute),end='  ')
						output[row].append(propertyElement.attribute(Attributes[row]))
				# print()
				else:
					# print("no tag attribute!")
					for row in range(len(Attributes)):
						output[row].append(None)
				propertyNode = propertyNode.nextSibling()
		return output

if __name__ == '__main__':
	document = IOXML.importXmlDOM("client.xml")
	print(getGlobalMachineAttribute(document,'Machine','name'))
	print(getGlobalMachineAttribute(document,'Machine','Node'))
	print(getGlobalMachineAttribute(document,'Machine','ExperimentName'))
	print(getGlobalMachineAttribute(document,'Machine','TeamName'))

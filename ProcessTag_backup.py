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
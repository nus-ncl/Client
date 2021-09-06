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



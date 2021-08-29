from PySide2.QtXml import (QDomDocument)
from PySide2.QtCore import QFile, QFileInfo, QIODevice, QTextStream
from xml.dom import minidom


def importXmlDOM(filename):
	'''
	The QDomDocument class represents the entire XML document
	The DOM classes that will be used most often are QDomNode , QDomDocument , QDomElement and QDomText
	The DOM tree might end up reserving a lot of memory if the XML document is big. For such documents,
	the QXmlStreamReaderor the QXmlQuery classes might be better solutions.
	:param filename: filename_path
	:return: document
	'''

	document = QDomDocument()
	error = None
	file = None
	try:
		# instantiate a device(QFile) specified by filename
		file = QFile(filename)
		if not file.open(QIODevice.ReadOnly):
			raise IOError(str(file.errorString()))
		# setContent parses an XML file and creates the DOM tree that represents the document
		if not document.setContent(file):
			raise ValueError("could not parse XML")
	except (IOError, OSError, ValueError) as e:
		error = "Failed to import: {0}".format(e)
	finally:
		if file is not None:
			file.close()
		if error is not None:
			print(error)
		return document


# TODO: export and insert
def exportXml(fname):
	# Generate Document Object Model Tree
	DOMTree = minidom.Document()

	# Generate and set all Elements and TextNodes
	rootElement = DOMTree.createElement('Root')
	emptyChild = DOMTree.createElement('emptyChild')
	aChild = DOMTree.createElement('aChild')
	aChild.setAttribute('attribute1', 'value1')
	aChild.setAttribute('attribute2', 'value2')

	bChild = DOMTree.createElement('bChild')
	bChild.setAttribute('attribute', 'value')

	cChild = DOMTree.createElement('cChild')
	cChild.setAttribute('Attribute', 'Value')

	dChild = DOMTree.createElement('dChild')
	eChild = DOMTree.createElement('eChild')
	fChild = DOMTree.createElement('fChild')

	TextNode1 = DOMTree.createTextNode('Text1')
	TextNode2 = DOMTree.createTextNode('Text2')
	TextNode3 = DOMTree.createTextNode('Text3')
	TextNode4 = DOMTree.createTextNode('Text4')

	# rootElement is appended to the DOMTree
	DOMTree.appendChild(rootElement)
	# first-level tags are appended to the rootElement
	rootElement.appendChild(aChild)
	rootElement.appendChild(bChild)
	rootElement.appendChild(cChild)
	rootElement.appendChild(emptyChild)

	# second-level tags are appended to the first-level tags
	aChild.appendChild(TextNode1)

	bChild.appendChild(dChild)
	dChild.appendChild(TextNode2)

	cChild.appendChild(eChild)
	eChild.appendChild(TextNode3)
	cChild.appendChild(fChild)
	fChild.appendChild(TextNode4)

	xml_str = DOMTree.toprettyxml(indent="\t", encoding="utf-8")

	saved_file = f'{fname}.xml'

	with open(saved_file, "wb") as f:
		f.write(xml_str)


if __name__ == '__main__':
	exportXml('new')

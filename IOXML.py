from PySide2.QtXml import (QDomDocument)
from PySide2.QtCore import QFile, QFileInfo, QIODevice, QTextStream


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
def exportXml(fname, movie):
	CODEC = "UTF-8"
	error = None
	fh = None
	try:
		fh = QFile(fname)
		if not fh.open(QIODevice.WriteOnly):
			raise IOError(str(fh.errorString()))
		stream = QTextStream(fh)
		stream.setCodec(CODEC)
		stream << ("<?xml version='1.0' encoding='{0}'?>\n"
		           "<!DOCTYPE MOVIES>\n"
		           "<MOVIES VERSION='1.0'>\n".format(CODEC))
		stream << ("<MOVIE YEAR='{0}' MINUTES='{1}' "
		           "ACQUIRED='{2}'>\n".format(movie.year,
		                                      movie.minutes,
		                                      movie.acquired)) \
		<< "<TITLE>" << movie.title \
		<< "</TITLE>\n<NOTES>"
		if movie.notes:
			stream << "\n" << movie.notes
		stream << "\n</NOTES>\n</MOVIE>\n"
		stream << "</MOVIES>\n"
	except EnvironmentError as e:
		error = "Failed to export: {0}".format(e)
	finally:
		if fh is not None:
			fh.close()
		if error is not None:
			print(error)
		print("Exported 1 movie records to {0}".format(
			QFileInfo(fname).fileName()))


# def addNode(document,element):
#     newElement = document.createElement("Machine")
#     newElement.setAttribute("name","Nginx4")
#     # element.appendChild(newElement)
#     pass

# def populateFromDOM(dom):
#     root = dom.documentElement()
#     # print(root.attribute("VERSION"))
#     if root.tagName() != "MOVIES":
#         raise ValueError("not a Movies XML file")
#     node = root.firstChild()
#
#     while not node.isNull():
#         if node.toElement().tagName() == "MOVIE":
#             readMovieNode(node.toElement())
#         node = node.nextSibling()
#
# def readMovieNode(element):
#     def getText(node):
#         child = node.firstChild()
#         text = ""
#         while not child.isNull():
#             if child.nodeType() == QDomNode.TextNode:
#                 text += child.toText().data()
#             child = child.nextSibling()
#         return text.strip()
#
#     year = int(element.attribute("YEAR"))
#     minutes = int(element.attribute("MINUTES"))
#     ymd = element.attribute("ACQUIRED").split("-")
#     if len(ymd) != 3:
#         raise ValueError("invalid acquired date {0}".format(
#             str(element.attribute("ACQUIRED"))))
#     acquired = datetime.date(int(ymd[0]), int(ymd[1]),
#                              int(ymd[2]))
#     title = notes = None
#     node = element.firstChild()
#     while title is None or notes is None:
#         if node.isNull():
#             raise ValueError("missing title or notes")
#         if node.toElement().tagName() == "TITLE":
#             title = getText(node)
#         elif node.toElement().tagName() == "NOTES":
#             notes = getText(node)
#         node = node.nextSibling()
#         # print('1',node.toElement().attribute("TITLE"))
#         # print('2',node.toElement().attribute("NOTES"))
#         print("title={},notes={}".format(title,notes))
#     if not title:
#         raise ValueError("missing title")
#     print(title, year, minutes, acquired, notes)

# def importSAX(self, fname):
#     error = None
#     fh = None
#     try:
#         handler = SaxMovieHandler(self)
#         parser = QXmlSimpleReader()
#         parser.setContentHandler(handler)
#         parser.setErrorHandler(handler)
#         fh = QFile(fname)
#         input = QXmlInputSource(fh)
#         if not parser.parse(input):
#             raise ValueError(handler.error)
#     except (IOError, OSError, ValueError) as e:
#         error = "Failed to import: {0}".format(e)
#     finally:
#         if fh is not None:
#             fh.close()
#         if error is not None:
#             print(error)
#         self.__fname = ""
#         print("Imported 1 movie records from {0}".format(
#                 QFileInfo(fname).fileName()))

# class SaxMovieHandler(QXmlDefaultHandler):
#
#     def __init__(self, movies):
#         super(SaxMovieHandler, self).__init__()
#         self.movies = movies
#         self.text = ""
#         self.error = None
#
#     def clear(self):
#         self.year = None
#         self.minutes = None
#         self.acquired = None
#         self.title = None
#         self.notes = None
#
#     def startElement(self, namespaceURI, localName, qName, attributes):
#         if qName == "MOVIE":
#             self.clear()
#             self.year = int(attributes.value("YEAR"))
#             self.minutes = int(attributes.value("MINUTES"))
#             ymd = attributes.value("ACQUIRED").split("-")
#             if len(ymd) != 3:
#                 raise ValueError("invalid acquired date {0}".format(
#                     str(attributes.value("ACQUIRED"))))
#             self.acquired = datetime.date(int(ymd[0]),
#                                           int(ymd[1]), int(ymd[2]))
#         elif qName in ("TITLE", "NOTES"):
#             self.text = ""
#         return True
#
#     def characters(self, text):
#         self.text += text
#         return True
#
#     def endElement(self, namespaceURI, localName, qName):
#         if qName == "MOVIE":
#             if (self.year is None or self.minutes is None or
#                     self.acquired is None or self.title is None or
#                     self.notes is None or not self.title):
#                 raise ValueError("incomplete movie record")
#             print(self.title, self.year,
#                   self.minutes, self.acquired,
#                   decodedNewlines(self.notes))
#
#         elif qName == "TITLE":
#             self.title = self.text.strip()
#         elif qName == "NOTES":
#             self.notes = self.text.strip()
#         return True
#
#     def fatalError(self, exception):
#         self.error = "parse error at line {0} column {1}: {2}".format(
#             exception.lineNumber(), exception.columnNumber(),
#             exception.message())
#         return False


if __name__ == '__main__':
	doc = importXmlDOM("client.xml")
	# Return root element of the document <VM>
	docElem = doc.documentElement()
	print(docElem.nodeType())
	print(doc.toString())
	# elements = doc.elementsByTagNa
	node = docElem.firstChild()
	while not node.isNull():
		print(node.toElement().attribute('name'))
		vrdeport = node.toElement().elementsByTagName('vrdeport')
		for i in range(vrdeport.length()):
			print(vrdeport.at(i).toElement().attribute('value'))
		node = node.nextSibling()


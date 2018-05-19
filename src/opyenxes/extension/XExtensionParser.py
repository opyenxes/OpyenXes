from opyenxes.extension.XExtension import XExtension
from opyenxes.utils.SingletonClassGenerator import XExtensionMetaclass
from xml.sax.handler import ContentHandler
from xml.sax import parse as xml_parse, parseString
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.id.XIDFactory import XIDFactory
from urllib import request, parse, error
import os


class XExtensionParser(metaclass=XExtensionMetaclass):
    """Parser for extension definition files.

    Uses the singleton metaclass
    """

    class XExtensionHandler(ContentHandler):
        """SAX handler class for extension definition files.

        """
        def __init__(self):
            super().__init__()
            self.__extension = None
            self.__currentAttribute = None
            self.__xAttributes = None
            self.__factory = XFactoryRegistry().current_default()
            self.reset()

        def reset(self):
            """Resets the handler to initial state.

            """
            self.__extension = None
            self.__currentAttribute = None
            self.__xAttributes = None
            self.__factory = XFactoryRegistry().current_default()

        def get_extension(self):
            """Retrieves the parsed extension after parsing.

            :return: The parsed extension.
            :rtype: `XExtension`
            """
            return self.__extension

        def startElement(self, name, attributes):
            """ Overrides startElement in class ContentHandler

            :param name:  Contains the raw XML 1.0 name of the element type
            :type name: str
            :param attributes: An instance of the Attributes class containing
             the attributes of the element
            :type attributes: xml.sax.xmlreader.AttributesImpl
            """
            tag_name = name

            if tag_name.lower() == "xesextension":
                mapping = attributes.getValue("name")
                name = attributes.getValue("prefix")
                x_uri = parse.urlparse(attributes.getValue("uri"))
                try:
                    request.urlopen(attributes.getValue("uri"))
                except error.URLError:
                    return

                self.__extension = XExtension(mapping, name, x_uri)

            elif tag_name.lower() == "log":
                self.__xAttributes = self.__extension.get_log_attributes()
            elif tag_name.lower() == "trace":
                self.__xAttributes = self.__extension.get_trace_attributes()
            elif tag_name.lower() == "event":
                self.__xAttributes = self.__extension.get_event_attributes()
            elif tag_name.lower() == "meta":
                self.__xAttributes = self.__extension.get_meta_attributes()

            elif tag_name.lower() == "string":
                self.__xAttributes = self.__extension.get_log_attributes()
                mapping = self.__extension.get_prefix() + ':' + attributes.getValue("key")
                self.__currentAttribute = self.__factory.create_attribute_literal(mapping, "DEFAULT", self.__extension)
                self.__xAttributes.add(self.__currentAttribute)

            elif tag_name.lower() == "date":
                self.__xAttributes = self.__extension.get_log_attributes()
                mapping = self.__extension.get_prefix() + ':' + attributes.getValue("key")
                self.__currentAttribute = self.__factory.create_attribute_timestamp(mapping, 0, self.__extension)
                self.__xAttributes.add(self.__currentAttribute)

            elif tag_name.lower() == "int":
                self.__xAttributes = self.__extension.get_log_attributes()
                mapping = self.__extension.get_prefix() + ':' + attributes.getValue("key")
                self.__currentAttribute = self.__factory.create_attribute_discrete(mapping, 0, self.__extension)
                self.__xAttributes.add(self.__currentAttribute)

            elif tag_name.lower() == "float":
                self.__xAttributes = self.__extension.get_log_attributes()
                mapping = self.__extension.get_prefix() + ':' + attributes.getValue("key")
                self.__currentAttribute = self.__factory.create_attribute_continuous(mapping, 0.0, self.__extension)
                self.__xAttributes.add(self.__currentAttribute)

            elif tag_name.lower() == "boolean":
                self.__xAttributes = self.__extension.get_log_attributes()
                mapping = self.__extension.get_prefix() + ':' + attributes.getValue("key")
                self.__currentAttribute = self.__factory.create_attribute_boolean(mapping, False, self.__extension)
                self.__xAttributes.add(self.__currentAttribute)

            elif tag_name.lower() == "id":
                self.__xAttributes = self.__extension.get_log_attributes()
                mapping = self.__extension.get_prefix() + ':' + attributes.getValue("key")
                self.__currentAttribute = self.__factory.create_attribute_id(mapping, XIDFactory.create_id(), self.__extension)
                self.__xAttributes.add(self.__currentAttribute)

            elif self.__currentAttribute is not None and tag_name.lower() == "alias":
                mapping = attributes.getValue("mapping")
                name = attributes.getValue("name")
                XGlobalAttributeNameMap().register_mapping(mapping, self.__currentAttribute.get_key(), name)

        def endElement(self, local_name):
            """ Overrides endElement in class ContentHandler

            :param local_name: The name of the element type, just as with the
              startElement event
            :type local_name: str
            """
            tag_name = local_name

            if tag_name.lower() in ["string", "date", "int", "float", "boolean", "id"]:
                self.__currentAttribute = None

    @staticmethod
    def parse(file):
        """Parses an extension from a definition file.

        :param file: The path of the file containing the extension or url string
          which represents the extension definition file..
        :type file: str
        :return: The extension object, as defined in the provided file.
        :rtype: `XExtension`
        """
        handler = XExtensionParser.XExtensionHandler()
        if os.path.isfile(file):
            with open(file) as data:
                xml_parse(data, handler)

        elif not os.path.isdir(file):
            parseString(request.urlopen(file).read(), handler)
        return handler.get_extension()

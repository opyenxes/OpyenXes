from xml.sax.handler import ContentHandler
from xml.sax import parse as xml_parse
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.extension.std.XTimeExtension import XTimeExtension
from opyenxes.extension.std.XConceptExtension import XConceptExtension
from opyenxes.extension.std.XOrganizationalExtension import XOrganizationalExtension
from opyenxes.extension.std.XLifecycleExtension import XLifecycleExtension
from opyenxes.extension.std.XSemanticExtension import XSemanticExtension
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.classification.XEventNameClassifier import XEventNameClassifier
from opyenxes.classification.XEventResourceClassifier import XEventResourceClassifier
from opyenxes.log.XLogging import XLogging
from opyenxes.utils.XsDateTimeConversion import parse_date_time


class XMxmlParser:
    """Parser for the MXML format for event logs (deprecated).

    :param factory: The factory to use for XES model building.
    :type factory: `XFactory`
    """
    MXML_CLASSIFIERS = [XEventAttributeClassifier("MXML Legacy Classifier", ["concept:name", "lifecycle:transition"]),
                        XEventNameClassifier(),
                        XEventResourceClassifier()]

    def __init__(self, factory=None):
        if factory:
            self.factory = factory
        else:
            self.factory = XFactoryRegistry().current_default()

    def can_parse(self, file):
        """Checks whether this parser can handle the given file.

        :param file: path of the file to check against parser.
        :type file: str
        :return: Whether this parser can handle the given file.
        :rtype: bool
        """
        return self.ends_with_ignore_case(file, ".mxml") or self.ends_with_ignore_case(file, ".xml")

    def parse(self, file):
        """Parses a set of logs from the given input stream, which is supposed
        to deliver an MXML serialization.



        :param file: file generated by the function 'open(path)', which is
          supposed to deliver an MXML serialization.
        :type file: _io.TextIOWrapper
        :return: The parsed list of logs.
        :rtype: list[`XLog`]
        """
        handler = XMxmlParser.MxmlHandler()

        xml_parse(file, handler)

        return handler.get_logs()

    @staticmethod
    def ends_with_ignore_case(name, suffix):
        """Returns whether the given file name ends (ignoring the case) with the given suffix.

        :param name: The given file name.
        :type name: str
        :param suffix: The given suffix.
        :type suffix: str
        :return: Whether the given file name ends (ignoring the case) with the given suffix.
        :rtype: bool
        """
        i = len(name) - len(suffix)
        if i > 0:
            return suffix in name[i:]
        return False

    class MxmlHandler(ContentHandler):
        """SAX handler class for XES in XML representation.

        """
        def __init__(self):
            super().__init__()
            self.__buffer = list()
            self.__logs = list()
            self.__currentProcess = None
            self.__currentInstance = None
            self.__entry = None
            self.__sourceAttribute = None
            self.__genericAttribute = None
            self.__eventTypeAttribute = None
            self.__originatorAttribute = None
            self.__sourceOpen = False
            self.__timestamp = None
            self.__lastTimestamp = None
            self.__numUnorderedEntries = 0

        def get_logs(self):
            """Retrieves the parsed list of logs.

            :return: The parsed list of logs.
            :rtype: list[`XLog`]
            """
            return self.__logs

        def startElement(self, element_name, attributes):
            """ Overrides startElement in class ContentHandler

            :param element_name: Contains the raw XML 1.0 name of the element type.
            :type element_name: str
            :param attributes: An instance of the Attributes class containing
              the attributes of the element
            :type attributes: xml.sax.xmlreader.AttributesImpl
            """
            tag_name = element_name
            if tag_name != "WorkflowLog":
                if tag_name == "Source":
                    self.__sourceOpen = True
                    description_string = attributes.get("program")
                    self.__sourceAttribute = XMxmlParser().factory.create_attribute_literal("source", description_string, None)
                    self.__add_model_reference__(attributes, self.__sourceAttribute)
                elif tag_name == "Process":
                    description_string = attributes.get("id")
                    description = attributes.get("description")

                    self.__currentProcess = XMxmlParser().factory.create_log()
                    self.__currentProcess.get_extensions().add(XConceptExtension())
                    self.__currentProcess.get_extensions().add(XOrganizationalExtension())
                    self.__currentProcess.get_extensions().add(XLifecycleExtension())
                    self.__currentProcess.get_extensions().add(XSemanticExtension())
                    self.__currentProcess.get_extensions().add(XTimeExtension())
                    if self.__sourceAttribute:
                        self.__currentProcess.get_attributes()[self.__sourceAttribute.get_key()] = self.__sourceAttribute

                    XConceptExtension().assign_name(self.__currentProcess, description_string)
                    XLifecycleExtension().assign_model(self.__currentProcess, "standard")

                    if description and len(description.lower()) > 0:

                        description1 = XMxmlParser().factory.create_attribute_literal("description", description, None)
                        self.__currentProcess.get_attributes()[description1.get_key()] = description1

                    self.__add_model_reference__(attributes, self.__currentProcess)

                elif tag_name == "ProcessInstance":
                    self.__currentInstance = XMxmlParser().factory.create_trace()
                    name = attributes.get("id")
                    if name is None:
                        name = "None"

                    XConceptExtension().assign_name(self.__currentInstance, name)
                    description_string = attributes.get("description")

                    if description_string and len(description_string.strip()) > 0:
                        description2 = XMxmlParser().factory.create_attribute_literal("description", description_string, None)
                        self.__currentInstance.get_attributes()[description2.get_key()] = description2

                    self.__add_model_reference__(attributes, self.__currentInstance)

                elif tag_name == "AuditTrailEntry":
                    self.__entry = XMxmlParser().factory.create_event()

                elif tag_name == "Attribute":
                    self.__genericAttribute = XMxmlParser().factory.create_attribute_literal(attributes.get("name").strip(), "DEFAULT_VALUE", None)
                    self.__add_model_reference__(attributes, self.__genericAttribute)

                elif tag_name == "EventType":
                    self.__eventTypeAttribute = XLifecycleExtension().ATTR_TRANSITION.clone()
                    unknown_type = attributes.get("unknowntype")
                    if unknown_type:
                        self.__eventTypeAttribute.set_value(unknown_type)
                    else:
                        self.__eventTypeAttribute.set_value("UNKNOWN")

                    self.__add_model_reference__(attributes, self.__eventTypeAttribute)

                elif tag_name == "WorkflowModelElement":
                    self.__add_model_reference__(attributes, self.__entry)

                elif tag_name == "Originator":
                    self.__originatorAttribute = XOrganizationalExtension().ATTR_RESOURCE.clone()
                    self.__add_model_reference__(attributes, self.__originatorAttribute)

        def endElement(self, local_name):
            """ Overrides endElement in class ContentHandler

            :param local_name: The name of the element type, just as with the startElement event
            :type local_name: str
            """
            tag_name = local_name

            if tag_name == "WorkflowLog":
                if self.__numUnorderedEntries > 0:
                    XLogging().log("LogData: Log contains " + str(self.__numUnorderedEntries) + " audit trail entries in non-natural order!", XLogging.Importance.ERROR)
                    XLogging().log("LogData: The log file you have loaded is not MXML compliant! (error compensated transparently)", XLogging.Importance.ERROR)

            elif tag_name == "Process":
                self.__currentProcess.get_classifiers().extend(XMxmlParser.MXML_CLASSIFIERS)
                self.__currentProcess.get_global_trace_attributes().append(XConceptExtension().ATTR_NAME.clone())
                self.__currentProcess.get_global_event_attributes().append(XConceptExtension().ATTR_NAME.clone())
                self.__currentProcess.get_global_event_attributes().append(XLifecycleExtension().ATTR_TRANSITION.clone())
                self.__logs.append(self.__currentProcess)
                self.__currentProcess = None

            elif tag_name == "Process":
                self.__sourceOpen = False

            elif tag_name == "ProcessInstance":
                if len(self.__currentInstance) > 0:
                    self.__currentProcess.append(self.__currentInstance)

                self.__currentInstance = None
                self.__lastTimestamp = None

            elif tag_name == "AuditTrailEntry":
                if self.__timestamp is None:
                    self.__currentInstance.append(self.__entry)
                elif self.__lastTimestamp is None:
                    self.__currentInstance.append(self.__entry)
                    self.__lastTimestamp = self.__timestamp
                elif self.__timestamp > self.__lastTimestamp:
                    self.__currentInstance.append(self.__entry)
                    self.__lastTimestamp = self.__timestamp
                else:
                    self.__currentInstance.append(self.__entry)

                self.__entry = None

            else:
                if tag_name == "Attribute":
                    originator = "".join(self.__buffer).strip()
                    if len(originator) > 0:
                        self.__genericAttribute.set_value("".join(self.__buffer).strip())
                        if self.__entry:
                            self.__entry.get_attributes()[self.__genericAttribute.get_key()] = self.__genericAttribute
                        elif self.__currentInstance:
                            self.__currentInstance.get_attributes()[self.__genericAttribute.get_key()] = self.__genericAttribute
                        elif self.__currentProcess:
                            self.__currentProcess.get_attributes()[self.__genericAttribute.get_key()] = self.__genericAttribute
                        elif self.__sourceOpen:
                            self.__sourceAttribute.get_attributes()[self.__genericAttribute.get_key()] = self.__genericAttribute
                    self.__genericAttribute = None

                elif tag_name == "EventType":
                    if self.__eventTypeAttribute.get_value() == "UNKNOWN":
                        originator = "".join(self.__buffer).strip()
                        if len(originator) > 0:
                            self.__eventTypeAttribute.set_value(originator)
                            self.__entry.get_attributes()[self.__eventTypeAttribute.get_key()] = self.__eventTypeAttribute
                    else:
                        self.__entry.get_attributes()[self.__eventTypeAttribute.get_key()] = self.__eventTypeAttribute
                    self.__eventTypeAttribute = None

                elif tag_name == "WorkflowModelElement":
                    XConceptExtension().assign_name(self.__entry, "".join(self.__buffer).strip())

                elif tag_name == "Timestamp":
                    originator = "".join(self.__buffer).strip()
                    self.__timestamp = parse_date_time(originator)
                    if self.__timestamp:
                        timestamp_attribute = XTimeExtension().ATTR_TIMESTAMP.clone()
                        timestamp_attribute.set_value(self.__timestamp)
                        self.__entry.get_attributes()[timestamp_attribute.get_key()] = timestamp_attribute

                elif tag_name == "Originator":
                    originator = "".join(self.__buffer).strip()
                    if len(originator) > 0:
                        self.__originatorAttribute.set_value(originator)

                    self.__entry.get_attributes()[self.__originatorAttribute.get_key()] = self.__originatorAttribute
                    self.__originatorAttribute = None

            self.__buffer.clear()

        @staticmethod
        def __add_model_reference__(attrib, subject):
            try:
                model_reference = attrib.getValue("modelReference")
            except KeyError:
                model_reference = None

            if model_reference:
                attribute = XSemanticExtension().ATTR_MODELREFERENCE.clone()
                attribute.set_value(model_reference)
                subject.get_attributes()[attribute.get_key()] = attribute

        def ignorableWhitespace(self, whitespace):
            """ Overrides ignorableWhitespace in class ContentHandler

            :param whitespace: The whitespace characters.
            :type whitespace: str
            """
            self.__buffer.append(whitespace)

        def characters(self, content):
            """ Overrides characters in class ContentHandler

            :param content: The characters.
            :type content: str
            """
            self.__buffer.append(content)

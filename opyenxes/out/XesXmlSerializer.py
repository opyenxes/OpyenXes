from opyenxes.log.XLogging import XLogging
import time
import xml.etree.ElementTree as Et
from xml.dom import minidom
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.model.XAttributeDiscrete import XAttributeDiscrete
from opyenxes.model.XAttributeLiteral import XAttributeLiteral
from opyenxes.model.XAttributeContinuous import XAttributeContinuous
from opyenxes.model.XAttributeBoolean import XAttributeBoolean
from opyenxes.model.XAttributeID import XAttributeID
from opyenxes.model.XAttributeList import XAttributeList
from opyenxes.model.XAttributeContainer import XAttributeContainer
from opyenxes.model.XAttributeTimestamp import XAttributeTimestamp
from opyenxes.model.XAttributeCollection import XAttributeCollection
from opyenxes.utils.XTokenHelper import XTokenHelper


class XesXmlSerializer:
    """XES plain XML serialization for the XES format.

    """
    @staticmethod
    def get_author():
        """Returns the name of this serialization's author.

        :return:  The author name.
        :rtype: str
        """
        return "Hernán F. Valdivieso"

    @staticmethod
    def get_suffices():
        """Returns an array of possible file suffices for this serialization.

        :return: An array of possible file suffices for this serialization.
        :rtype: list[str]
        """
        return ["xes"]

    def serialize(self, log, out, in_bytes=False):
        """Serializes a given log to the given output stream.

        :param log: Log to be serialized.
        :type log: `XLog`
        :param out: TextIOWrapper for serialization.
        :type out: _io.TextIOWrapper
        :param in_bytes: Private argument to decide if serialized as bytes or as string
        :type in_bytes: bool
        """
        XLogging().log("Start serializing log to XES.XML", XLogging.Importance.DEBUG)
        start = time.time() * 1000

        log_xml = Et.Element("log")
        log_xml.set("xes.version", "1.0")
        log_xml.set("xes.features", "nested-attributes")
        log_xml.set("openxes.version", "1.0RC7")

        for extension in log.get_extensions():
            extension_xml = Et.SubElement(log_xml, "extension")
            extension_xml.set("name", extension.get_name())
            extension_xml.set("prefix", extension.get_prefix())
            extension_xml.set("uri", extension.get_uri().geturl())

        self.add_global_attributes(log_xml, "trace", log.get_global_trace_attributes())
        self.add_global_attributes(log_xml, "event", log.get_global_event_attributes())

        for classifier in log.get_classifiers():
            if isinstance(classifier, XEventAttributeClassifier):
                classifier_xml = Et.SubElement(log_xml, "classifier")
                classifier_xml.set("name", classifier.name())
                classifier_xml.set("keys", XTokenHelper.format_token(classifier.get_defining_attribute_keys()))

        self.add_attributes(log_xml, log.get_attributes().values())

        for trace in log:
            trace_xml = Et.SubElement(log_xml, "trace")
            self.add_attributes(trace_xml, trace.get_attributes().values())

            for event in trace:
                event_xml = Et.SubElement(trace_xml, "event")
                self.add_attributes(event_xml, event.get_attributes().values())

        text = minidom.parseString(Et.tostring(log_xml, "utf-8"))
        c1 = text.createComment("This file has been generated with the OpenXES library. It conforms")
        c2 = text.createComment("to the XML serialization of the XES standard for log storage and")
        c3 = text.createComment("management.")
        c4 = text.createComment("XES standard version: 1.0")
        c5 = text.createComment("OpenXES library version: 1.0RC7")
        c6 = text.createComment("OpenXES is available from http://www.openxes.org/")
        text.insertBefore(c6, text.childNodes[0])
        text.insertBefore(c5, text.childNodes[0])
        text.insertBefore(c4, text.childNodes[0])
        text.insertBefore(c3, text.childNodes[0])
        text.insertBefore(c2, text.childNodes[0])
        text.insertBefore(c1, text.childNodes[0])

        if in_bytes:
            out.write(text.toprettyxml("\t").encode())
        else:
            out.write(text.toprettyxml("\t"))

        duration1 = " (" + str(time.time() * 1000 - start) + " msec.)"
        XLogging().log("finished serializing log" + duration1, XLogging.Importance.DEBUG)

    def add_global_attributes(self, parent, scope, attributes):
        """Helper method for defining global attributes on a given scope.

        :param parent: xml element to add a children element with the global attributes
        :type parent: xml.etree.ElementTree.Element
        :param scope: Name of the global attributes, can be 'trace' or 'event'.
        :type scope: str
        :param attributes: Collection with the attributes to add.
        :type attributes: dict_values
        """
        if len(attributes) > 0:
            global_attribute = Et.SubElement(parent, "global")
            global_attribute.set("scope", scope)
            self.add_attributes(global_attribute, attributes)

    def add_attributes(self, tag, attributes):
        """Helper method, adds the given collection of attributes to the given Tag.

        :param tag: Tag to add attributes to.
        :type tag: xml.etree.ElementTree.Element
        :param attributes: Collection with the attributes to add.
        :type attributes: dict_values
        """
        for attribute in attributes:
            if isinstance(attribute, XAttributeDiscrete):
                attribute_tag = Et.SubElement(tag, "int")
                attribute_tag.set("key", attribute.get_key())
                attribute_tag.set("value", str(attribute))
            elif isinstance(attribute, XAttributeLiteral):
                attribute_tag = Et.SubElement(tag, "string")
                attribute_tag.set("key", attribute.get_key())
                attribute_tag.set("value", str(attribute))
            elif isinstance(attribute, XAttributeContinuous):
                attribute_tag = Et.SubElement(tag, "float")
                attribute_tag.set("key", attribute.get_key())
                attribute_tag.set("value", str(attribute))
            elif isinstance(attribute, XAttributeBoolean):
                attribute_tag = Et.SubElement(tag, "boolean")
                attribute_tag.set("key", attribute.get_key())
                attribute_tag.set("value", str(attribute))
            elif isinstance(attribute, XAttributeID):
                attribute_tag = Et.SubElement(tag, "id")
                attribute_tag.set("key", attribute.get_key())
                attribute_tag.set("value", str(attribute))
            elif isinstance(attribute, XAttributeList):
                attribute_tag = Et.SubElement(tag, "list")
                attribute_tag.set("key", attribute.get_key())
            elif isinstance(attribute, XAttributeContainer):
                attribute_tag = Et.SubElement(tag, "container")
                attribute_tag.set("key", attribute.get_key())
            elif isinstance(attribute, XAttributeTimestamp):
                attribute_tag = Et.SubElement(tag, "date")
                attribute_tag.set("key", attribute.get_key())
                attribute_tag.set("value", str(attribute))

            if isinstance(attribute, XAttributeCollection):
                collection = attribute.get_collection()
                self.add_attributes(attribute_tag, collection)
            elif attribute.has_attributes():
                self.add_attributes(attribute_tag, attribute.get_attributes().values())

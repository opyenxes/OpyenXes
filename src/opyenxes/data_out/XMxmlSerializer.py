from opyenxes.log.XLogging import XLogging
import time
import xml.etree.ElementTree as Et
from xml.dom import minidom
from opyenxes.extension.std.XConceptExtension import XConceptExtension


class XMxmlSerializer:
    """MXML serialization for XES data (legacy implementation). Note that this
    serialization may be lossy, you should preferrably use the XES.XML
    serialization for XES data.

    """
    def __init__(self):
        self.__known_types = set()
        self.__known_types.add("schedule")
        self.__known_types.add("assign")
        self.__known_types.add("withdraw")
        self.__known_types.add("reassign")
        self.__known_types.add("start")
        self.__known_types.add("suspend")
        self.__known_types.add("resume")
        self.__known_types.add("pi_abort")
        self.__known_types.add("ate_abort")
        self.__known_types.add("complete")
        self.__known_types.add("autoskip")
        self.__known_types.add("manualskip")

    @staticmethod
    def get_suffices():
        """Returns an array of possible file suffices for this serialization.

        :return: An array of possible file suffices for this serialization.
        :rtype: list[str]
        """
        return ["mxml"]

    def serialize(self, log, out, in_bytes=False):
        """Serializes a given log to the given output stream.

        :param log: Log to be serialized.
        :type log: `XLog`
        :param out:  TextIOWrapper for serialization.
        :type out: _io.TextIOWrapper
        :param in_bytes: Private argument to decide if serialized in bytes or in string
        :type in_bytes: bool
        """
        XLogging().log("start serializing log to MXML", XLogging.Importance.DEBUG)
        start = time.time() * 1000

        root = Et.Element("WorkflowLog")
        source = Et.SubElement(root, "Source")
        source.set("program", "XES MXML serialization")
        source.set("openxes.version", "1.0RC7")
        process = Et.SubElement(root, "Process")
        identity = XConceptExtension().extract_name(log)
        if identity is None:
            process.set("id", "none")
        else:
            process.set("id", identity)
        name = XConceptExtension().extract_name(log)
        if name is None:
            name = "None"
        process.set("description", "process with id " + name)
        self.add_model_reference(log, process)
        self.add_attribute(process, log.get_attributes().values())

        for trace in log:
            instance = Et.SubElement(process, "ProcessInstance")
            identity = XConceptExtension().extract_name(trace)
            if identity is None:
                identity = "None"
            instance.set("id", identity)
            name = XConceptExtension().extract_name(trace)
            if name is None:
                name = "None"
            instance.set("description", "instance with id " + name)
            self.add_model_reference(trace, instance)
            self.add_attribute(instance, trace.get_attributes().values())

            for event in trace:
                ate = Et.SubElement(instance, "AuditTrailEntry")
                self.add_attribute(ate, event.get_attributes().values())
                workflow_mode = Et.SubElement(ate, "WorkflowModelElement")
                self.add_model_reference(event, workflow_mode)
                workflow_mode.text = XConceptExtension().extract_name(event)
                type_ = Et.SubElement(ate, "EventType")
                type_attr = event.get_attributes().get("lifecycle:transition")

                if type_attr:
                    self.add_model_reference(type_attr, type_)
                    originator_attr = type_attr.get_value().strip().lower()
                    if originator_attr in self.__known_types:
                        type_.text = originator_attr
                    else:
                        type_.set("unknownType", type_attr.get_value())
                        type_.text = "unknown"

                else:
                    type_.text = "complete"

                originator_attr_1 = event.get_attributes().get("org:resource")
                if originator_attr_1 is None:
                    originator_attr_1 = event.get_attributes().get("org:role")

                if originator_attr_1 is None:
                    originator_attr_1 = event.get_attributes().get("org:group")

                if originator_attr_1 is not None:
                    timestamp_attr = Et.SubElement(ate, "originator")
                    self.add_model_reference(originator_attr_1, timestamp_attr)
                    timestamp_attr.text = (originator_attr_1.get_value())

                timestamp_attr_1 = event.get_attributes().get("time:timestamp")
                if timestamp_attr_1:
                    timestamp = Et.SubElement(ate, "timestamp")
                    self.add_model_reference(timestamp_attr_1, timestamp)
                    date = timestamp_attr_1.get_value()
                    timestamp.text = str(date)

        text = minidom.parseString(Et.tostring(root, "utf-8"))
        c1 = text.createComment("This file has been generated with the OpenXES library. It conforms")
        c2 = text.createComment("to the legacy MXML standard for log storage and management.")
        c3 = text.createComment("OpenXES library version: 1.0RC7")
        c4 = text.createComment("OpenXES is available from http://www.xes-standard.org/")
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

    def add_attribute(self, tag, attributes, key_prefix=None):
        """Helper method, adds attributes to a tag.

        :param tag: The tag to add attributes to.
        :type tag: xml.etree.ElementTree.Element
        :param attributes: The attributes to add.
        :type attributes: dict_values
        :param key_prefix: The Key prefix of attributes.
        :type key_prefix: str
        """
        if key_prefix is None:
            key_prefix = ""
            node = Et.SubElement(tag, "Data")
        else:
            node = tag

        for attribute in attributes:
            if attribute.get_key() == "semantic:modelReference":
                attribute_tag = Et.SubElement(node, "attribute")
                attribute_tag.set("name", key_prefix + attribute.get_key())
                self.add_model_reference(attribute, attribute_tag)

                if attribute_tag.text is None:
                    attribute_tag.text = str(attribute)
                else:
                    attribute_tag.text += str(attribute)

                sub_attributes = attribute.get_attributes().values()

                if len(sub_attributes) > 0:
                    sub_key_prefix = attribute.get_key()

                    if len(sub_key_prefix) > 0:
                        sub_key_prefix = key_prefix + ":" + sub_key_prefix

                    self.add_attribute(node, sub_key_prefix, sub_attributes)

    @staticmethod
    def add_model_reference(element, target):
        """Helper method, adds all model references of an attributable to the given tag.

        :param element: Attributable element.
        :type element: `XAttributable`
        :param target: Tag to add model references to.
        :type target: xml.etree.ElementTree.Element
        """
        model_ref_attr = element.get_attributes().get("semantic:modelReference")
        if model_ref_attr:
            target.set("modelReference", model_ref_attr.get_value())

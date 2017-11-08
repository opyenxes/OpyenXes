from opyenxes.model.XAttributeBoolean import XAttributeBoolean
from opyenxes.model.XAttributeContainer import XAttributeContainer
from opyenxes.model.XAttributeContinuous import XAttributeContinuous
from opyenxes.model.XAttributeDiscrete import XAttributeDiscrete
from opyenxes.model.XAttributeID import XAttributeID
from opyenxes.model.XAttributeList import XAttributeList
from opyenxes.model.XAttributeLiteral import XAttributeLiteral
from opyenxes.model.XAttributeMap import XAttributeMap
from opyenxes.model.XAttributeTimestamp import XAttributeTimestamp
from opyenxes.model.XEvent import XEvent
from opyenxes.model.XLog import XLog
from opyenxes.model.XTrace import XTrace


class XFactory:
    """
    Provide methods for creating all element classes of the XES model type
    hierarchy
    """
    @staticmethod
    def create_log(attribute=None):
        """Creates a new XES log instance.

        :param attribute: A `XAttributeMap` with the attribute for the log.
        :type attribute: `XAttributeMap`
        :return: A new log instance.
        :rtype: `XLog`
        """
        if attribute:
            return XLog(attribute)
        return XLog(XAttributeMap())

    @staticmethod
    def create_trace(attribute=None):
        """Creates a new XES trace instance.

        :param attribute: A `XAttributeMap` with the attribute for the trace.
        :type attribute: `XAttributeMap`
        :return: A new trace instance.
        :rtype: `XTrace`
        """
        if attribute:
            return XTrace(attribute)
        return XTrace(XAttributeMap())

    @staticmethod
    def create_event(attribute=None, identity=None):
        """Creates a new XES event instance.

        :param attribute: A `XAttributeMap` with the attribute for the event.
        :type attribute: `XAttributeMap`
        :param identity:  The identity defining the attribute (set to None, if
         the attribute is not associated to an identity).
        :type identity: `XID`
        :return: A new event instance.
        :rtype: `XEvent`
        """
        if attribute and identity:
            return XEvent(attribute, identity)

        if attribute:
            return XEvent(attribute)

        return XEvent()

    @staticmethod
    def create_attribute_map():
        """Creates a new XES attribute map.

        :return: A new attribute map instance.
        :rtype: `XAttributeMap`
        """
        return XAttributeMap()

    @staticmethod
    def create_attribute_boolean(key, value, extension=None):
        """Creates a new XES attribute with boolean value.

        :param key: The key of the attribute.
        :type key: str
        :param value: The value of the attribute.
        :type value: bool
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new attribute with boolean value.
        :rtype: `XAttributeBoolean`
        """
        return XAttributeBoolean(key, value, extension)

    @staticmethod
    def create_attribute_continuous(key, value, extension=None):
        """Creates a new XES attribute with float value.

        :param key: The key of the attribute.
        :type key: str
        :param value: The value of the attribute.
        :type value: float
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new attribute with float value.
        :rtype: `XAttributeContinuous`
        """
        return XAttributeContinuous(key, value, extension)

    @staticmethod
    def create_attribute_discrete(key, value, extension=None):
        """Creates a new XES attribute with integer value.

        :param key: The key of the attribute.
        :type key: str
        :param value: The value of the attribute.
        :type value: int
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new attribute with integer value.
        :rtype: `XAttributeDiscrete`
        """
        return XAttributeDiscrete(key, value, extension)

    @staticmethod
    def create_attribute_literal(key, value, extension=None):
        """Creates a new XES attribute with string value.

        :param key: The key of the attribute.
        :type key: str
        :param value: The value of the attribute.
        :type value: str
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new attribute with string value.
        :rtype: `XAttributeLiteral`
        """
        return XAttributeLiteral(key, value, extension)

    @staticmethod
    def create_attribute_timestamp(key, value, extension=None):
        """Creates a new XES attribute with datetime value.

        :param key: The key of the attribute.
        :type key: str
        :param value: The value of the attribute.
        :type value: datetime.datetime or int
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new attribute with datetime value.
        :rtype: `XAttributeTimestamp`
        """
        return XAttributeTimestamp(key, value, extension)

    @staticmethod
    def create_attribute_id(key, value, extension=None):
        """Creates a new XES attribute with XID value.

        :param key: The key of the attribute.
        :type key: str
        :param value: The value of the attribute.
        :type value: `XID`
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new attribute with XID value.
        :rtype: `XAttributeID`
        """
        return XAttributeID(key, value, extension)

    @staticmethod
    def create_attribute_list(key, extension=None):
        """Creates a new XES list attribute.

        :param key: The key of the attribute.
        :type key: str
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new list attribute.
        :rtype: `XAttributeList`
        """
        return XAttributeList(key, extension)

    @staticmethod
    def create_attribute_container(key, extension=None):
        """Creates a new XES container attribute.

        :param key: The key of the attribute.
        :type key: str
        :param extension: The extension defining the attribute (set to None, if
         the attribute is not associated to an extension).
        :type extension: `XExtension` or None
        :return: A new container attribute.
        :rtype: `XAttributeContainer`
        """
        return XAttributeContainer(key, extension=extension)

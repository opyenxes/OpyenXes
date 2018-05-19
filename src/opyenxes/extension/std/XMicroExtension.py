from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.id.XIDFactory import XIDFactory
from opyenxes.utils.SingletonClassGenerator import XMicroExtensionMetaclass


class XMicroExtension(XExtension, metaclass=XMicroExtensionMetaclass):
    """ The micro event extension defines a nesting level, a nesting parent,
    and the number of nested children for events within a log.

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Micro", "micro", urlparse("http://www.xes-standard.org/micro.xesext"))
        factory = XFactoryRegistry().current_default()

        self.ATTR_LEVEL = factory.create_attribute_discrete("micro:level", -1, self)
        self.ATTR_PID = factory.create_attribute_id("micro:parentId", XIDFactory.create_id(), self)
        self.ATTR_LENGTH = factory.create_attribute_discrete("micro:length", -1, self)

        self.get_event_attributes().add(self.ATTR_LEVEL.clone())
        self.get_event_attributes().add(self.ATTR_PID.clone())
        self.get_event_attributes().add(self.ATTR_LENGTH.clone())

        XGlobalAttributeNameMap().register_mapping("EN", "micro:level", "Micro level of this event")
        XGlobalAttributeNameMap().register_mapping("EN", "micro:parentId", "Id of parent event of this event")
        XGlobalAttributeNameMap().register_mapping("EN", "micro:length", "Number of child events for this event")

    @staticmethod
    def extract_level(event):
        """Retrieves the level of an event, if set by this extension's level
        attribute.

        :param event: Event to extract level from.
        :type event: `XEvent`
        :return: The requested event level, -1 if not set.
        :rtype: int
        """
        attribute = event.get_attributes().get("micro:level")
        if attribute:
            return attribute.get_value()
        return -1

    def assign_level(self, event, level):
        """ Assigns any event its level, as defined by this extension's level
        attribute.

        :param event: Event to assign level to.
        :type event: `XAttributable`
        :param level: The level to be assigned. Should be a positive integer.
        :type level: int
        """
        if level > 0:
            attr = self.ATTR_LEVEL.clone()
            attr.set_value(level)
            event.get_attributes()["micro:level"] = attr

    @staticmethod
    def remove_level(event):
        """Removes the level from an event.

        :param event: The event to remove th elevel from.
        :type event: `XAttributable`
        """
        if "micro:level" in event.get_attributes():
            del event.get_attributes()["micro:level"]

    @staticmethod
    def extract_parent_id(event):
        """Retrieves the parent Id of an event, if set by this extension's
        parentId attribute.

        :param event: Event to extract parent Id from.
        :type event: `XEvent`
        :return: The requested event parent Id, null if not set.
        :rtype: XID
        """
        attribute = event.get_attributes()["micro:parentId"]
        if attribute:
            return attribute.get_value()
        return None

    def assign_parent_id(self, event, parent_id):
        """ Assigns any event its parent Id, as defined by this extension's
        parentId attribute.

        :param event: Event to assign parent Id to.
        :type event: `XAttributable`
        :param parent_id: The parent Id to be assigned. May not be null.
        :type parent_id: `XID`
        """
        if parent_id is not None:
            attr = self.ATTR_PID.clone()
            attr.setValue(parent_id)
            event.get_attributes()["micro:parentId"] = attr
        else:
            if "micro:parentId" in event.get_attributes():
                del event.get_attributes()["micro:parentId"]

    @staticmethod
    def remove_parent_id(event):
        """Removes the parent Id from an event.

        :param event: The event to remove the parent Id from.
        :type event: `XAttributable`
        """
        if "micro:parentId" in event.get_attributes():
            del event.get_attributes()["micro:parentId"]

    @staticmethod
    def extract_length(event):
        """Retrieves the stated number of children of an event, if set by this
        extension's length attribute. Note that this simply returns the value of
        the "micro:legnth" attribute, and -1 if not present. This does not count
        the children, it simply returns the number as found in the event.

        :param event: Event to extract stated number of children from.
        :type event: `XEvent`
        :return: The requested number for this event, -1 if not set.
        :rtype: int
        """
        attribute = event.get_attributes().get("micro:length")
        if attribute:
            return attribute.get_value()
        return None

    def assign_length(self, event, length):
        """Assigns any event its state number of children, as defined by this
        extension's length attribute.

        :param event: Event to assign number of children to.
        :type event: `XAttributable`
        :param length: The number to be assigned. Should be a non-negative integer.
        :type length: int
        """
        if length >= 0:
            attr = self.ATTR_LENGTH.clone()
            attr.set_value(length)
            event.get_attributes()["micro:length"] = attr

    @staticmethod
    def remove_length(event):
        """Removes the stated number of children from an event.

        :param event: The event to remove the number from.
        :type event: `XAttributable`
        """
        if "micro:length" in event.get_attributes():
            del event.get_attributes()["micro:length"]

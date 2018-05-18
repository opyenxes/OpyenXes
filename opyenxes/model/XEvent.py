from opyenxes.model.XElement import XElement
from opyenxes.model.XAttributeMap import XAttributeMap
from opyenxes.id.XIDFactory import XIDFactory


class XEvent(XElement):
    """
    An event is an element of an XES event log structure. Events are
    sequentially contained in traces. Events refer to something that has
    happened during the execution of a process, e.g. the execution of an
    activity.

    :param attributes: Map of attribute for the event.
    :type attributes: `XAttributeMap`
    :param identity: The unique id that represent this event.
    :type identity: `XID`
    """
    def __init__(self, attributes=None, identity=None):
        if not attributes:
            attributes = XAttributeMap()
        if identity:
            self.__id = identity
        else:
            self.__id = XIDFactory.create_id()
        super().__init__(attributes)

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XEvent`
        """
        clone = XEvent()
        clone.set_attributes(self.get_attributes().clone())
        clone.set_id(XIDFactory.create_id())
        return clone

    def get_id(self):
        """Retrieves the id value of this event

        :return: id of this event
        :rtype: `XID`
        """
        return self.__id

    def set_id(self, idem):
        """Assigns the id value of this event.

        :param idem: id of the event.
        :type idem: `XID`
        """
        self.__id = idem

    def __eq__(self, other):
        if isinstance(other, XEvent):
            return self.__id.__eq__(other.__id)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__id)

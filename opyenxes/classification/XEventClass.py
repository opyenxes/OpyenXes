from opyenxes.utils.CompareUtils import compare_to_string


class XEventClass:
    """Implements an event class. An event class is an identity for events,
    making them comparable. If two events are part of the same class,
    they are considered to be equal, i.e. to be referring to the same
    higher-level concept.

    :param identity: Unique identification string of the class, i.e. its name.
    :type identity: str
    :param index: Unique index of class.
    :type index: int
    """
    def __init__(self, identity, index):
        self.__id = identity
        self.__index = index
        self.__size = 0

    def get_id(self):
        """Retrieves the name, i.e. unique identification string, of this event
         class.

        :return: The name of this class, as a unique string.
        :rtype: str
        """
        return self.__id

    def get_index(self):
        """Returns the index of this event class.

        :return: Unique index.
        :rtype: int
        """
        return self.__index

    def size(self):
        """Retrieves the size, i.e. the number of events represented by this
         event class.

        :return: Size of this class.
        :rtype: int
        """
        return self.__size

    def set_size(self, size):
        """Sets the size of this event class, i.e. the number of represented
        instances.

        :param size: Number of events in this class.
        :type size: int
        """
        self.__size = size

    def increment_size(self):
        """Increments the size of this class by one, i.e. adds another event to
         the number of represented instances.

        """
        self.__size += 1

    def compare_to(self, obj):
        """Helper method to compares this object with the specified object for order.

        :param obj: The Object to be compared.
        :type obj: `XAttributeDiscrete`
        :return: A negative integer, zero, or a positive integer as this object
         is less than, equal to, or greater than the specified object.
        :rtype: int
        """
        return compare_to_string(self.__id, obj.get_id())

    def __str__(self):
        return self.__id

    def __hash__(self):
        return hash(self.__id)

    def __lt__(self, other):
        return True if self.compare_to(other) < 0 else False

    def __le__(self, other):
        return True if self.compare_to(other) <= 0 else False

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, XEventClass):
            return self.__id == other.get_id()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return True if self.compare_to(other) > 0 else False

    def __ge__(self, other):
        return True if self.compare_to(other) >= 0 else False

import uuid


class XID:
    """
    Implements a unique ID based on UUID.

    :param uuid_arg: The UUID implementing XID uniqueness.
    :type uuid_arg: uuid.UUID
    """

    @staticmethod
    def parse(id_string):
        """Parses an XID object from its text representation.

        :param id_string: Text representation of an XID.
        :type id_string: str
        :return: The parsed XID.
        :rtype: `XID`
        """
        return XID(uuid.UUID(id_string))

    def __init__(self, uuid_arg=None):
        if uuid_arg:
            self.__uuid = uuid_arg
        else:
            self.__uuid = uuid.uuid4()

    def get_uuid(self):
        """Retrieves the uuid value of this object.

        :return: The uuid attribute.
        :rtype: uuid.UUID
        """
        return self.__uuid

    def set_uuid(self, uuid_arg):
        """Assigns the uuid value of this object.

        :param uuid_arg: The new uuid value.
        :type uuid_arg: uuid.UUID
        """
        self.__uuid = uuid_arg

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XID`
        """
        return XID(self.__uuid)

    def compare_to(self, other):
        """Helper method to compares this object with the specified object for order.

        :param other: the Object to be compared.
        :type other: `XID`
        :return: A negative integer, zero, or a positive integer as this object
         is less than, equal to, or greater than the specified object.
        :rtype: int
        """
        if self.__uuid == other.get_uuid():
            return 0
        return 1 if self.__uuid > other.get_uuid() else -1

    def __str__(self):
        return str(self.__uuid).upper()

    def __hash__(self):
        return hash(self.__uuid)

    def __lt__(self, other):
        return True if self.compare_to(other) < 0 else False

    def __le__(self, other):
        return True if self.compare_to(other) <= 0 else False

    def __eq__(self, other):
        if isinstance(other, XID):
            return self.__uuid == other.get_uuid()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return True if self.compare_to(other) > 0 else False

    def __ge__(self, other):
        return True if self.compare_to(other) >= 0 else False

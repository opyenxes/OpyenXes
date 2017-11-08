from opyenxes.model.XAttribute import XAttribute


class XAttributeID(XAttribute):
    """ Attribute with ID type value.

    :param key: The key of the attribute.
    :type key: str
    :param value: The value of the attribute.
    :type value: `XID`
    :param extension: The extension defining the attribute (set to None, if
     the attribute is not associated to an extension)
    :type extension: `XExtension` or None
    """
    def __init__(self, key, value, extension=None):
        super().__init__(key, extension)
        self.__value = value

    def get_value(self):
        """Retrieves the ID value of this attribute

        :return: Value of this attribute
        :rtype: `XID`
        """
        return self.__value

    def set_value(self, value):
        """Assigns the ID value of this attribute.

        :param value: Value of the attribute.
        :type value: `XID`
        """
        self.__value = value

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XAttributeID`
        """
        clone = XAttributeID(self.get_key(), self.__value.clone(),
                             self.get_extension())
        return clone

    def compare_to(self, obj):
        """Helper method to compares this object with the specified object for order.

        :param obj: the Object to be compared.
        :type obj: `XAttributeID`
        :return: A negative integer, zero, or a positive integer as this object
         is less than, equal to, or greater than the specified object.
        :rtype: int
        """
        result = super().compare_to(obj)
        if result == 0:
            return self.__value.compare_to(obj.get_value())
        return result

    def __str__(self):
        return str(self.__value)

    def __hash__(self):
        return hash((self.get_key(), self.__value))

    def __lt__(self, other):
        return True if self.compare_to(other) < 0 else False

    def __le__(self, other):
        return True if self.compare_to(other) <= 0 else False

    def __eq__(self, other):
        if other is self:
            return True
        elif not isinstance(other, XAttributeID):
            return False
        else:
            return super().__eq__(other) and self.__value.__eq__(other.get_value())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return True if self.compare_to(other) > 0 else False

    def __ge__(self, other):
        return True if self.compare_to(other) >= 0 else False

from opyenxes.model.XAttributable import XAttributable
from opyenxes.utils.CompareUtils import compare_to_string


class XAttribute(XAttributable):
    """
    This class defines attributes used for describing meta-information about
    event log hierarchy elements. Attributes have a name (i.e., a key), which
    is string-based

    :param key: The key of the attribute.
    :type key: str
    :param extension: The extension defining the attribute (set to None, if
     the attribute is not associated to an extension)
    :type extension: `XExtension` or None
    """
    def __init__(self, key, extension=None):
        super(XAttribute, self).__init__()
        self.__key = key
        self.__extension = extension

    def get_key(self):
        """ Retrieves the key, i.e. unique identifier, of this attribute

        :return: The key of this attribute, as a string.
        :rtype: str
        """
        return self.__key

    def get_extension(self):
        """Retrieves the extension defining this attribute.

        :return: The extension of this attribute. May return null, if there is
         no extension defining this attribute.
        :rtype: `XExtension` or None
        """
        return self.__extension

    def compare_to(self, other):
        """Helper method to compares this object with the specified object for order.

        :param other: the Object to be compared.
        :type other: `XAttribute`
        :return: A negative integer, zero, or a positive integer as this object
         is less than, equal to, or greater than the specified object.
        :rtype: int
        """
        return compare_to_string(self.__key, other.get_key())

    def __hash__(self):
        return hash(self.__key)

    def __lt__(self, other):
        return True if self.compare_to(other) < 0 else False

    def __le__(self, other):
        return True if self.compare_to(other) <= 0 else False

    def __eq__(self, other):
        if isinstance(other, XAttribute):
            return self.__key == other.get_key()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return True if self.compare_to(other) > 0 else False

    def __ge__(self, other):
        return True if self.compare_to(other) >= 0 else False

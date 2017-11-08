from opyenxes.model.XAttribute import XAttribute
from datetime import datetime
import platform
import time


class XAttributeTimestamp(XAttribute):
    """ Attribute with datetime type value.

    :param key: The key of the attribute.
    :type key: str
    :param value: The value of the attribute.
    :type value: datetime or int
    :param extension: The extension defining the attribute (set to None, if
     the attribute is not associated to an extension)
    :type extension: `XExtension` or None
    """
    def __init__(self, key, value, extension=None):
        super().__init__(key, extension)
        self.__relative_zone = ""

        if isinstance(value, datetime):
            self.__value = value
        elif isinstance(value, int):
            self.__value = datetime.fromtimestamp(self.__timestamp(value))

    def get_value(self):
        """Retrieves the datetime value of this attribute

        :return: Value of this attribute
        :rtype: datetime
        """
        return self.__value

    def get_value_millis(self):
        return time.mktime(self.__value.timetuple()) * 1000

    def set_value(self, value):
        """Assigns the string value or datetime value of this attribute.

        :param value: Value of the attribute.
        :type value: datetime
        """
        self.__value = value

    def set_value_millies(self, value):
        self.__value = datetime.fromtimestamp(value / 1000.0)

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XAttributeLiteral`
        """
        clone = XAttributeTimestamp(self.get_key(), self.__value,
                                    self.get_extension())
        return clone

    def compare_to(self, obj):
        """Helper method to compares this object with the specified object for order.

        :param obj: the Object to be compared.
        :type obj: `XAttributeTimestamp`
        :return: A negative integer, zero, or a positive integer as this object
         is less than, equal to, or greater than the specified object.
        :rtype: int
        """
        result = super().compare_to(obj)
        if result == 0:
            if self.__value == obj.get_value():
                return 0
            return 1 if self.__value > obj.get_value() else -1
        return result

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        if self.__value.tzinfo is None:
            return "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.{:03}{}".format(
                self.__value.year,
                self.__value.month,
                self.__value.day,
                self.__value.hour,
                self.__value.minute,
                self.__value.second,
                self.__value.microsecond // 1000,
                "Z")

        return "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.{:03}{}".format(
            self.__value.year,
            self.__value.month,
            self.__value.day,
            self.__value.hour,
            self.__value.minute,
            self.__value.second,
            self.__value.microsecond // 1000,
            self.__value.tzname().replace("UTC", "").replace("+00:00", "Z").replace("-00:00", "Z"))

    def __lt__(self, other):
        return True if self.compare_to(other) < 0 else False

    def __le__(self, other):
        return True if self.compare_to(other) <= 0 else False

    def __eq__(self, other):
        if other is self:
            return True
        elif not isinstance(other, XAttributeTimestamp):
            return False
        else:
            return super().__eq__(other) and self.__value == other.get_value()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return True if self.compare_to(other) > 0 else False

    def __ge__(self, other):
        return True if self.compare_to(other) >= 0 else False

    def __timestamp(self, value):
        """ Windows timestamp workaround
        
        Creating the timestamp will fail if less than 86400 on Windows with
        Python 3.6.
        """
        value = value / 1000.0
        if (platform.system() == 'Windows') and (value < 86400):
            return 86400
        return value

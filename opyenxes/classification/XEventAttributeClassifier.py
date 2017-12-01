from opyenxes.model.XEvent import XEvent
from opyenxes.utils.CompareUtils import compare_to_string


class XEventAttributeClassifier:
    """Event classifier which considers two events as equal, if, for a set of
    given (configurable) attributes, they have the same values.

    :param name: Name of the classifier.
    :type name: str
    :param keys: List with the keys of the attributes used for event comparison.
    :type keys: list[str]
    """
    def __init__(self, name, keys):
        self.__name = name
        self.__keys = sorted(keys)

    def get_class_identity(self, event):
        """Retrieves the unique class identity string of a given event.

        :param event: The given event to transform in the identity string.
        :type event: `XEvent`
        :return: The string that represent that event with this classifier.
        :rtype: str
        """
        if len(self.__keys) == 1:
            attribute = event.get_attributes().get(self.__keys[0])
            if attribute:
                return str(attribute)
            return ""

        elif len(self.__keys) == 2:
            attribute_1 = event.get_attributes().get(self.__keys[0])
            attribute_2 = event.get_attributes().get(self.__keys[1])
            if attribute_1 and attribute_2:
                return "{}&&{}".format(str(attribute_1),
                                      str(attribute_2))
            elif attribute_1:
                return "{}&&".format(str(attribute_1))
            elif attribute_2:
                return "&&{}".format(str(attribute_2))

            return "&&"

        else:
            identity = []
            for key in self.__keys:
                attribute = event.get_attributes().get(key)
                if attribute:
                    identity.append(str(attribute))

            return "&&".join(identity)

    def name(self):
        """Returns the name of this comparator

        :return: The name of this comparator.
        :rtype: str
        """
        return self.__name

    def set_name(self, name):
        """Assigns a custom name to this classifier

        :param name: Name to be assigned to this classifier.
        :rtype: str
        """
        self.__name = name

    def same_event_class(self, event_a, event_b):
        """Checks whether two event instances correspond to the same event
        class, i.e. are equal in that sense.

        :param event_a: The first event to check.
        :type event_a: `XEvent`
        :param event_b: The second event to check with the first.
        :type event_b: `XEvent`
        :return: True if two event have the same event class, False otherwise.
        :rtype: bool
        """

        return self.get_class_identity(event_a) ==\
            self.get_class_identity(event_b)

    def get_defining_attribute_keys(self):
        """Retrieves the set of attribute keys which are used in this event
        classifier (May be used for the construction of events that are not
        part of an existing event class).

        :return: An array of attribute keys, which are used for defining this
         classifier.
        :rtype: list[str]
        """
        return self.__keys

    def compare_to(self, obj):
        """Helper method to compares this object with the specified object for
        order.

        :param obj: the Object to be compared.
        :type obj: `XAttributeDiscrete`
        :return: A negative integer, zero, or a positive integer as this object
         is less than, equal to, or greater than the specified object.
        :rtype: int
        """
        if self.__name != obj.name():
            return compare_to_string(self.__name, obj.name())
        if len(self.__keys) != len(obj.get_defining_attribute_keys()):
            return len(self.__keys) - len(obj.get_defining_attribute_keys())
        for key_1, key_2 in zip(self.__keys, obj.get_defining_attribute_keys()):
            if key_1 != key_2:
                return compare_to_string(key_1, key_2)
        return 0

    def __str__(self):
        return self.__name

    def __hash__(self):
        return (31 + hash(tuple(self.__keys))) * 31 + hash(self.__name)

    def __lt__(self, other):
        return True if self.compare_to(other) < 0 else False

    def __le__(self, other):
        return True if self.compare_to(other) <= 0 else False

    def __eq__(self, other):
        if isinstance(other, XEventAttributeClassifier):
            return self.compare_to(other) == 0
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return True if self.compare_to(other) > 0 else False

    def __ge__(self, other):
        return True if self.compare_to(other) >= 0 else False

class XAttributeMap(dict):
    """An attribute map is used to hold a set of attributes, indexed by their
    key strings, for event log hierarchy elements

    :param dictionary: Dictionary with attributes for add in this object.
    :type dictionary: dict or None
    """
    def __init__(self, dictionary=None):
        super().__init__()
        if dictionary:
            self.update(dictionary)

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XAttributeMap`
        """
        clone = XAttributeMap()
        for key in self.keys():
            clone[key] = self[key]

        return clone

    def is_empty(self):
        """Return if this map contains elements

        :return: Returns True if this map contains element, False otherwise.
        :rtype: bool
        """
        return len(self) == 0

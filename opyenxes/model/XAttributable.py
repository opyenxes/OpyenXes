from opyenxes.model.XAttributeMap import XAttributeMap


class XAttributable:
    """
    This class is implemented by all elements of the log hierarchy, which can
    be equipped with attributes

    :param attribute: A `XAttributeMap` with the attribute for this class.
    :type attribute: `XAttributeMap`
    """
    def __init__(self, attribute=None):
        if attribute:
            self.__attributes = attribute
        else:
            self.__attributes = XAttributeMap()

    def get_extensions(self):
        """Retrieves the extensions used by this element, i.e. the extensions
        used by all attributes of this element, and the element itself

        :return: A set of extensions
        :rtype: set(`XExtension`)
        """
        extensions = set()
        for attribute in self.__attributes.values():
            extension = attribute.get_extensions()
            if len(extension) != 0:
                extensions.add(extension)
        return extensions

    def get_attributes(self):
        """Retrieves the attributes set for this element.

        :return: A map of attributes.
        :rtype: `XAttributeMap`
        """
        return self.__attributes

    def set_attributes(self, attributes):
        """Sets the map of attributes for this element.

        :param attributes: A map of attributes
        :type attributes: `XAttributeMap`
        """
        self.__attributes = attributes

    def has_attributes(self):
        """Checks for the existence of attributes

        :return: True if this element has any attributes; False otherwise.
        :rtype: bool
        """
        return not self.__attributes.is_empty()

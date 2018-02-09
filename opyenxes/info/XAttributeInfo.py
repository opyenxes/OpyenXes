from opyenxes.utils.XAttributeUtils import XAttributeUtils
from opyenxes.model.XAttribute import XAttribute


class XAttributeInfo:
    """This class provides aggregate information about attributes within one
    container in the log type hierarchy. For example, it may store information
    about all event attributes in a log.

    """
    def __init__(self):
        self.__key_map = dict()
        self.__type_map = dict()
        self.__extension_map = dict()
        self.__no_extension_set = set()
        self.__frequencies = dict()
        self.__total_frequencies = 0

    def get_attributes(self):
        """Provides access to prototypes of all registered attributes.

        :return: A tuple of attribute prototypes.
        :rtype: tuple
        """
        return tuple(self.__key_map.values())

    def get_attribute_keys(self):
        """Provides access to prototypes of all registered attributes' keys.

        :return: A tuple of attribute keys.
        :rtype: tuple
        """
        return tuple(self.__key_map.keys())

    def get_frequency(self, element):
        """Returns the total frequency, i.e. number of occurrences, for the
        requested attribute.

        :param element: Key of an attribute or an attribute.
        :type element: str or `XAttribute`
        :return: Total frequency of that attribute as registered.
        :rtype: int
        """
        if isinstance(element, str):
            return self.__frequencies.get(element)
        elif isinstance(element, XAttribute):
            return self.__frequencies.get(element.get_key())

    def get_relative_frequency(self, element):
        """Returns the relative frequency, i.e. between 0 and 1, for the
        requested attribute.

        :param element: Key of an attribute or an attribute.
        :type element: str or `XAttribute`
        :return: Relative frequency of that attribute as registered.
        :rtype: int
        """
        if isinstance(element, str):
            return self.__frequencies.get(element) / self.__total_frequencies
        elif isinstance(element, XAttribute):
            return self.__frequencies.get(element.get_key()) / self.__total_frequencies

    def get_attributes_for_type(self, type_argument):
        """For a given type, returns prototypes of all registered attributes
        with that type.

        :param type_argument: Requested attribute type.
        :type type_argument: type
        :return: A tuple of attribute prototypes registered for that type.
        :rtype: tuple
        """
        type_set = self.__type_map.get(type_argument)
        if type_set is None:
            type_set = set()

        return tuple(type_set)

    def get_keys_for_type(self, type_argument):
        """For a given type, returns the keys of all registered attributes with
        that type.


        :param type_argument: Requested attribute type.
        :type type_argument: type
        :return: A tuple of attribute keys registered for that type.
        :rtype: tuple
        """
        type_collection = self.get_attributes_for_type(type_argument)
        key_set = set()
        for attribute in type_collection:
            key_set.add(attribute.get_key())

        return tuple(key_set)

    def get_attributes_for_extension(self, extension):
        """For a given extension, returns prototypes of all registered
        attributes defined by that extension.

        :param extension:  Requested attribute extension.
        :type extension: `XExtension`
        :return: A tuple of attribute prototypes registered for that extension.
        :rtype: tuple
        """
        if extension is None:
            return self.get_attributes_without_extension()
        else:
            extension_set = self.__extension_map.get(extension)
            if extension_set is None:
                extension_set = set()
            return tuple(extension_set)

    def get_keys_for_extension(self, extension):
        """For a given extension, returns the keys of all registered attributes
        defined by that extension.

        :param extension:  Requested attribute extension.
        :type extension: `XExtension`
        :return: A tuple of attribute keys registered for that extension.
        :rtype: tuple
        """
        extension_collection = self.get_attributes_for_extension(extension)
        key_set = set()
        for attribute in extension_collection:
            key_set.add(attribute.get_key())

        return tuple(key_set)

    def get_attributes_without_extension(self):
        """Returns prototypes of all registered attributes defined by no extension.

        :return: A tuple of attribute prototypes registered for no extension.
        :rtype: tuple
        """
        return self.__no_extension_set

    def get_keys_without_extension(self):
        """Returns keys of all registered attributes defined by no extension.

        :return: A tuple of attribute keys registered for no extension.
        :rtype: tuple
        """
        return self.get_keys_for_extension(None)

    def register(self, attribute):
        """Registers a concrete attribute with this registry.

        :param attribute: Attribute to be registered.
        :type attribute: `XAttribute`
        """
        if attribute.get_key() not in self.__key_map:
            prototype = XAttributeUtils.derive_prototype(attribute)
            self.__key_map[attribute.get_key()] = prototype
            self.__frequencies[attribute.get_key()] = 1
            type_set = self.__type_map.get(XAttributeUtils.get_type(prototype))
            if type_set is None:
                type_set = set()
            self.__type_map[XAttributeUtils.get_type(prototype)] = type_set
        else:
            self.__frequencies[attribute.get_key()] += 1

        self.__total_frequencies += 1

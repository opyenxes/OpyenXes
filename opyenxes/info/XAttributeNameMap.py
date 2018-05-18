from opyenxes.model.XAttribute import XAttribute


class XAttributeNameMap:
    """Implements an attribute name mapping.

    :param name: Name of the mapping.
    :type name: str
    """
    def __init__(self, name):
        self.__name = name
        self.__mapping = dict()

    def get_mapping_name(self):
        """Returns the name of this mapping.

        :return: The name of this mapping.
        :rtype: str
        """
        return self.__name

    def map(self, attribute):
        """Returns the name mapped onto the provided attribute by this mapping.
        If no mapping for the given attribute is provided by this map, null is
        returned.

        :param attribute: Attribute or Attribute key to retrieve mapping for.
        :type attribute: `XAttribute` or Str
        :return: The mapping for the given attribute key, or null, if no such
         mapping exists.
        :rtype: str
        """
        if isinstance(attribute, str):
            return self.__mapping.get(attribute)
        elif isinstance(attribute, XAttribute):
            return self.map(attribute.get_key())

    def register_mapping(self, attribute, alias):
        """Registers a mapping for a given attribute or attribute key.

        :param attribute: Attribute or attribute key for which to register a
         mapping.
        :type attribute: `XAttribute` or str
        :param alias: Alias string to map the attribute to.
        :type alias: str
        """
        if isinstance(alias, str):
            if isinstance(attribute, str):
                self.__mapping[attribute] = alias
            elif isinstance(attribute, XAttribute):
                self.register_mapping(attribute.get_key(), alias)

    def __str__(self):
        sb = list()
        sb.append("Attribute name map: ")
        sb.append(self.__name)
        for key in self.__mapping.keys():
            sb.append("\n")
            sb.append(key)
            sb.append(" -> ")
            sb.append(self.__mapping[key])

        return "".join(sb)

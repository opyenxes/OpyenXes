from opyenxes.info.XAttributeNameMap import XAttributeNameMap
from opyenxes.utils.SingletonClassGenerator import XGlobalAttributeNameMapMetaclass
from opyenxes.model.XAttribute import XAttribute


class XGlobalAttributeNameMap(metaclass=XGlobalAttributeNameMapMetaclass):
    """This singleton class implements a global attribute name mapping facility
    and can manage a number of attribute name mappings. Further, this class also
    acts as a proxy to the standard mapping, i.e. it can be used directly as a
    attribute name mapping instance.

    """
    MAPPING_STANDARD = "EN"
    MAPPING_ENGLISH = "EN"
    MAPPING_GERMAN = "DE"
    MAPPING_DUTCH = "NL"
    MAPPING_FRENCH = "FR"
    MAPPING_ITALIAN = "IT"
    MAPPING_SPANISH = "ES"
    MAPPING_PORTUGUESE = "PT"

    def __init__(self):
        self.__standard_mapping = XAttributeNameMap("EN")
        self.__mappings = {"EN": self.__standard_mapping}

    def get_available_mapping_names(self):
        """Returns the names of all available mappings. Note that referenced
        mappings may be empty.

        :return: A tuple of names of all available mappings.
        :rtype: tuple
        """
        return tuple(self.__mappings.keys())

    def get_available_mappings(self):
        """Returns all available mappings. Note that returned mappings may be empty.

        :return: A tuple of all available mappings.
        :rtype: tuple
        """
        result = set()
        for values in self.__mappings.values():
            result.add(values)

        return tuple(result)

    def get_mapping(self, name):
        """Provides access to a specific attribute name mapping by its name. If
        the requested mapping does not exist yet, a new mapping will be created,
        added to the set of managed mappings, and returned. This means, this
        method will always return a mapping, but this could be empty.

        :param name: Name of the requested mapping.
        :type name: str
        :return: The requested mapping, as stored in this facility (or newly created).
        :rtype: `XAttributeNameMap`
        """
        mapping = self.__mappings.get(name)
        if mapping is None:
            mapping = XAttributeNameMap(name)
            self.__mappings[name] = mapping

        return mapping

    def get_standard_mapping(self):
        """Retrieves the standard attribute name mapping, i.e. the EN english
        language mapping.

        :return: The standard mapping.
        :rtype: `XAttributeNameMap`
        """
        return self.__standard_mapping

    def map_safely(self, attribute, mapping):
        """Maps an attribute safely, using the given attribute mapping. Safe
        mapping attempts to map the attribute using the given mapping first.
        If this does not succeed, the standard mapping (EN) will be used for
        mapping. If no mapping is available in the standard mapping, the
        original attribute key is returned unchanged. This way, it is always
        ensured that this method returns a valid string for naming attributes.

        :param attribute: Attribute to map or key of the attribute to map.
        :type attribute: `XAttribute` or str
        :param mapping: Name of the mapping to be used preferably or attribute
         name map to be used preferably.
        :type mapping: str or `XAttributeNameMap`
        :return: The safe mapping for the given attribute.
        :rtype: str
        """
        if isinstance(attribute, XAttribute) and isinstance(mapping, XAttributeNameMap):
            return self.map_safely(attribute.get_key(), mapping)

        elif isinstance(attribute, str) and isinstance(mapping, XAttributeNameMap):
            alias = None
            if mapping is not None:
                alias = mapping.map(attribute)

            if alias is None:
                alias = self.__standard_mapping.map(attribute)

            if alias is None:
                alias = attribute

            return alias

        elif isinstance(attribute, XAttribute) and isinstance(mapping, str):
            return self.map_safely(attribute, self.__mappings.get(mapping))

        elif isinstance(attribute, str) and isinstance(mapping, str):
            return self.map_safely(attribute, self.__mappings.get(mapping))

    def register_mapping(self, mapping_name, attribute_key, alias):
        """Registers a known attribute for mapping in a given attribute name
        map. **IMPORTANT**: This method should only be called when one intends
        to create, or add to, the global attribute name mapping.

        :param mapping_name: Name of the mapping to register with.
        :type mapping_name: str
        :param attribute_key: Attribute key to be mapped.
        :type attribute_key: str
        :param alias: Alias to map the given attribute to.
        :type alias: str

        """
        mapping = self.get_mapping(mapping_name)
        mapping.register_mapping(attribute_key, alias)

    @staticmethod
    def get_mapping_name():
        """Returns the name of this mapping.

        :return: The name of this mapping.
        :rtype: str
        """
        return "EN"

    def map(self, attribute):
        """Returns the name mapped onto the provided attribute by this mapping.
        If no mapping for the given attribute is provided by this map, null is
        returned.

        :param attribute: Attribute or attribute key to retrieve mapping for.
        :type attribute: str or `XAttribute`
        :return: The mapping for the given attribute, or null, if no such
         mapping exists.
        :rtype: str
        """
        return self.__standard_mapping.map(attribute)

    def __str__(self):
        sb = list()
        sb.append("Global attribute name map.\n\nContained maps:\n\n")
        for values in self.__mappings.values():
            sb.append(str(values))
            sb.append("\n\n")
        return "".join(sb)

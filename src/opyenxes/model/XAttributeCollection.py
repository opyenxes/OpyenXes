from opyenxes.model.XAttribute import XAttribute


class XAttributeCollection(XAttribute):
    """This Class is implemented by all attribute that contain more attributes,
    for example list and container.

    :param key: The key of the attribute.
    :type key: str
    :param extension: The extension defining the attribute (set to None, if
     the attribute is not associated to an extension)
    :type extension: `XExtension` or None
    """
    def __init__(self, key, extension=None):
        super().__init__(key, extension)
        self.__collection = list()

    def add_to_collection(self, attribute):
        """Add attribute in the collection of this object.

        :param attribute: The attribute to add in the collection
        :type attribute: `XAttribute`
        """
        if self.__collection is not None:
            self.__collection.append(attribute)

    def get_collection(self):
        """Retrieves the list with the attribute of this object.

        :return: List of attributes
        :rtype: list(`XAttribute`)
        """
        if self.__collection is None:
            return self.get_attributes().values()
        return self.__collection.copy()

    def __str__(self):
        text = []
        sep = "["
        for attribute in self.get_collection():
            text.append(sep)
            sep = ","
            text.append(attribute.get_key())
            text.append(":")
            text.append(str(attribute))

        if len(text) == 0:
            text.append("[")

        text.append("]")
        return "".join(text)

from abc import abstractclassmethod
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.model.XAttribute import XAttribute


class XAbstractNestedAttributeSupport:
    """This class offers generic support for extracting and assigning values to
    and from nested attributes.

    """
    @abstractclassmethod
    def assign_value(self, element, value):
        """Abstract method to assign a value to an element.

        :param element: The element to assign the value to.
        :type element: XAttribute
        :param value: The value to be assigned.
        :type value: Any
        """
        pass

    @abstractclassmethod
    def extract_value(self, element):
        """ Abstract method to extract a value from an element.

        :param element:  The element to extract the value from.
        :type element: `XAttribute`
        """
        pass

    def extract_values(self, element):
        """Retrieves a map containing all values for all child attributes of an
        element. For example, the XES fragment: ::

            <trace>
                <string key="key.1" value="">
                    <float key="ext:attr" value="val.1"/>
                    <string key="key.1.1" value="">
                        <float key="ext:attr" value="val.1.1"/>
                    </string>
                    <string key="key.1.2" value="">
                        <float key="ext:attr" value="val.1.2"/>
                    </string>
                </string>
                <string key="key.2" value="">
                   <float key="ext:attr" value="val.2"/>
                </string>
                <string key="key.3" value="">
                   <float key="ext:attr" value="val.3"/>
                </string>
            </trace>

        should result into the following:::

            {"key.1": val.1, "key.2": val.2, "key.3": val.3}

        :param element: Element to retrieve all values for.
        :type element: `XAttributable`
        :return: Dictionary with all child keys to values.
        :rtype: dict(str: any}
        """
        values = dict()
        nested_values = self.extract_nested_values(element)
        for keys in nested_values.keys():
            if len(keys) == 1:
                values[keys[0]] = nested_values[keys]
        return values

    def extract_nested_values(self, element):
        """Retrieves a map containing all values for all descending attributes
        of an element. For example, the XES fragment:::

            <trace>
                <string key="key.1" value="">
                    <float key="ext:attr" value="val.1"/>
                    <string key="key.1.1" value="">
                        <float key="ext:attr" value="val.1.1"/>
                    </string>
                    <string key="key.1.2" value="">
                        <float key="ext:attr" value="val.1.2"/>
                    </string>
                </string>
                <string key="key.2" value="">
                   <float key="ext:attr" value="val.2"/>
                </string>
                <string key="key.3" value="">
                   <float key="ext:attr" value="val.3"/>
                </string>
            </trace>


        should result into the following:::

            {["key.1"]: val.1, ["key.1", "key.1.1"]: val.1.1, ["key.1", "key.1.2"]: val.1.2, ["key.2"]: val.2, ["key.3"]: val.3}


        :param element: Element to retrieve all values for.
        :type element: `XAttributable`
        :return: Dictionary with all descending keys to values.
        :rtype: dict(list[str]: Any)
        """
        nested_values = dict()
        for attr in element.get_attributes().values():
            keys = list()
            keys.append(attr.get_key())
            self.__extract_nested_values_private__(attr, nested_values, keys)
        return nested_values

    def __extract_nested_values_private__(self, element, nested_values, keys):
        """ helper and private method to assign the nested values.

        """
        value = self.extract_value(element)
        if value:
            nested_values[keys] = value

        for attr in element.get_attributes().values():
            new_keys = list(keys)
            new_keys.append(element.get_key())
            self.__extract_nested_values_private__(attr, nested_values, new_keys)

    def assign_values(self, element, values):
        """Assigns (to the given element) multiple values given their keys. Note
        that as a side effect this method creates attributes when it does not
        find an attribute with the proper key. For example, the call:::

            assign_values(event, {"key.1": val.1, "key.2": val.2, "key.3": val.3})

        should result into the following XES fragment:::

            <event>
                <string key="key.1" value="">
                    <float key="ext:attr" value="val.1"/>
                </string>
                <string key="key.2" value="">
                   <float key="ext:attr" value="val.2"/>
                </string>
                <string key="key.3" value="">
                   <float key="ext:attr" value="val.3"/>
                </string>
            </event>

        :param element: Element to assign the values to.
        :type element: `XAttributable`
        :param values: dictionary with keys to values which are to be assigned.
        :type values: dict(str: Any)
        """
        nested_values = dict()
        for key in values.keys():
            keys = list()
            keys.append(key)
            nested_values[keys] = values[key]

        self.assign_nested_values(element, nested_values)

    def assign_nested_values(self, element, amounts):
        """Assigns (to the given event) multiple values given their key lists.
        The i-th element in the key list should correspond to an i-level
        attribute with the prescribed key. Note that as a side effect this
        method creates attributes when it does not find an attribute with the
        proper key. For example, the call:::

            assignNestedValues(event, {["key.1"]: val.1, ["key.1", "key.1.1"]: val.1.1, ["key.1", "key.1.2"]: val.1.2, ["key.2"]: val.2, ["key.3"]: val.3})

        should result into the following XES fragment:::

            <event>
                <string key="key.1" value="">
                    <float key="ext:attr" value="val.1"/>
                    <string key="key.1.1" value="">
                        <float key="ext:attr" value="val.1.1"/>
                    </string>
                    <string key="key.1.2" value="">
                        <float key="ext:attr" value="val.1.2"/>
                    </string>
                </string>
                <string key="key.2" value="">
                   <float key="ext:attr" value="val.2"/>
                </string>
                <string key="key.3" value="">
                   <float key="ext:attr" value="val.3"/>
                </string>
            </event>

        :param element: Element to assign the values to.
        :type element: `XAttributable`
        :param amounts: Dictionary with key lists to values which are to be
         assigned.
        :type amounts: dict(list[str]: Any)
        """

        for keys in amounts.keys():
            self.__assign_nested_values_private__(element, keys, amounts[keys])

    def __assign_nested_values_private__(self, element, keys, value):
        """ helper and private method to assign the nested values.

        """
        if len(keys) == 0:
            if isinstance(element, XAttribute):
                self.assign_value(element, value)
        else:
            key = keys[0]
            keys_tail = keys[1:]
            if key in element.get_attributes():
                attr = element.get_attributes()[key]
            else:
                attr = XFactoryRegistry().current_default().create_attribute_literal(key, "", None)
                element.get_attributes()[key] = attr
            self.__assign_nested_values_private__(attr, keys_tail, value)

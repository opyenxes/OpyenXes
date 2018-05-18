from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.extension.std.XAbstractNestedAttributeSupport import XAbstractNestedAttributeSupport
from opyenxes.extension.XExtension import XExtension
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.utils.SingletonClassGenerator import XConceptExtensionMetaclass, XCostAmountMetaclass, XCostDriverMetaclass, XCostTypeMetaclass


class XCostAmount(XAbstractNestedAttributeSupport, metaclass=XCostAmountMetaclass):
    """Class which value contains the cost amount for a cost driver.

    Uses the singleton metaclass
    """
    def extract_value(self, attribute):
        """Abstract method to extract a value from an element.

        :param attribute: The element to extract the value from.
        :type attribute: `XAttribute`
        :return: The extracted value.
        :rtype: float
        """
        return XCostExtension().extract_amount(attribute)

    def assign_value(self, attribute, value):
        """Abstract method to assign a value to an element.

        :param attribute: The element to assign the value to.
        :type attribute: `XAttribute`
        :param value: The value to be assigned.
        :type value: float
        """
        XCostExtension().assign_amount(attribute, value)


class XCostDriver(XAbstractNestedAttributeSupport, metaclass=XCostDriverMetaclass):
    """Class which value contains the cost amount for a cost driver.

    Uses the singleton metaclass
    """
    def extract_value(self, attribute):
        """Abstract method to extract a value from an element.

        :param attribute: The element to extract the value from.
        :type attribute: `XAttribute`
        :return: The extracted value.
        :rtype: str
        """
        return XCostExtension().extract_driver(attribute)

    def assign_value(self, attribute, value):
        """Abstract method to assign a value to an element.

        :param attribute: The element to assign the value to.
        :type attribute: `XAttribute`
        :param value: The value to be assigned.
        :type value: str
        """
        XCostExtension().assign_driver(attribute, value)


class XCostType(XAbstractNestedAttributeSupport, metaclass=XCostTypeMetaclass):
    """Class which value contains the cost type (e.g., Fixed,Overhead, Materials).

    Uses the singleton metaclass
    """
    def extract_value(self, attribute):
        """Abstract method to extract a value from an element.

        :param attribute: The element to extract the value from.
        :type attribute: `XAttribute`
        :return: The extracted value.
        :rtype: str
        """
        return XCostExtension().extract_type(attribute)

    def assign_value(self, attribute, value):
        """Abstract method to assign a value to an element.

        :param attribute: The element to assign the value to.
        :type attribute: `XAttribute`
        :param value: The value to be assigned.
        :type value: str
        """
        XCostExtension().assign_type(attribute, value)


class XCostExtension(XExtension, metaclass=XConceptExtensionMetaclass):
    """This extension provides costs for traces and events. It defines five
    attributes:

    * cost total: Contains total cost incurred for a trace or an event.
      The value represents the sum of all the cost amounts within the
      element.
    * cost currecny: Any valid currency format.
    * cost amount: The value contains the cost amount for a cost driver.
    * cost driver: The value contains the id for the cost driver used to
      calculate the cost.
    * cost type: The value contains the cost type (e.g., Fixed, Overhead,
      Materials).

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Cost", "cost", urlparse("http://www.xes-standard.org/cost.xesext"))
        factory = XFactoryRegistry().current_default()

        self.ATTR_TOTAL = factory.create_attribute_continuous("cost:total", 0.0, self)
        self.ATTR_CURRENCY = factory.create_attribute_literal("cost:currency", "UNKNOWN", self)
        self.ATTR_AMOUNT = factory.create_attribute_continuous("cost:amount", 0.0, self)
        self.ATTR_DRIVER = factory.create_attribute_literal("cost:driver", "UNKNOWN", self)
        self.ATTR_TYPE = factory.create_attribute_literal("cost:type", "UNKNOWN", self)

        self.get_trace_attributes().add(self.ATTR_TOTAL.clone())
        self.get_trace_attributes().add(self.ATTR_CURRENCY.clone())
        self.get_event_attributes().add(self.ATTR_TOTAL.clone())
        self.get_event_attributes().add(self.ATTR_CURRENCY.clone())
        self.get_event_attributes().add(self.ATTR_AMOUNT.clone())
        self.get_event_attributes().add(self.ATTR_DRIVER.clone())
        self.get_event_attributes().add(self.ATTR_TYPE.clone())

        XGlobalAttributeNameMap().register_mapping("EN", "cost:total", "Total Cost")
        XGlobalAttributeNameMap().register_mapping("EN", "cost:currency", "Currency of Cost")
        XGlobalAttributeNameMap().register_mapping("EN", "cost:amount", "Cost Amount")
        XGlobalAttributeNameMap().register_mapping("EN", "cost:driver", "Cost Driver")
        XGlobalAttributeNameMap().register_mapping("EN", "cost:type", "Cost Type")

    @staticmethod
    def extract_total(element):
        """Retrieves the total costs of a trace or event, if set by this
        extension's total attribute.

        :param element: Trace or Event to retrieve total costs for.
        :type element: `XTrace` or `XEvent`
        :return: The requested total costs.
        :rtype: float
        """
        attribute = element.get_attributes().get("cost:total")
        if attribute:
            return attribute.get_value()
        return None

    def assign_total(self, element, total):
        """Assigns any trace or event its total costs, as defined by this
        extension's total attribute.

        :param element:  Trace or Event to assign total costs to.
        :type element: `XTrace` or `XEvent`
        :param total: The total costs to be assigned.
        :type total: float
        """
        if total is not None and total > 0:
            attr = self.ATTR_TOTAL.clone()
            attr.set_value(total)
            element.get_attributes()["cost:total"] = attr

    @staticmethod
    def extract_currency(element):
        """Retrieves the cost currency for an event or trace, if set by this
        extension's currency attribute.

        :param element: Event or Trace to retrieve currency for.
        :type element: `XTrace` or `XEvent`
        :return: The requested cost currency.
        :rtype: str
        """
        attribute = element.get_attributes().get("cost:currency")
        if attribute:
            return attribute.get_value()
        return None

    def assign_currency(self, element, currency):
        """Assigns any trace or event its cost currency, as defined by this
        extension's currency attribute.

        :param element: Trace or Event to assign cost currency to.
        :type element: `XEvent` or `XEvent`
        :param currency: The currency to be assigned.
        :type currency: str
        """
        if currency is not None and len(currency.strip()) > 0:
            attr = self.ATTR_CURRENCY.clone()
            attr.set_value(currency)
            element.get_attributes()["concept:name"] = attr

    @staticmethod
    def extract_amount(attribute):
        """Retrieves the cost amount for an attribute, if set by this
        extension's amount attribute.

        :param attribute: Attribute element to retrieve cost amount for.
        :type attribute: `XAttribute`
        :return: The requested cost amount.
        :rtype: float
        """
        attr = attribute.get_attributes().get("cost:amount")
        if attr:
            return attr.get_value()
        return None

    @staticmethod
    def extract_amounts(element):
        """Retrieves a map containing all cost amounts for all child attributes
        of an event. For example, the XES fragment:::

            <trace>
                <string key="a" value="">
                    <float key="cost:amount" value="10.00"/>
                    <string key="b" value="">
                        <float key="cost:amount" value="20.00"/>
                    </string>
                    <string key="c" value="">
                        <float key="cost:amount" value="30.00"/>
                    </string>
                </string>
                <string key="b" value="">
                    <float key="cost:amount" value="15.00"/>
                </string>
                <string key="c" value="">
                    <float key="cost:amount" value="25.00"/>
                </string>
            </trace>

        should result into the following:::

            {"a": 10.00, "b": 15.00, "c": 25.00}

        :param element: Trace or Event to retrieve all cost amounts for.
        :type element: `XTrace` or `XEvent`
        :return: Dictionary with all child keys to cost amounts.
        :rtype: dict(str: float)
        """
        return XCostAmount().extract_values(element)

    @staticmethod
    def extract_nested_amounts(element):
        """Retrieves a map containing all cost amounts for all child attributes
        of an event. For example, the XES fragment:::

            <trace>
                <string key="a" value="">
                    <float key="cost:amount" value="10.00"/>
                    <string key="b" value="">
                        <float key="cost:amount" value="20.00"/>
                    </string>
                    <string key="c" value="">
                        <float key="cost:amount" value="30.00"/>
                    </string>
                </string>
                <string key="b" value="">
                    <float key="cost:amount" value="15.00"/>
                </string>
                <string key="c" value="">
                    <float key="cost:amount" value="25.00"/>
                </string>
            </trace>

        should result into the following:::

            {["a"]: 10.00, ["a", "b"]: 20.00, ["a", "c"]: 30.00, ["b"]: 15.00, ["c"]: 25.00}

        :param element: Trace or Event to retrieve all cost amounts for.
        :type element: `XTrace` or `XEvent`
        :return: Dictionary with all descending keys to cost amounts.
        :rtype: dict(list[str]: float)
        """
        return XCostAmount().extract_nested_values(element)

    def assign_amount(self, attribute, amount):
        """Assigns any attribute its cost amount, as defined by this extension's
        amount attribute.

        :param attribute: Attribute to assign cost amount to
        :type attribute: `XAttribute`
        :param amount: The cost amount to be assigned.
        :type amount: float
        """
        if amount is not None and amount > 0:
            attr = self.ATTR_AMOUNT.clone()
            attr.set_value(amount)
            attribute.get_attributes()["cost:amount"] = attr

    @staticmethod
    def assign_amounts(element, amounts):
        """Assigns (to the given trace or event) multiple amounts given their
        keys. Note that as a side effect this method creates attributes when it
        does not find an attribute with the proper key. For example, the call:::

            assign_amounts(trace, {"a": 10.00, "b": 15.00, "c": 25.00})

        should result into the following XES fragment:::

            <trace>
                <string key="a" value="">
                    <float key="cost:amount" value="10.00"/>
                </string>
                <string key="b" value="">
                    <float key="cost:amount" value="15.00"/>
                </string>
                <string key="c" value="">
                    <float key="cost:amount" value="25.00"/>
                </string>
            </trace>

        :param element: Trace or Event to assign the amounts to.
        :type element: `XEvent` or `XTrace`
        :param amounts:  Dictionary with keys to amounts which are to be assigned.
        :type amounts: dict(str: float)
        """
        XCostAmount().assign_values(element, amounts)

    @staticmethod
    def assign_nested_amounts(element, amounts):
        """Assigns (to the given trace or event) multiple amounts given their
        key lists. The i-th element in the key list should correspond to an
        i-level attribute with the prescribed key. Note that as a side effect
        this method creates attributes when it does not find an attribute with
        the proper key. For example, the call:::

            assign_nested_amounts(trace, {["a"]: 10.00], ["a", "b"]: 20.00, ["a", "c"]: 30.00, ["b"]: 15.00, ["c"]: 25.00})

        should result into the following XES fragment:::

            <trace>
                <string key="a" value="">
                    <float key="cost:amount" value="10.00"/>
                    <string key="b" value="">
                        <float key="cost:amount" value="20.00"/>
                    </string>
                    <string key="c" value="">
                        <float key="cost:amount" value="30.00"/>
                    </string>
                </string>
                <string key="b" value="">
                   <float key="cost:amount" value="15.00"/>
                </string>
                <string key="c" value="">
                   <float key="cost:amount" value="25.00"/>
                </string>
            </trace>

        :param element: Trace or Event to assign the amounts to.
        :type element: `XEvent` or `XTrace`
        :param amounts:  Dictionary with list of keys to amounts which are to
         be assigned.
        :type amounts: dict(list[str]: float)
        """
        XCostAmount().assign_nested_values(element, amounts)

    @staticmethod
    def extract_driver(attribute):
        """Retrieves the cost driver for an attribute, if set by this extension's
        driver attribute.

        :param attribute: Attribute element to retrieve cost driver for.
        :type attribute: `XAttribute`
        :return: The requested cost driver.
        :rtype: str
        """
        attr = attribute.get_attributes().get("cost:driver")
        if attr:
            return attr.get_value()
        return None

    @staticmethod
    def extract_drivers(element):
        """Retrieves a map containing all cost drivers for all child attributes
        of a trace or event.

        :param element: Trace or Event to retrieve all cost drivers for.
        :type element: `XTrace` or `XEvent`
        :return: Dictionary with all child keys to cost drivers.
        :rtype: dict(str: str)
        """
        return XCostDriver().extract_values(element)

    @staticmethod
    def extract_nested_drivers(element):
        """Retrieves a map containing all cost drivers for all descending
        attributes of a trace or event.

        :param element: Trace or Event to retrieve all cost drivers for.
        :type element: `XTrace` or `XEvent`
        :return: Dictionary with all descending keys to cost drivers.
        :rtype: dict(list[str]: str)
        """
        return XCostDriver().extract_nested_values(element)

    def assign_driver(self, attribute, driver):
        """Assigns any attribute its cost driver, as defined by this
        extension's driver attribute.

        :param attribute: Attribute to assign cost driver to.
        :type attribute: `XAttribute`
        :param driver: The cost driver to be assigned.
        :type driver: str
        """
        if driver is not None and len(driver.strip()) > 0:
            attr = self.ATTR_DRIVER.clone()
            attr.set_value(driver)
            attribute.get_attributes()["cost:driver"] = attr

    @staticmethod
    def assign_drivers(element, drivers):
        """Assigns (to the given trace or event) multiple cost drivers given
        their keys. Note that as a side effect this method creates attributes
        when it does not find an attribute with the proper key.

        :param element: Trace or Event to assign the cost drivers to.
        :type element: `XTrace` or `XEvent`
        :param drivers: Dictionary with keys to cost drivers which are to be assigned.
        :type drivers: dict(str: str)
        """
        XCostDriver().assign_values(element, drivers)

    @staticmethod
    def assign_nested_drivers(element, drivers):
        """Assigns (to the given trace) multiple cost drivers given their key
        lists. The i-th element in the key list should correspond to an i-level
        attribute with the prescribed key. Note that as a side effect this
        method creates attributes when it does not find an attribute with the
        proper key.

        :param element: Trace or Event to assign the cost drivers to.
        :type element: `XTrace` or `XEvent`
        :param drivers: Dictionary with keys to cost drivers which are to be assigned.
        :type drivers: dict(list[str]: str)
        """
        XCostDriver().assign_nested_values(element, drivers)

    @staticmethod
    def extract_type(attribute):
        """Retrieves the cost type for an attribute, if set by this extension's
        type attribute.

        :param attribute: Attribute element to retrieve cost type for.
        :type attribute: `XAttribute`
        :return: The requested cost type.
        :rtype: str
        """
        attr = attribute.get_attributes().get("cost:type")
        if attr:
            return attr.get_value()
        return None

    @staticmethod
    def extract_types(element):
        """Retrieves a map containing all cost types for all child attributes
        of a trace or event.

        :param element: Trace or Event to retrieve all cost types for.
        :type element: `XTrace` or `XEvent`
        :return: Dictionary with all child keys to cost types.
        :rtype: dict(str: str)
        """
        return XCostType().extract_values(element)

    @staticmethod
    def extract_nested_types(element):
        """Retrieves a map containing all cost types for all descending
        attributes of a trace or event.

        :param element: Trace or Event to retrieve all cost types for.
        :type element: `XTrace` or `XEvent`
        :return: Dictionary with all descending keys to cost types.
        :rtype: dict(list[str]: str)
        """
        return XCostType().extract_nested_values(element)

    def assign_type(self, attribute, type_):
        """Assigns any attribute its cost type, as defined by this extension's
        type attribute.

        :param attribute: Attribute to assign cost type to.
        :type attribute: `XAttribute`
        :param type_: The cost type to be assigned.
        :type type_: str
        """
        if type_ is not None and len(type_.strip()) > 0:
            attr = self.ATTR_TYPE.clone()
            attr.set_value(type)
            attribute.get_attributes()["cost:type"] = attr

    @staticmethod
    def assign_types(element, types):
        """Assigns (to the given event or trace) multiple cost types given their
        keys. Note that as a side effect this method creates attributes when it
        does not find an attribute with the proper key.

        :param element: Event or Trace to assign the cost types to.
        :type element: `XTrace` or `XEvent`
        :param types: Dictionary with keys to cost types which are to be assigned.
        :type types: dict(list[str]: str)
        """
        XCostType().assign_nested_values(element, types)

    @staticmethod
    def assign_nested_types(element, types):
        """Assigns (to the given trace or event) multiple cost types given
        their key lists. The i-th element in the key list should correspond to
        an i-level attribute with the prescribed key. Note that as a side
        effect this method creates attributes when it does not find an attribute
        with the proper key.

        :param element: Event or Trace to assign the cost types to.
        :type element: `XTrace` or `XEvent`
        :param types: Dictionary with keys to cost types which are to be assigned.
        :type types: dict(list[str]: str)
        """
        XCostType().assign_nested_values(element, types)

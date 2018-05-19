from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.model.XAttributable import XAttributable
from opyenxes.id.XIDFactory import XIDFactory
from opyenxes.utils.SingletonClassGenerator import XIdentityExtensionMetaclass


class XIdentityExtension(XExtension, metaclass=XIdentityExtensionMetaclass):
    """Provides unique identifiers (UUIDs) for elements.

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Identity", "identity", urlparse("http://www.xes-standard.org/identity.xesext"))
        factory = XFactoryRegistry().current_default()
        self.ATTR_ID = factory.create_attribute_id("identity:id", XIDFactory.create_id(), self)
        self.get_log_attributes().add(self.ATTR_ID.clone())
        self.get_trace_attributes().add(self.ATTR_ID.clone())
        self.get_event_attributes().add(self.ATTR_ID.clone())
        self.get_meta_attributes().add(self.ATTR_ID.clone())
        XGlobalAttributeNameMap().register_mapping("EN", "identity:id", "Identity")
        XGlobalAttributeNameMap().register_mapping("DE", "identity:id", "Identität")
        XGlobalAttributeNameMap().register_mapping("FR", "identity:id", "Identité")
        XGlobalAttributeNameMap().register_mapping("ES", "identity:id", "Identidad")
        XGlobalAttributeNameMap().register_mapping("PT", "identity:id", "Identidade")

    @staticmethod
    def extract_name(element):
        """Retrieves the name of a log data hierarchy element, if set by this
        extension's name attribute.

        :param element: Log hierarchy element to extract name from.
        :type element: `XAttributable`
        :return: The requested element name.
        :rtype: str
        """
        attribute = element.get_attributes().get("identity:id")
        if attribute:
            return attribute.get_value()
        return None

    @staticmethod
    def extract_id(element):
        """Retrieves the id of a log data hierarchy element, if set by this
        extension's id attribute.

        :param element: Log hierarchy element to assign name from.
        :type element: `XAttributable`
        :return: The requested element id.
        :rtype: XID
        """
        attribute = element.get_attributes().get("identity:id")
        if attribute is not None:
            return attribute.get_value()
        return None

    def assign_id(self, element, identity):
        """Assigns any log data hierarchy element its id, as defined by this
        extension's id attribute.

        :param element: Log hierarchy element to assign id to.
        :type element: `XAttributable`
        :param identity: The id to be assigned.
        :type identity: XID
        """
        if identity is not None:
            attr = self.ATTR_ID.clone()
            attr.set_value(identity)
            element.get_attributes()["identity:id"] = attr

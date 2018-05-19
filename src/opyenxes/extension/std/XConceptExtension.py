from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.utils.SingletonClassGenerator import XConceptExtensionMetaclass


class XConceptExtension(XExtension, metaclass=XConceptExtensionMetaclass):
    """This extension provides naming for concepts in the event log type
    hierarchy. It defines two attributes:
        * concept:name: Name (of any type hierarchy element)
        * concept:instance: Instance identifier (of events)

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Concept", "concept", urlparse("http://www.xes-standard.org/concept.xesext"))
        factory = XFactoryRegistry().current_default()
        self.ATTR_NAME = factory.create_attribute_literal("concept:name", "UNKNOWN", self)
        self.ATTR_INSTANCE = factory.create_attribute_literal("concept:instance", "UNKNOWN", self)
        self.get_log_attributes().add(self.ATTR_NAME.clone())
        self.get_trace_attributes().add(self.ATTR_NAME.clone())
        self.get_event_attributes().add(self.ATTR_NAME.clone())
        self.get_event_attributes().add(self.ATTR_INSTANCE.clone())
        XGlobalAttributeNameMap().register_mapping("EN", "concept:name", "Name")
        XGlobalAttributeNameMap().register_mapping("EN", "concept:instance", "Instance")
        XGlobalAttributeNameMap().register_mapping("DE", "concept:name", "Name")
        XGlobalAttributeNameMap().register_mapping("DE", "concept:instance", "Instanz")
        XGlobalAttributeNameMap().register_mapping("FR", "concept:name", "Appellation")
        XGlobalAttributeNameMap().register_mapping("FR", "concept:instance", "Entité")
        XGlobalAttributeNameMap().register_mapping("ES", "concept:name", "Nombre")
        XGlobalAttributeNameMap().register_mapping("ES", "concept:instance", "Instancia")
        XGlobalAttributeNameMap().register_mapping("PT", "concept:name", "Nome")
        XGlobalAttributeNameMap().register_mapping("PT", "concept:instance", "Instância")

    @staticmethod
    def extract_name(element):
        """Retrieves the name of a log data hierarchy element, if set by this
        extension's name attribute.

        :param element: Log hierarchy element to extract name from.
        :type element: `XAttributable`
        :return: The requested element name.
        :rtype: str
        """
        attribute = element.get_attributes().get("concept:name")
        if attribute:
            return attribute.get_value()
        return None

    def assign_name(self, element, name):
        """Assigns any log data hierarchy element its name, as defined by this
        extension's name attribute.

        :param element: Log hierarchy element to assign name to.
        :type element: `XAttributable`
        :param name: The name to be assigned.
        :type name: str
        """
        if name is not None and len(name.strip()) > 0:
            attr = self.ATTR_NAME.clone()
            attr.set_value(name)
            element.get_attributes()["concept:name"] = attr

    @staticmethod
    def extract_instance(event):
        """Retrieves the activity instance identifier of an event, if set by
        this extension's instance attribute.

        :param event: Event to extract instance from.
        :type event: `XEvent`
        :return: The requested activity instance identifier.
        :rtype: str
        """
        attribute = event.get_attributes().get("concept:instance")
        if attribute:
            return attribute.get_value()
        return None

    def assign_instance(self, event, instance):
        """Assigns any event its activity instance identifier, as defined by
        this extension's instance attribute.

        :param event: Event to assign activity instance identifier to.
        :type event: `XEvent`
        :param instance: The activity instance identifier to be assigned.
        :type instance: str
        """
        if instance is not None and len(instance.strip()) > 0:
            attr = self.ATTR_INSTANCE.clone()
            attr.set_value(instance)
            event.get_attributes()["concept:name"] = attr

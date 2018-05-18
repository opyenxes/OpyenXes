from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.utils.SingletonClassGenerator import XOrganizationalExtensionMetaclass


class XOrganizationalExtension(XExtension, metaclass=XOrganizationalExtensionMetaclass):
    """This extension adds the organizational perspective to event logs. It
    defines for events three attributes, referring to:

        * The resource which has executed the event
        * The role of this resource
        * The group of this resource

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Organizational", "org", urlparse("http://www.xes-standard.org/org.xesext"))
        factory = XFactoryRegistry().current_default()

        self.ATTR_RESOURCE = factory.create_attribute_literal("org:resource", "UNKNOWN", self)
        self.ATTR_ROLE = factory.create_attribute_literal("org:role", "UNKNOWN", self)
        self.ATTR_GROUP = factory.create_attribute_literal("org:group", "UNKNOWN", self)

        self.get_event_attributes().add(self.ATTR_RESOURCE.clone())
        self.get_event_attributes().add(self.ATTR_ROLE.clone())
        self.get_event_attributes().add(self.ATTR_GROUP.clone())
        XGlobalAttributeNameMap().register_mapping("EN", "org:resource", "Resource")
        XGlobalAttributeNameMap().register_mapping("EN", "org:role", "Role")
        XGlobalAttributeNameMap().register_mapping("EN", "org:group", "Group")
        XGlobalAttributeNameMap().register_mapping("DE", "org:resource", "Akteur")
        XGlobalAttributeNameMap().register_mapping("DE", "org:role", "Rolle")
        XGlobalAttributeNameMap().register_mapping("DE", "org:group", "Gruppe")
        XGlobalAttributeNameMap().register_mapping("FR", "org:resource", "Agent")
        XGlobalAttributeNameMap().register_mapping("FR", "org:role", "Rôle")
        XGlobalAttributeNameMap().register_mapping("FR", "org:group", "Groupe")
        XGlobalAttributeNameMap().register_mapping("ES", "org:resource", "Recurso")
        XGlobalAttributeNameMap().register_mapping("ES", "org:role", "Papel")
        XGlobalAttributeNameMap().register_mapping("ES", "org:group", "Grupo")
        XGlobalAttributeNameMap().register_mapping("PT", "org:resource", "Recurso")
        XGlobalAttributeNameMap().register_mapping("PT", "org:role", "Papel")
        XGlobalAttributeNameMap().register_mapping("PT", "org:group", "Grupo")

    @staticmethod
    def extract_resource(event):
        """Extracts the resource attribute string from an event.

        :param event: Event to extract instance from.
        :type event: `XEvent`
        :return: Resource string for the given event (may be None if not defined)
        :rtype: str
        """
        attribute = event.get_attributes().get("org:resource")
        if attribute:
            return attribute.get_value()
        return None

    def assign_resource(self, event, instance):
        """Assigns the resource attribute value for a given event.

        :param event: Event to be modified.
        :type event: `XEvent`
        :param instance: Resource string to be assigned.
        :type instance: str
        """
        if instance is not None and len(instance.strip()) > 0:
            attr = self.ATTR_RESOURCE.clone()
            attr.set_value(instance)
            event.get_attributes()["org:resource"] = attr

    @staticmethod
    def extract_role(event):
        """Extracts the role attribute string from an event.

        :param event: Event to extract instance from.
        :type event: `XEvent`
        :return: Role string for the given event (may be None if not defined)
        :rtype: str
        """
        attribute = event.get_attributes().get("org:role")
        if attribute:
            return attribute.get_value()
        return None

    def assign_role(self, event, instance):
        """Assigns the role attribute value for a given event.

        :param event: Event to be modified.
        :type event: `XEvent`
        :param instance: Role string to be assigned.
        :type instance: str
        """
        if instance is not None and len(instance.strip()) > 0:
            attr = self.ATTR_ROLE.clone()
            attr.set_value(instance)
            event.get_attributes()["org:role"] = attr

    @staticmethod
    def extract_group(event):
        """Extracts the group attribute string from an event.

        :param event: Event to extract instance from.
        :type event: `XEvent`
        :return: The requested activity instance identifier.
        :rtype: str
        """
        attribute = event.get_attributes().get("org:group")
        if attribute:
            return attribute.get_value()
        return None

    def assign_group(self, event, instance):
        """Assigns the group attribute value for a given event.

        :param event: Event to be modified.
        :type event: `XEvent`
        :param instance: Group string to be assigned.
        :type instance: str
        """
        if instance is not None and len(instance.strip()) > 0:
            attr = self.ATTR_GROUP.clone()
            attr.set_value(instance)
            event.get_attributes()["org:group"] = attr

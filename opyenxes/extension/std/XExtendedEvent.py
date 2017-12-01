from opyenxes.extension.std.XConceptExtension import XConceptExtension
from opyenxes.extension.std.XTimeExtension import XTimeExtension
from opyenxes.extension.std.XOrganizationalExtension import XOrganizationalExtension
from opyenxes.extension.std.XLifecycleExtension import XLifecycleExtension
from opyenxes.extension.std.XSemanticExtension import XSemanticExtension
from opyenxes.id.XIDFactory import XIDFactory


class XExtendedEvent:
    """Helper class. This class can be used to dynamically wrap any event, and
    provides an extended set of getter and setter methods for
    typically-available extension attributes.

    :param event: The original event to be wrapped.
    :type event: `XEvent`
    """

    @staticmethod
    def wrap(event):
        """Static wrapper method. Wraps the given event into an instance of
        this class, which transparently provides extended access to attributes.

        :param event: The original event to be wrapped.
        :type event: `XEvent`
        :return: A wrapped event.
        :rtype: `XExtendedEvent`
        """
        return XExtendedEvent(event)

    def __init__(self, event):
        self.__original = event
        self.__id = XIDFactory.create_id()

    def get_name(self):
        """Retrieves the activity name of this event, as defined by the Concept
        extension.

        :return: Activity name of the event.
        :rtype: str
        """
        return XConceptExtension().extract_name(self.__original)

    def set_name(self, name):
        """Sets the activity name of this event, as defined by the Concept
        extension.

        :param name: Activity instance of the event.
        :type name: str
        """
        XConceptExtension().assign_name(self.__original, name)

    def get_instance(self):
        """Retrieves the activity instance of this event, as defined by the
        Concept extension.

        :return: Activity instance of the event.
        :rtype: str
        """
        return XConceptExtension().extract_instance(self.__original)

    def set_instance(self, instance):
        """Sets the activity instance of this event, as defined by the Concept
        extension.

        :param instance: Activity instance of the event.
        :type instance: str
        """
        XConceptExtension().assign_instance(self.__original, instance)

    def get_time_stamp(self):
        """Retrieves the timestamp of the event, as defined by the Time
        extension.

        :return: Timestamp as Date object, or null if not defined.
        :rtype: datetime.datetime
        """
        return XTimeExtension().extract_timestamp(self.__original)

    def set_time_stamp(self, time_stamp):
        """Sets the timestamp of the event, as defined by the Time extension.

        :param time_stamp: Timestamp, as Date or as long value in milliseconds,
        to be set.
        :type time_stamp: datetime.datetime or int
        """
        XTimeExtension().assign_timestamp(self.__original, time_stamp)

    def get_resourse(self):
        """Returns the resource of the event, as defined by the Organizational
        extension.

        :return: Resource string. Can be null, if not defined.
        :rtype: str
        """
        return XOrganizationalExtension().extract_resource(self.__original)

    def set_resource(self, resource):
        """ Sets the resource of the event, as defined by the Organizational
        extension.

        :param resource: Resource string.
        :type resource: str
        """
        XOrganizationalExtension().assign_resource(self.__original, resource.lower())

    def get_role(self):
        """Returns the role of the event, as defined by the Organizational
        extension.

        :return: Role string. Can be null, if not defined.
        :rtype: str
        """
        return XOrganizationalExtension().extract_role(self.__original)

    def set_role(self, role):
        """Sets the role of the event, as defined by the Organizational
        extension.

        :param role: Role string.
        :type role: str
        """
        XOrganizationalExtension().assign_role(self.__original, role.lower())

    def get_group(self):
        """Returns the group of the event, as defined by the Organizational
        extension.

        :return: Group string. Can be null, if not defined.
        :rtype: str
        """
        return XOrganizationalExtension().extract_group(self.__original)

    def set_group(self, group):
        """Sets the group of the event, as defined by the Organizational
        extension.

        :param group: Group string.
        :type group: str
        """
        XOrganizationalExtension().assign_group(self.__original, group.lower())

    def get_transition(self):
        """Returns the lifecycle transition of the event, as defined by the
        Lifecycle extension.

        :return: Lifecycle transition string. Can be null, if not defined.
        :rtype: str
        """
        return XLifecycleExtension().extract_transition(self.__original)

    def set_transition(self, transition):
        """Sets the lifecycle transition of the event, as defined by the
        Lifecycle extension.

        :param transition: Lifecycle transition string.
        :type transition: str
        """
        XLifecycleExtension().assign_transition(self.__original, transition)

    def get_standard_transition(self):
        """Returns the standard lifecycle transition of the event, as defined
        by the Lifecycle extension.

        :return: Standard lifecycle transition as string. Can be null, if not
         defined.
        :rtype: str
        """
        return XLifecycleExtension().extract_standard_transition(self.__original)

    def set_standard_transition(self, transition):
        """Sets the standard lifecycle transition of the event, as defined by
        the Lifecycle extension.

        :param transition: Standard lifecycle transition object as string.
        :type transition: str
        """
        XLifecycleExtension().assign_standard_transition(self.__original, transition)

    def get_model_references(self):
        """Returns the list of model references defined for this event, as
        defined in the Semantic extension.

        :return: List of model reference strings.
        :rtype: list[str]
        """
        return XSemanticExtension().extract_model_references(self.__original)

    def set_model_references(self, model_references):
        """Sets the list of model reference strings defined for this event,
        as defined in the Semantic extension.

        :param model_references: List of model reference strings.
        :type model_references: list[str]
        """
        XSemanticExtension().assign_model_references(self.__original, model_references)

    def get_model_references_uris(self):
        """Returns the list of model reference URIs defined for this event,
        as defined in the Semantic extension.

        :return: List of model reference URIs.
        :rtype: list[ParseResult]
        """
        return XSemanticExtension().extract_model_reference_uris(self.__original)

    def set_model_references_uris(self, model_references_uris):
        """Sets the list of model reference URIs defined for this event, as
        defined in the Semantic extension.

        :param model_references_uris: List of model reference URIs.
        :type model_references_uris: list[ParseResult or SplitResult]
        """
        XSemanticExtension().assign_model_reference_uris(self.__original,
                                                         model_references_uris)

    def get_attributes(self):
        """Retrieves the attributes set for this element.

        :return: A map of attributes.
        :rtype: `XAttributeMap`
        """
        return self.__original.get_attributes()

    def get_extensions(self):
        """Retrieves the extensions used by this element, i.e. the extensions
        used by all attributes of this element, and the element itself

        :return: A set of extensions
        :rtype: set(`XExtension`)
        """
        return self.__original.get_extensions()

    def set_attributes(self, attributes):
        """Sets the map of attributes for this element.

        :param attributes: A map of attributes
        :type attributes: `XAttributeMap`
        """
        self.__original.set_attributes(attributes)

    def has_attributes(self):
        """Checks for the existence of attributes

        :return: True if this element has any attributes; False otherwise.
        :rtype: bool
        """
        return self.__original.has_attributes()

    def clone(self):
        """Clones this event, i.e. creates a deep copy, but with a new ID, so
        equals does not hold between this and the clone

        :return: An identical clone.
        :rtype: `XExtendedEvent`
        """
        aux = XExtendedEvent(self.__original.clone())
        aux._XExtendedEvent__id = XIDFactory.create_id()
        return aux

    def get_id(self):
        """Retrieves the id value of this event

        :return: id of this event
        :rtype: XID
        """
        return self.__id

    def __eq__(self, other):
        if isinstance(other, XExtendedEvent):
            return self.__id == other.get_id()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__id)

from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.utils.SingletonClassGenerator import XLifecycleExtensionMetaclass
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry


class XLifecycleExtension(XExtension, metaclass=XLifecycleExtensionMetaclass):
    """Extension defining additional attributes for the event lifecycle.
    Lifecycles define a set of states for activities, with an accompanying set
    of transitions between those states. Any event which is referring to by a
    lifecycle represents a certain transition of an activity within that
    lifecycle.

    Uses the singleton metaclass
    """
    class StandardModel:
        """Class with the standard lifecycle model.

        """
        SCHEDULE = "schedule"
        ASSIGN = "assign"
        WITHDRAW = "withdraw"
        REASSIGN = "reassign"
        START = "start"
        SUSPEND = "suspend"
        RESUME = "resume"
        PI_ABORT = "pi_abort"
        ATE_ABORT = "ate_abort"
        COMPLETE = "complete"
        AUTOSKIP = "autoskip"
        MANUALSKIP = "manualskip"
        UNKNOWN = "unknown"

        def values(self):
            """Returns an array containing the constants of this enum type, in
            the order they are declared. This method may be used to iterate over
            the constants as follows:

            :return: An array containing the constants of this enum type, in the
             order they are declared
            :rtype: list[str]
            """
            return [self.SCHEDULE, self.ASSIGN, self.WITHDRAW, self.REASSIGN,
                    self.START, self.SUSPEND, self.RESUME, self.PI_ABORT,
                    self.ATE_ABORT, self.COMPLETE, self.AUTOSKIP, self.MANUALSKIP,
                    self.UNKNOWN]

        def decode(self, encoding):
            """Decodes any encoding string, referring to the respective
            standard-model lifecycle transition object in this enum.

            :param encoding: Encoding string.
            :type encoding: str
            :return: Standard-model transition string
            :rtype: str
            """
            encoding = encoding.strip().lower()
            for elem in self.values():
                if encoding == elem:
                    return elem
            return self.UNKNOWN

    def __init__(self):
        super().__init__("Lifecycle", "lifecycle", urlparse("http://www.xes-standard.org/lifecycle.xesext"))
        factory = XFactoryRegistry().current_default()
        self.ATTR_MODEL = factory.create_attribute_literal("lifecycle:model", "standart", self)
        self.ATTR_TRANSITION = factory.create_attribute_literal("lifecycle:transition", XLifecycleExtension.StandardModel.COMPLETE, self)
        self.get_log_attributes().add(self.ATTR_MODEL.clone())
        self.get_event_attributes().add(self.ATTR_TRANSITION.clone())
        XGlobalAttributeNameMap().register_mapping("EN", "lifecycle:model", "Lifecycle Model")
        XGlobalAttributeNameMap().register_mapping("EN", "lifecycle:transition", "Lifecycle Transition")
        XGlobalAttributeNameMap().register_mapping("DE", "lifecycle:model", "Lebenszyklus-Model")
        XGlobalAttributeNameMap().register_mapping("DE", "lifecycle:transition", "Lebenszyklus-Transition")
        XGlobalAttributeNameMap().register_mapping("FR", "lifecycle:model", "Modèle du Cycle Vital")
        XGlobalAttributeNameMap().register_mapping("FR", "lifecycle:transition", "Transition en Cycle Vital")
        XGlobalAttributeNameMap().register_mapping("ES", "lifecycle:model", "Modelo de Ciclo de Vida")
        XGlobalAttributeNameMap().register_mapping("ES", "lifecycle:transition", "Transición en Ciclo de Vida")
        XGlobalAttributeNameMap().register_mapping("PT", "lifecycle:model", "Modelo do Ciclo de Vida")
        XGlobalAttributeNameMap().register_mapping("PT", "lifecycle:transition", "Transição do Ciclo de Vida")

    @staticmethod
    def extract_model(log):
        """Extracts the lifecycle model identifier from a given log.

        :param log: Event log.
        :type log: `XLog`
        :return: Lifecycle model identifier string.
        :rtype: str
        """
        attribute = log.get_attributes().get("lifecycle:model")
        if attribute:
            return attribute.get_value()
        return None

    def assign_model(self, log, model):
        """Assigns a value for the lifecycle model identifier to a given log.

        :param log: Log to be tagged.
        :type log: `XLog`
        :param model: Lifecycle model identifier string to be used.
        :type model: str
        """
        if model is not None and len(model.strip()) > 0:
            attr = self.ATTR_MODEL.clone()
            attr.set_value(model.strip())
            log.get_attributes()["lifecycle:model"] = attr

    def uses_standard_model(self, log):
        """Checks, whether a given log uses the standard model for lifecycle
        transitions.

        :param log: Log to be checked.
        :type log: `XLog`
        :return: Returns true, if the log indeed uses the standard lifecycle model.
        :rtype: bool
        """
        model = self.extract_model(log)
        if model is None:
            return False
        return model.strip() == "standard"

    @staticmethod
    def extract_transition(event):
        """Extracts the lifecycle transition string from a given event.

        :param event: The given event
        :type event: `XEvent`
        :return: The lifecycle transition string of this event. Can be null, if
         not defined.
        :rtype: str
        """
        attribute = event.get_attributes().get("lifecycle:transition")
        if attribute is not None:
            return attribute.get_value()
        return None

    def extract_standard_transition(self, event):
        """Extracts the standard lifecycle transition object from a given event.

        :param event: The given event
        :type event: `XEvent`
        :return: The standard lifecycle transition instance of this event. Can
         be null, if not defined.
        :rtype: str
        """
        transition = self.extract_transition(event)
        if transition is not None:
            return XLifecycleExtension.StandardModel().decode(transition)
        return None

    def assign_transition(self, event, transition):
        """Assigns a lifecycle transition string to the given event.

        :param event: Event to be tagged.
        :type event: `XEvent`
        :param transition: Lifecycle transition string to be assigned.
        :type transition: str
        """
        if transition is not None and len(transition.strip()) > 0:
            trans_attr = self.ATTR_TRANSITION.clone()
            trans_attr.set_value = transition.strip()
            event.get_attributes()["lifecycle:transition"] = trans_attr

    def assign_standard_transition(self, event, transition):
        """Assigns a standard lifecycle transition to the given event..

        :param event: Event to be tagged.
        :type event: `XEvent`
        :param transition: Standard lifecycle transition to be assigned.
        :type transition: str
        """
        self.assign_transition(event, XLifecycleExtension.StandardModel().decode(transition))

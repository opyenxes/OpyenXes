from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.classification.XEventLifeTransClassifier import XEventLifeTransClassifier
from opyenxes.classification.XEventResourceClassifier import XEventResourceClassifier
from opyenxes.classification.XEventNameClassifier import XEventNameClassifier
from opyenxes.classification.XEventClasses import XEventClasses
from opyenxes.info.XAttributeInfo import XAttributeInfo
from opyenxes.info.XTimeBounds import XTimeBounds


class XLogInfo:
    """This class implements a bare-bones log info summary which can be created
    on demand by using applications. The log info summary is based on an event
    classifier, which is used to identify event class abstractions.

    :param log: The event log to create an info summary for.
    :type log: `XLog`
    :param default_classifier: The default event classifier to be used
    :type default_classifier: `XEventAttributeClassifier`
    :param classifiers: A collection of additional event classifiers to be
     covered by the created log info instance.
    :type classifiers: list[`XEventAttributeClassifier`]
    """
    STANDARD_CLASSIFIER = XEventAttributeClassifier("MXML Legacy Classifier", ["concept:name", "lifecycle:transition"])
    NAME_CLASSIFIER = XEventNameClassifier()
    RESOURCE_CLASSIFIER = XEventResourceClassifier()
    LIFECYCLE_TRANSITION_CLASSIFIER = XEventLifeTransClassifier()

    @staticmethod
    def create(log, default_classifier=None, classifiers=None):
        """Creates a new log info summary with the standard event classifier.

        :param log: The event log to create an info summary for.
        :type log: `XLog`
        :param default_classifier: The default event classifier to be used
        :type default_classifier: `XEventAttributeClassifier`
        :param classifiers: A collection of additional event classifiers to be
         covered by the created log info instance.
        :type classifiers: list[`XEventAttributeClassifier`]
        :return: The log info summary for this log.
        :rtype: `XLogInfo`
        """
        if default_classifier is None:
            return XLogInfo(log, XLogInfo.STANDARD_CLASSIFIER, classifiers)
        return XLogInfo(log, default_classifier, classifiers)

    def __init__(self, log, default_classifier, classifiers):
        self.__log = log
        self.__default_classifier = default_classifier
        if classifiers is None:
            classifiers = list()
        self.__event_classes = dict()
        for classifier in classifiers:
            self.__event_classes[classifier] = XEventClasses(classifier)

        self.__event_classes[self.__default_classifier] = XEventClasses(self.__default_classifier)
        self.__event_classes[self.NAME_CLASSIFIER] = XEventClasses(self.NAME_CLASSIFIER)
        self.__event_classes[self.RESOURCE_CLASSIFIER] = XEventClasses(self.RESOURCE_CLASSIFIER)
        self.__event_classes[self.LIFECYCLE_TRANSITION_CLASSIFIER] = XEventClasses(self.LIFECYCLE_TRANSITION_CLASSIFIER)

        self.__number_of_events = 0
        self.__number_of_traces = 0
        self.__log_boundaries = XTimeBounds()
        self.__trace_boundaries = dict()
        self.__log_attribute_info = XAttributeInfo()
        self.__trace_attribute_info = XAttributeInfo()
        self.__event_attribute_info = XAttributeInfo()
        self.__meta_attribute_info = XAttributeInfo()
        self.setup()

    def setup(self):
        """Creates the internal data structures of this summary on setup from
        the log.

        """
        self.register_attributes(self.__log_attribute_info, self.__log)

        for trace in self.__log:
            self.__number_of_traces += 1
            self.register_attributes(self.__trace_attribute_info, trace)
            trace_bounds = XTimeBounds()

            for event in trace:
                self.__number_of_events += 1
                self.register_attributes(self.__event_attribute_info, event)

                for classes in self.__event_classes.values():
                    classes.register(event)

                trace_bounds.register(event)

            self.__trace_boundaries[trace] = trace_bounds
            self.__log_boundaries.register(trace_bounds)

        for classes in self.__event_classes.values():
            classes.harmonize_indices()

    def register_attributes(self, attribute_info, attributable):
        """Registers all attributes of a given attributable, i.e. model type
        hierarchy element, in the given attribute info registry.

        :param attribute_info: Attribute info registry to use for registration.
        :type attribute_info: `XAttributeInfo`
        :param attributable: Attributable whose attributes to register.
        :type attributable: `XAttributable`
        """
        if attributable.has_attributes():
            for attribute in attributable.get_attributes().values():
                attribute_info.register(attribute)
                self.register_attributes(self.__meta_attribute_info, attribute)

    def get_log(self):
        """Retrieves the log used for this summary.

        :return: The event log which this summary describes.
        :rtype: `XLog`
        """
        return self.__log

    def get_number_of_event(self):
        """Retrieves the total number of events in this log.

        :return: Total number of events.
        :rtype: int
        """
        return self.__number_of_events

    def get_number_of_traces(self):
        """Retrieves the number of traces in this log.

        :return: Number of traces available in this log.
        :rtype: int
        """
        return self.__number_of_traces

    def get_event_classes(self, classifier=None):
        """Retrieves the event classes for a given classifier.
        *Note:* The given event classifier must be covered by this log info,
        i.e., the log info must have been created with this classifier.
        Otherwise, this method will return null. You can retrieve the collection
        of event classifiers covered by this log info instance by calling the
        method getEventClassifiers().

        :param classifier: The classifier for which to retrieve the event classes.
        :type classifier: `XEventAttributeClassifier` or None
        :return: The requested event classes, or null if the given event
         classifier is not covered by this log info instance.
        :rtype: `XEventClasses`
        """
        if classifier is None:
            return self.__event_classes.get(self.__default_classifier)
        return self.__event_classes.get(classifier)

    def get_event_classifiers(self):
        """Retrieves the set of event classifiers covered by this log info,
        i.e., for which event classes are registered in this log info instance.

        :return: The tuple of event classifiers covered by this log info instance.
        :rtype: tuple
        """
        return set(self.__event_classes.keys())

    def get_resource_classes(self):
        """Retrieves the resource classes of the summarized log.

        :return: The resource classes of the summarized log.
        :rtype: `XEventClasses`
        """
        return self.__event_classes.get(self.RESOURCE_CLASSIFIER)

    def get_name_classes(self):
        """Retrieves the event name classes of the summarized log.

        :return: The event name classes of the summarized log.
        :rtype: `XEventClasses`
        """
        return self.__event_classes.get(self.NAME_CLASSIFIER)

    def get_transition_classes(self):
        """Retrieves the lifecycle transition classes of the summarized log.

        :return: The lifecycle transition classes of the summarized log.
        :rtype: `XEventClasses`
        """
        return self.__event_classes.get(self.LIFECYCLE_TRANSITION_CLASSIFIER)

    def get_log_time_boundaries(self):
        """Retrieves the global timestamp boundaries of this log.

        :return: Timestamp boundaries for the complete log.
        :rtype `XTimeBounds`
        """
        return self.__log_boundaries

    def get_trace_time_boundaries(self, trace):
        """ Retrieves the timestamp boundaries for a specified trace.

        :param trace: Trace to be queried for.
        :return: Timestamp boundaries for the indicated trace.
        :rtype: `XTimeBounds`
        """
        return self.__trace_boundaries.get(trace)

    def get_log_attribute_info(self):
        """Retrieves attribute information about all attributes this log
        contains on the log level.

        :return: Attribute information on the log level.
        :rtype: `XAttributeInfo`
        """
        return self.__log_attribute_info

    def get_trace_attribute_info(self):
        """Retrieves attribute information about all attributes this log
        contains on the trace level.

        :return: Attribute information on the trace level.
        :rtype: `XAttributeInfo`
        """
        return self.__trace_attribute_info

    def get_event_attribute_info(self):
        """Retrieves attribute information about all attributes this log
        contains on the event level.

        :return: Attribute information on the event level.
        :rtype: `XAttributeInfo`
        """
        return self.__event_attribute_info

    def get_meta_attribute_info(self):
        """Retrieves attribute information about all attributes this log
        contains on the meta (i.e., attribute) level.

        :return: Attribute information on the meta level.
        :rtype: `XAttributeInfo`
        """
        return self.__meta_attribute_info


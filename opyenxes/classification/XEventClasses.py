from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.classification.XEventClass import XEventClass
from opyenxes.model.XElement import XElement
from opyenxes.model.XEvent import XEvent


class XEventClasses:
    """A set of event classes. For any log, this class can be used to impose a
    classification of events. Two events which belong to the same event class
    can be considered equal, i.e. to refer to the same higher-level concept
    they represent (e.g., an activity). Event classes are imposed on a log by
    a specific classifier. This class can be configured with such a classifier,
    which is then used to derive the actual event classes from a log, by
    determining the identity of the contained events.

    :param classifier: The classifier used for creating the set of event classes.
    :type classifier: `XEventAttributeClassifier`
    """
    def __init__(self, classifier):
        self.__classifier = classifier
        self.__class_map = {}

    @staticmethod
    def derive_event_classes(classifier, log):
        """Creates a new set of event classes, factory method.

        :param classifier: The classifier to be used for event comparison.
        :type classifier: `XEventAttributeClassifier`
        :param log: The log, on which event classes should be imposed.
        :type log: `XLog`
        :return: A set of event classes, as an instance of this class.
        :rtype: `XEventClasses`
        """
        n_classes = XEventClasses(classifier)
        n_classes.register(log)
        n_classes.harmonize_indices()
        return n_classes

    def get_classifier(self):
        """ Returns the classifier used for determining event classes.

        :return: A classifier used in this set of classes.
        :rtype: dict
        """
        return self.__classifier

    def get_classes(self):
        """Returns the collection of event classes contained in this instance.


        :return: A collection of event classes.
        :rtype: dict_values
        """
        return self.__class_map.values()

    def get_class_of(self, event):
        """For any given event, returns the corresponding event class as
        determined by this set.

        :param event: The event of which the event class should be determined.
        :type event: `XEvent`
        :return: The event class of this event, as found in this set of event
         classes. If no matching event class is found, this method may return
          null.
        :rtype: `XEventClass`
        """
        return self.__class_map.get(self.__classifier.get_class_identity(event))

    def get_by_identity(self, identity):
        """Returns a given event class by its identity, i.e. its unique
        identifier string.

        :param identity: Identifier string of the requested event class.
        :type identity: str
        :return: The requested event class. If no matching event class is found,
         this method may return null.
        :rtype: `XEventClass`
        """
        return self.__class_map.get(identity)

    def get_by_index(self, index):
        """Returns a given event class by its unique index.

        :param index: Unique index of the requested event class.
        :type index: int
        :return: The requested event class. If no matching event class is found,
         this method may return null.
        :rtype: `XEventClass`
        """
        for event_class in self.__class_map.values():
            if event_class.get_index() == index:
                return event_class
        return None

    def register(self, element):
        """Registers a XES Element(log, trace and event and class ID) with this
        set of event classes. This will result in all events of this log being
        analyzed, and potentially new event classes being added to this set of
        event classes. Event classes will be incremented in size, as new
        members of these classes are found among the events in the log.

        :param element: The Xes Element or Class ID to be analyzed.
        :type element: `XLog` or `XTrace` or `XEvent` or str
        """
        if isinstance(element, XElement) and not isinstance(element, XEvent):
            for objects in element:
                self.register(objects)
        elif isinstance(element, XEvent):
            self.register(self.__classifier.get_class_identity(element))
        elif isinstance(element, str):
            event_class = self.__class_map.get(element)
            if event_class is None and element is not None:
                event_class = XEventClass(element, len(self.__class_map))
                self.__class_map[element] = event_class

            if event_class:
                event_class.increment_size()

        else:
            raise TypeError("The argument must be a XElement or string")

    def harmonize_indices(self):
        """This method harmonizeds the indices of all contained event classes.
        Indices are re-assigned according to the natural order of class
        identities, i.e., the alphabetical order of class identity strings.
        This method should be called after the composition or derivation of
        event classes is complete, e.g., after scanning a log for generating
        the log info. Using parties should not have to worry about event class
        harmonization, and can thus safely ignore this method.
        """
        array_list = sorted(self.__class_map.values())
        self.__class_map = {}
        for i in range(len(array_list)):
            original = array_list[i]
            harmonized = XEventClass(original.get_id(), i)
            harmonized.set_size(original.size())
            self.__class_map[harmonized.get_id()] = harmonized

    def __eq__(self, other):
        if isinstance(other, XEventClasses):
            return self.__classifier == other.get_classifier()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Event classes defined by " + self.__classifier.name()

    def __len__(self):
        return len(self.__class_map)

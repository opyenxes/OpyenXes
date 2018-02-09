from opyenxes.model.XElement import XElement


class XLog(XElement, list):
    """
    A log is an element of an XES event log structure. Logs are contained in
    archives. Any log is a list of traces. Logs represent a collection of
    traces, which are all representing executions of the same kind of process.

    :param attributes: Map of attribute for the log.
    :type attributes: `XAttributeMap`
    """
    def __init__(self, attributes):
        super().__init__(attribute=attributes)
        self.__classifiers = []
        self.__globalTraceAttributes = []
        self.__globalEventAttributes = []
        self.__cachedClassifier = None
        self.__cachedInfo = None
        self.__features = {}
        self.__extension = set()

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XLog`
        """
        clone = XLog(self.get_attributes().clone())
        for elem in self.__extension:
            clone.get_extensions().add(elem)

        clone.__classifiers = self.__classifiers.copy()
        clone.__globalTraceAttributes = self.__globalTraceAttributes.copy()
        clone.__globalEventAttributes = self.__globalEventAttributes.copy()
        clone.__features = self.__features.copy()

        for trace in self:
            clone.append(trace.clone())

        return clone

    def get_extensions(self):
        """Retrieves the extensions used by this element, i.e. the extensions
        used by all attributes of this element, and the element itself

        :return: A set of extensions
        :rtype: set(`XExtension`)
        """
        return self.__extension

    def get_classifiers(self):
        """
        This method returns the list of classifiers defined for this log. This
        list can be used for reading or writing, i.e., it must be supported to
        add further classifiers to this list.

        :return: The list of classifiers defined for this log.
        :rtype: list[`XEventAttributeClassifier`]
        """
        return self.__classifiers

    def get_global_event_attributes(self):
        """
        This method returns a list of attributes which are global for all
        events, i.e. every event in the log is guaranteed to have these
        attributes.

        :return: List of ubiquitous trace attributes.
        :rtype: List[`XAttribute`]
        """
        return self.__globalEventAttributes

    def get_global_trace_attributes(self):
        """
        This method returns a list of attributes which are global for all
        traces, i.e. every trace in the log is guaranteed to have these
        attributes.

        :return: List of ubiquitous trace attributes.
        :rtype: List[`XAttribute`]
        """
        return self.__globalTraceAttributes

    def set_features(self, key, values):
        """Assigns the key with the value in de features dictionary.

        :param key: key of the feature.
        :type key: str
        :param values: data of that features
        :type values: Any
        """
        self.__features[key] = values

    def get_features(self):
        """Retrieves the features of the log for example version, encoding,
         if have nested-attributes, etc

        :return: Dictionary with features
        :rtype: dict
        """
        return self.__features

    def set_info(self, classifier, info):
        """Adds the given info for the given classifier to the info cache.

        :param classifier: The given classifier.
        :type classifier: `XEventClassifier`
        :param info: The given info.
        :type info: `XLogInfo`
        """
        self.__cachedClassifier = classifier
        self.__cachedInfo = info

    def get_info(self, classifier):
        """Returns the cached info for the given classifier, null if not available.

        :param classifier: The given classifier
        :type classifier: `XEventAttributeClassifier`
        :return: The cached info for the given classifier, null if not available
        :rtype: `XLogInfo` or None
        """
        if classifier == self.__cachedClassifier:
            return self.__cachedInfo
        return None

    def append(self, p_object):
        """
        Add only a trace object in the log.

        :param p_object: a Trace object to append for the log
        :type p_object: `XTrace`
        """
        super(XLog, self).append(p_object)

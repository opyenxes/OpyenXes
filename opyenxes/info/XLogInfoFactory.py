from opyenxes.info.XLogInfo import XLogInfo


class XLogInfoFactory:
    """Factory for deriving log info summaries from logs.

    """
    @staticmethod
    def create_log_info(log, classifier=None):
        """Creates a new log info summary with a custom or standard event
        classifier.

        :param log: The event log to create an info summary for.
        :type log: `XLog`
        :param classifier: The event classifier to be used.
        :type classifier: `XEventAttributeClassifier`
        :return: The log info summary for this log.
        :rtype: `XLogInfo`
        """
        if classifier is None:
            classifier = XLogInfo.STANDARD_CLASSIFIER
        info = log.get_info(classifier)
        if info is None:
            info = XLogInfo.create(log, classifier)
            log.set_info(classifier, info)
        return info

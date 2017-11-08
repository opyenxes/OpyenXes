from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


class XEventNameClassifier(XEventAttributeClassifier):
    """Implements an event classifier based on the activity name of events.

    """
    def __init__(self):
        super().__init__("Event Name", ["concept:name"])

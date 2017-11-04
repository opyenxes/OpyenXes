from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


class XEventResourceClassifier(XEventAttributeClassifier):
    """Implements an event classifier based on the resource name attribute of
    events.

    """
    def __init__(self):
        super().__init__("Resource", ["org:resource"])

from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


__all__ = [ 'XEventLifeTransClassifier' ]


class XEventLifeTransClassifier(XEventAttributeClassifier):
    """Implements an event classifier based on the lifecycle transition
    attribute of events.


    """
    def __init__(self):
        super().__init__("Lifecycle transition", ["lifecycle:transition"])

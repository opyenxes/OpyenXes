from opyenxes.model.XAttributable import XAttributable
from opyenxes.model.XAttributeMap import XAttributeMap


class XElement(XAttributable):
    """This Class is implemented by all elements of an event log structure.
    It defines that all elements are attributable

    :param attribute: A `XAttributeMap` with the attribute for this class.
    :type attribute: `XAttributeMap`
    """
    def __init__(self, attribute=XAttributeMap()):
        super(XElement, self).__init__(attribute)

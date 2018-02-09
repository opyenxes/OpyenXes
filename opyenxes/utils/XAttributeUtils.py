from opyenxes.model.XAttributeDiscrete import XAttributeDiscrete
from opyenxes.model.XAttributeLiteral import XAttributeLiteral
from opyenxes.model.XAttributeContinuous import XAttributeContinuous
from opyenxes.model.XAttributeBoolean import XAttributeBoolean
from opyenxes.model.XAttributeID import XAttributeID
from opyenxes.model.XAttributeList import XAttributeList
from opyenxes.model.XAttributeContainer import XAttributeContainer
from opyenxes.model.XAttributeTimestamp import XAttributeTimestamp
from opyenxes.id.XIDFactory import XIDFactory


class XAttributeUtils:
    """Utilities for working with attributes.

    """
    @staticmethod
    def get_type(attribute):
        """For the given attribute, returns its type, i.e., the most high-level,
        typed interface this attribute implements.

        :param attribute: Attribute to analyze.
        :type attribute: `XAttribute`
        :return: Class of this attribute.
        :rtype: type
        """
        if isinstance(attribute, XAttributeDiscrete):
            return XAttributeDiscrete
        elif isinstance(attribute, XAttributeLiteral):
            return XAttributeLiteral
        elif isinstance(attribute, XAttributeContinuous):
            return XAttributeContinuous
        elif isinstance(attribute, XAttributeBoolean):
            return XAttributeBoolean
        elif isinstance(attribute, XAttributeID):
            return XAttributeID
        elif isinstance(attribute, XAttributeList):
            return XAttributeList
        elif isinstance(attribute, XAttributeContainer):
            return XAttributeContainer
        elif isinstance(attribute, XAttributeTimestamp):
            return XAttributeTimestamp
        else:
            raise TypeError("Unexpected attribute type!")

    @staticmethod
    def get_type_string(attribute):
        """For the given attribute, derives the standardized string describing
        the attributes specific type (used, e.g., for serialization).

        :param attribute: Attribute to extract type string from.
        :type attribute: `XAttribute`
        :return: String representation of the attribute's specific type.
        :rtype: str
        """
        if isinstance(attribute, XAttributeDiscrete):
            return "DISCRETE"
        elif isinstance(attribute, XAttributeLiteral):
            return "LITERAL"
        elif isinstance(attribute, XAttributeContinuous):
            return "CONTINUOUS"
        elif isinstance(attribute, XAttributeBoolean):
            return "BOOLEAN"
        elif isinstance(attribute, XAttributeID):
            return "ID"
        elif isinstance(attribute, XAttributeList):
            return "LIST"
        elif isinstance(attribute, XAttributeContainer):
            return "CONTAINER"
        elif isinstance(attribute, XAttributeTimestamp):
            return "TIMESTAMP"
        else:
            raise TypeError("Unexpected attribute type!")

    @staticmethod
    def derive_prototype(instance):
        """Derives a prototype for the given attribute. This prototype attribute
        will be equal in all respects, expect for the value of the attribute.
        This value will be set to a default value, depending on the specific
        type of the given attribute.

        :param instance: Attribute to derive prototype from.
        :type instance: `XAttribute`
        :return: The derived prototype attribute.
        :rtype: `XAttribute`
        """
        prototype = instance.clone()

        if not isinstance(prototype, XAttributeList) and not isinstance(prototype, XAttributeContainer):
            if isinstance(prototype, XAttributeLiteral):
                prototype.set_value("UNKNOWN")
            elif isinstance(prototype, XAttributeBoolean):
                prototype.set_value(True)
            elif isinstance(prototype, XAttributeContinuous):
                prototype.set_value(0.0)
            elif isinstance(prototype, XAttributeDiscrete):
                prototype.set_value(0)
            elif isinstance(prototype, XAttributeTimestamp):
                prototype.set_value_millies(0)
            elif isinstance(prototype, XAttributeID):
                prototype.set_value(XIDFactory().create_id())
            else:
                raise TypeError("Unexpected attribute type!")

        return prototype

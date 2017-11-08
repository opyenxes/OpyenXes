from opyenxes.id.XID import XID
from opyenxes.utils.SingletonClassGenerator import XIDFactoryMetaclass


class XIDFactory(metaclass=XIDFactoryMetaclass):
    """
    This class is a factory for unique identifiers, as they are used throughout
    the XES model for element identification.

    Uses the singleton metaclass
    """
    @staticmethod
    def create_id():
        """Creates a new, unique ID

        :return: Unique ID
        :rtype: `XID`
        """
        return XID()

from opyenxes.utils.XRegistry import XRegistry
from opyenxes.utils.SingletonClassGenerator import XParserRegistryMetaclass
from opyenxes.data_in.XesXmlParser import XesXmlParser
from opyenxes.data_in.XMxmlParser import XMxmlParser
from opyenxes.data_in.XMxmlGZIPParser import XMxmlGZIPParser
from opyenxes.data_in.XesXmlGZIPParser import XesXmlGZIPParser


class XParserRegistry(XRegistry, metaclass=XParserRegistryMetaclass):
    """System-wide registry for XES parser implementations. Applications can use
    this registry as a convenience to provide an overview about parseable
    formats, e.g., in the user interface. Any custom parser implementation can
    be registered with this registry, so that it transparently becomes available
    also to any other using application.

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__()
        self.register(XMxmlParser())
        self.register(XMxmlGZIPParser())

        self.register(XesXmlParser())
        self.set_current_default(XesXmlGZIPParser())

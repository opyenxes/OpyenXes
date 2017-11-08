from utils.XRegistry import XRegistry
from utils.SingletonClassGenerator import XSerializerRegistryMetaclass
from out.XesXmlGZIPSerializer import XesXmlGZIPSerializer
from out.XesXmlSerializer import XesXmlSerializer
from out.XMxmlSerializer import XMxmlSerializer
from out.XMxmlGZIPSerializer import XMxmlGZIPSerializer


class XSerializerRegistry(XRegistry, metaclass=XSerializerRegistryMetaclass):
    """System-wide registry for XES serializer implementations. Applications can
    use this registry as a convenience to provide an overview about
    serializeable formats, e.g., in the user interface. Any custom serializer
    implementation can be registered with this registry, so that it
    transparently becomes available also to any other using application.

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__()
        self.register(XMxmlSerializer())
        self.register(XMxmlGZIPSerializer())

        self.register(XesXmlSerializer())

        self.set_current_default(XesXmlGZIPSerializer())
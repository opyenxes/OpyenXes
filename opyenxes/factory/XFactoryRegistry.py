from opyenxes.utils.XRegistry import XRegistry
from opyenxes.utils.SingletonClassGenerator import XFactoryRegistryMetaclass
from opyenxes.factory.XFactory import XFactory


class XFactoryRegistry(XRegistry, metaclass=XFactoryRegistryMetaclass):
    """XModelFactoryRegistry is the most important integration point for
    external contributors, aside from the extension infrastructure. This
    singleton class serves as a system-wide registry for XES factory implementations.
    It provides a current, i.e. standard, factory implementation, which can
    be switched by applications. This factory will be used in any internal
    places, e.g., for creating models from reading XES serializations. Other,
    e.g. proprietary or domain-specific, implementations of the XES standard
    (and the OpenXES model hierarchy interface) are suggested to implement the
    XModelFactory interface, and to register their factory with this registry.
    This enables to transparently switch the storage implementation of the
    complete OpenXES system (wherever applicable), and every application making
    use of this registry to create new models.

    """
    def __init__(self):
        super().__init__()
        self.set_current_default(XFactory())

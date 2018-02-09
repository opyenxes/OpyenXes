class XCostAmountMetaclass(type):
    """
    This Metaclass produce a singleton XCostAmount class
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XCostAmountMetaclass.instance:
            XCostAmountMetaclass.instance = super().__call__(*args, **kw)
        return XCostAmountMetaclass.instance


class XCostDriverMetaclass(type):
    """
    This Metaclass produce a singleton XCostDriver class
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XCostDriverMetaclass.instance:
            XCostDriverMetaclass.instance = super().__call__(*args, **kw)
        return XCostDriverMetaclass.instance


class XCostTypeMetaclass(type):
    """
    This Metaclass produce a singleton XCostType class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XCostTypeMetaclass.instance:
            XCostTypeMetaclass.instance = super().__call__(*args, **kw)
        return XCostTypeMetaclass.instance


class XConceptExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XCostExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XConceptExtensionMetaclass.instance:
            XConceptExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XConceptExtensionMetaclass.instance


class XExtensionManagerMetaclass(type):
    """
    This Metaclass produce a singleton XExtensionManager class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XExtensionManagerMetaclass.instance:
            XExtensionManagerMetaclass.instance = super().__call__(*args, **kw)
        return XExtensionManagerMetaclass.instance


class XExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XExtensionMetaclass.instance:
            XExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XExtensionMetaclass.instance


class XLifecycleExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XLifecycleExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XLifecycleExtensionMetaclass.instance:
            XLifecycleExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XLifecycleExtensionMetaclass.instance


class XIdentityExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XIdentityExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XIdentityExtensionMetaclass.instance:
            XIdentityExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XIdentityExtensionMetaclass.instance


class XFactoryRegistryMetaclass(type):
    """
    This Metaclass produce a singleton XFactoryRegistry class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XFactoryRegistryMetaclass.instance:
            XFactoryRegistryMetaclass.instance = super().__call__(*args, **kw)
        return XFactoryRegistryMetaclass.instance


class XIDFactoryMetaclass(type):
    """
    This Metaclass produce a singleton XIDFactory class
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XIDFactoryMetaclass.instance:
            XIDFactoryMetaclass.instance = super().__call__(*args, **kw)
        return XIDFactoryMetaclass.instance


class XGlobalAttributeNameMapMetaclass(type):
    """
    This Metaclass produce a singleton XGlobalAttributeNameMap class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XGlobalAttributeNameMapMetaclass.instance:
            XGlobalAttributeNameMapMetaclass.instance = super().__call__(*args, **kw)
        return XGlobalAttributeNameMapMetaclass.instance


class XMicroExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XMicroExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XMicroExtensionMetaclass.instance:
            XMicroExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XMicroExtensionMetaclass.instance


class XTimeExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XMicroExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XTimeExtensionMetaclass.instance:
            XTimeExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XTimeExtensionMetaclass.instance


class XOrganizationalExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XOrganizationalExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XOrganizationalExtensionMetaclass.instance:
            XOrganizationalExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XOrganizationalExtensionMetaclass.instance


class XSemanticExtensionMetaclass(type):
    """
    This Metaclass produce a singleton XOrganizationalExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XSemanticExtensionMetaclass.instance:
            XSemanticExtensionMetaclass.instance = super().__call__(*args, **kw)
        return XSemanticExtensionMetaclass.instance


class XSerializerRegistryMetaclass(type):
    """
    This Metaclass produce a singleton XOrganizationalExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XSerializerRegistryMetaclass.instance:
            XSerializerRegistryMetaclass.instance = super().__call__(*args, **kw)
        return XSerializerRegistryMetaclass.instance


class XParserRegistryMetaclass(type):
    """
    This Metaclass produce a singleton XOrganizationalExtension class.
    """
    instance = None

    def __call__(cls, *args, **kw):
        if not XParserRegistryMetaclass.instance:
            XParserRegistryMetaclass.instance = super().__call__(*args, **kw)
        return XParserRegistryMetaclass.instance

class XRegistry:
    """Template implementation for a generic registry.

    """
    def __init__(self):
        self.__registry = set()
        self.__current = None

    def get_available(self):
        """Retrieves an unmodifiable set of all available instances.

        :return: Tuple of all available instances.
        :rtype: tuple
        """
        return tuple(self.__registry)

    def current_default(self):
        """Retrieves the current default instance.

        :return: The current default instance.
        :rtype: Any
        """
        return self.__current

    def register(self, instance):
        """Registers a new instance with this registry.

        :param instance: Instance to be registered.
        :type instance: Any.
        """
        if instance not in self:
            self.__registry.add(instance)
            if self.__current is None:
                self.__current = instance

    def set_current_default(self, instance):
        """Sets the current default instance of this registry.

        :param instance: Instance to be the current default of this registry.
        :type instance: Any
        """
        self.__registry.add(instance)
        self.__current = instance

    def __contains__(self, item):
        return item in self.__registry

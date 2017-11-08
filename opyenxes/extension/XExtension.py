class XExtension:
    """This class defines and implements extensions to the basic log meta-model.
    Extensions have a name, a defined prefix, and a unique URI. They can define
    additional, typed attributes on the level of the log, trace, and event.
    Also, extensions may define meta attributes

    :param name: The name of the extension.
    :type name: str
    :param prefix: Prefix string of the extension, used for addressing attributes.
    :type prefix:  str
    :param uri: Unique URI of the extension. This URI should point to the file
      defining the extension, and must be able to be resolved. Extension files
      should be accessible over the internet, e.g. stored on web servers.
    :type uri: urllib.parse.ParseResult or urllib.parse.SplitResult
    """
    def __init__(self, name, prefix, uri):
        self.__name = name
        self.__prefix = prefix
        self.__uri = uri
        self.__all_attributes = None
        self.__log_attributes = set()
        self.__trace_attributes = set()
        self.__event_attributes = set()
        self.__meta_attributes = set()

    def get_name(self):
        """ Returns the human-readable name of this extension.

        :return: The name of this extension.
        :rtype: str
        """
        return self.__name

    def get_uri(self):
        """ Returns a unique URI associated with this extension. This URI should
        point to the file defining the extension, and must be able to be
        resolved. Extension files should be accessible over the internet, e.g.
        stored on web servers.

        :return: An unique URI associated with this extension
        :rtype: urllib.parse.ParseResult or urllib.parse.SplitResult
        """
        return self.__uri

    def get_prefix(self):
        """Returns a unique prefix associated with this extension. This prefix
        should be no longer than 5 characters, so as not to unnecessarily blow
        up storage files.

        :return: An unique prefix associated with this extension
        :rtype: str
        """
        return self.__prefix

    def get_defined_attributes(self):
        """Returns the collection of attributes defined by this extension for
        any log elements (archive-, log-, trace-, event-, and meta-attributes).

        :return: The collection of attributes defined by this extension
        :rtype: set
        """
        if self.__all_attributes is None:
            self.__all_attributes = set()
            self.__all_attributes.add(self.__log_attributes)
            self.__all_attributes.add(self.__trace_attributes)
            self.__all_attributes.add(self.__event_attributes)
            self.__all_attributes.add(self.__meta_attributes)

        return self.__all_attributes

    def get_log_attributes(self):
        """ Returns the collection of attributes defined by this extension for
        log elements.

        :return: the collection of attributes for log elements
        :rtype: set
        """
        return self.__log_attributes

    def get_trace_attributes(self):
        """ Returns the collection of attributes defined by this extension for
        trace elements.

        :return: the collection of attributes for trace elements
        :rtype: set
        """
        return self.__trace_attributes

    def get_event_attributes(self):
        """ Returns the collection of attributes defined by this extension for
        event elements.

        :return: The collection of attributes for event elements
        :rtype: set
        """
        return self.__event_attributes

    def get_meta_attributes(self):
        """  Return the collection of meta-attributes defined by this extension
        for attributes.

        :return: The collection of meta-attributes for attributes.
        :rtype: set
        """
        return self.__meta_attributes

    def __eq__(self, other):
        if isinstance(other, XExtension):
            return self.__uri == other.get_uri()
        return False

    def __hash__(self):
        return hash(self.__uri)

    def __str__(self):
        return self.__name

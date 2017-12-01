from opyenxes.extension.std.XConceptExtension import XConceptExtension
from opyenxes.extension.std.XCostExtension import XCostExtension
from opyenxes.extension.std.XIdentityExtension import XIdentityExtension
from opyenxes.extension.std.XLifecycleExtension import XLifecycleExtension
from opyenxes.extension.std.XMicroExtension import XMicroExtension
from opyenxes.extension.std.XOrganizationalExtension import XOrganizationalExtension
from opyenxes.extension.std.XSemanticExtension import XSemanticExtension
from opyenxes.extension.std.XTimeExtension import XTimeExtension
from opyenxes.extension.XExtensionParser import XExtensionParser
from opyenxes.utils.SingletonClassGenerator import XExtensionManagerMetaclass
from opyenxes.utils.XRuntimeUtils import XRuntimeUtils
from opyenxes.log.XLogging import XLogging
from urllib import request
import os
import time


class XExtensionManager(metaclass=XExtensionManagerMetaclass):
    """The extension manager is used to access, store, and manage extensions in
    a system. Extensions can be loaded from their given URI, which should point
    to the file defining the extension. Also, extensions can be registered
    locally, which then override any remotely-loaded extensions (which are more
    generic placeholders). Extension files downloaded from remote sources
    (which happens when the extension cannot be resolved locally) are cached on
    the local system, so that the network source of extension files is not put
    under extensive stress. The extension manager is a singleton, there is no
    need to instantiate more than one extension manager, which is necessary to
    avoid states of inconsistency.

    Uses the singleton metaclass
    """
    def __init__(self):
        self.__extension_map = dict()
        self.__extension_list = list()
        self.register_standard_extensions()

    def register(self, extension):
        """Explicitly registers an extension instance with the extension manager.

        :param extension: The extension to be registered.
        :type extension: `XExtension`
        """
        self.__extension_map[extension.get_uri()] = extension
        if extension not in self.__extension_list:
            self.__extension_list.append(extension)

    def get_by_uri(self, uri):
        """Retrieves an extension instance by its unique URI. If the extension
        has not been registered before, it is looked up in the local cache. If
        it cannot be found in the cache, the manager attempts to download it
        from its unique URI, and add it to the set of managed extensions.

        :param uri: The unique URI of the requested extension.
        :type uri: urllib.parse.ParseResult or urllib.parse.SplitResult
        :return: The requested extension.
        :rtype: `XExtension`
        """
        return self.__extension_map.get(uri)

    def get_by_name(self, name):
        """Retrieves an extension by its name. If no extension by that name can
        be found, this method returns null.

        :param name: The name of the requested extension.
        :type name: str
        :return: The requested extension (may be null, if it cannot be found).
        :rtype: `XExtension`
        """
        for elem in self.__extension_list:
            if elem.get_name() == name:
                return elem
        return None

    def get_by_prefix(self, prefix):
        """Retrieves an extension by its prefix. If no extension by that prefix
        can be found, this method returns null.

        :param prefix: The prefix of the requested extension.
        :type prefix: str
        :return: The requested extension (may be null, if it cannot be found).
        :rtype: `XExtension`
        """
        for elem in self.__extension_list:
            if elem.get_prefix() == prefix:
                return elem
        return None

    def get_by_index(self, index):
        """Retrieves an extension by ints index. If no extension with the given
        index is found, this method returns null.

        :param index: The index of the requested extension.
        :type index: int
        :return: The requested extension (may be null, if it cannot be found).
        :rtype: `XExtension`
        """
        if index in range(len(self.__extension_list)):
            return self.__extension_list[index]
        return None

    def get_index(self, extension):
        """Resolves the index of an extension, given that this extension has
        been previously registered with this manager instance. If the given
        index has not been registered previously, this method returns -1.

        :param extension:  The extension to look up the index for.
        :type extension: `XExtension`
        :return: Unique index of the requested extension (positive integer).
        :rtype: int
        """
        for i in range(len(self.__extension_list)):
            if self.__extension_list[i] == extension:
                return i
        return -1

    def register_standard_extensions(self):
        """Registers all defined standard extensions with the extension manager
        before caching.

        """
        self.register(XConceptExtension())
        self.register(XCostExtension())
        self.register(XIdentityExtension())
        self.register(XLifecycleExtension())
        self.register(XMicroExtension())
        self.register(XOrganizationalExtension())
        self.register(XSemanticExtension())
        self.register(XTimeExtension())

    @staticmethod
    def cache_extension(uri):
        """Downloads and caches an extension from its remote definition file.
        The extension is subsequently placed in the local cache, so that future
        loading is accelerated.

        :param uri: Unique URI of the extension which is to be cached.
        :type uri: urllib.parse.ParseResult or urllib.parse.SplitResult
        """
        uri_str = uri.geturl()
        if uri_str[-1] == "/":
            uri_str = uri_str[(0, len(uri_str) - 1)]
        filename = uri_str[uri_str.rindex(chr(47)):]
        if not filename.endswith(".xesext"):
            filename += ".xesext"

        cache_file = XRuntimeUtils().get_extension_cache_folder() + os.path.sep + filename

        try:
            bis = request.urlopen(uri.geturl())
            bos = open(cache_file, "w")

            file = bis.read(1024)
            while file != b"":
                bos.write(file)
                file = bis.read(1024)
            bos.close()
            XLogging().log("Cached XES extension \\'" + uri.geturl() + "\\'",
                           XLogging.Importance.DEBUG)

        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    def load_extension_cache(self):
        """Loads all extensions stored in the local cache. Cached extensions
        which exceed the maximum caching age are discarded, and downloaded
        freshly.

        """
        min_modified = (lambda: int(round(time.time() * 1000)))() - 2592000000
        ext_folder = XRuntimeUtils().get_extension_cache_folder()
        ext_files = list(filter(os.path.isfile, os.listdir(ext_folder)))
        if len(ext_files) == 0:
            XLogging().log("Extension caching disabled (Could not access cache"
                           " directory)!",
                           XLogging.Importance.WARNING)
            return

        for i in range(len(ext_files)):
            ext_file = ext_files[i]
            if ext_file.lower().endswith(".xesext"):
                file_name = ext_folder + os.path.sep + ext_file
                if os.path.getmtime(file_name) * 1000 < min_modified:
                        if os.path.exists(file_name):
                            os.remove(file_name)
                else:
                    try:
                        extension = XExtensionParser.parse(file_name)
                        if extension.get_uri() not in self.__extension_map:
                            self.__extension_map[extension.get_uri()] = extension
                            self.__extension_list.append(extension)
                            XLogging().log("Loaded XES extension \'" +
                                           extension.get_uri().geturl() +
                                           "\' from cache",
                                           XLogging.Importance.DEBUG)
                        else:
                            XLogging().log("Skipping cached XES extension \'" +
                                           extension.get_uri().geturl() +
                                           "\' (already defined)",
                                           XLogging.Importance.DEBUG)
                    except Exception as e:
                        print("Exception error: {}".format(e))

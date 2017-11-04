import sys
import os


class XRuntimeUtils:
    """This class provides runtime utilities for library components.
    Its main purpose is to identify the host OS, and to locate a standard
    support folder location on each platform.

    """
    xes_version = "1.0"
    openxes_version = "1.0RC7"

    def __init__(self):
        self.__current_os = None

    def determine_os(self):
        """Determines the current host platform.

        :return: Current host platform.
        :rtype: str
        """
        if self.__current_os is None:
            self.__current_os = sys.platform

        return self.__current_os

    def is_running_windows(self):
        """ Checks whether the current platform is Windows.

        :return: True if the current platform is Windows. False otherwise.
        :rtype: bool
        """
        return self.determine_os().startswith("win32")

    def is_running_mac_os_x(self):
        """ Checks whether the current platform is Mac OS X.

        :return: True if the current platform is Mac OS X. False otherwise.
        :rtype: bool
        """
        return self.determine_os().startswith("darwin")

    def is_running_linux(self):
        """ Checks whether the current platform is Linux.

        :return: True if the current platform is Linux. False otherwise.
        :rtype: bool
        """
        return self.determine_os().startswith("linux")

    def is_running_unix(self):
        """ Checks whether the current platform is some flavor of Unix.

        :return: True if the current platform is some flavor of Unix. False otherwise.
        :rtype: bool
        """
        return self.determine_os().startswith("freebsd") or self.is_running_linux() or self.is_running_mac_os_x()

    def get_support_folder(self):
        """Retrieves the path of the platform-dependent OpenXES support folder.

        :return: The path of the platform-dependent OpenXES support folder.
        :rtype: str
        """
        home_dir = os.path.expanduser(os.getenv('USERPROFILE'))
        dir_name = "OpenXES"
        if self.is_running_windows():
            os.makedirs(home_dir + "\\" + dir_name)
            return home_dir + "\\" + dir_name + "\\"
        elif self.is_running_mac_os_x():
            os.makedirs(home_dir + "/Library/Application Support/" + dir_name)
            return home_dir + "/Library/Application Support/" + dir_name + "/"
        else:
            os.makedirs(home_dir + "/." + dir_name)
            return home_dir + "/." + dir_name + "/"

    def get_extension_cache_folder(self):
        """Retrieves the directory file of the platform-dependent OpenXES extension definition file folder.

        :return: the directory file of the platform-dependent.
        :rtype: str
        """
        ext_folder = self.get_support_folder() + "ExtensionCache"
        os.makedirs(ext_folder)
        return ext_folder

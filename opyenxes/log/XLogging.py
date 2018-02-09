from opyenxes.log.XStdoutLoggingListener import XStdOutLoggingListener


class XLogging:
    """This class provides low-level logging for library components.
    Used for debugging.

    """
    def __init__(self):
        self.__listener = XStdOutLoggingListener()

    def set_listener(self, listener):
        """Sets a new logging listener.

        :param listener: New logging listener.
        :type listener: `XStdOutLoggingListener`
        """
        self.__listener = listener

    def log(self, message, importance=None):
        """Logs the given message with debug importance.

        :param message: The log message.
        :param importance: Importance of the message.
        """
        if importance is None:
            self.log(message, "DEBUG")

        elif self.__listener is not None:
            self.__listener.log(message, importance)

    class Importance:
        """Defines the importance of logging messages.

        """
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"

class XStdOutLoggingListener:
    """Default standard output logging listener.

    """
    @staticmethod
    def log(message, importance):
        """Receives an internal OpenXES log message and print that in the
        console.

        :param message: Text of the log message.
        :type message: str
        :param importance: Importance of the log message.
        :type importance: str
        """
        print("Importance: {}\nMessage: {}\n".format(importance, message))

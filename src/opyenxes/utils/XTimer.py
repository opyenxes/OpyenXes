import time


class XTimer:
    """This class implements a simple timer that can be used to quickly profile
    the speed of operations within library components. The timer simply uses the
    system time for timing, and thus does not incur significant overhead on
    runtime.

    """
    DAY_MILLIS = 86400000
    HOUR_MILLIS = 3600000
    MINUTE_MILLIS = 60000
    SECOND_MILLIS = 1000
    __start = time.time() * 1000

    def __init__(self):
        self.__stop = self.__start

    def start(self):
        """Starts the timer.

        """
        self.__start = time.time() * 1000
        self.__stop = self.__start

    def stop(self):
        """Stops the timer (takes time).

        """
        self.__stop = time.time()

    def get_duration(self):
        """Retrieve the runtime of the timer.

        :return: Runtime between start (or creation of timer) and stop, in milliseconds.
        :rtype: int
        """
        if self.__start == self.__stop:
            return time.time() * 1000 - self.__stop
        return self.__stop - self.__start

    def get_duration_string(self):
        """Retrieve the runtime of the timer as a pretty-print string.

        :return: Runtime between start (or creation of timer) and stop, as a
         pretty-print string.
        :rtype: str
        """
        return self.format_duration(self.get_duration())

    @staticmethod
    def format_duration(millis):
        """Formats a duration in milliseconds as a pretty-print string.

        :param millis: Duration in milliseconds.
        :type millis: int or float
        :return: Given duration as a pretty-print string.
        :rtype: str
        """
        sb = list()
        if millis > 86400000:
            sb.append(str(millis // 86400000))
            sb.append(" days, ")
            millis %= 86400000

        if millis > 3600000:
            sb.append(str(millis // 3600000))
            sb.append(" hours, ")
            millis %= 3600000

        if millis > 60000:
            sb.append(str(millis // 60000))
            sb.append(" minutes, ")
            millis %= 60000

        if millis > 1000:
            sb.append(str(millis // 1000))
            sb.append(" seconds, ")
            millis %= 1000

        sb.append(str(millis))
        sb.append(" milliseconds")
        return "".join(sb)

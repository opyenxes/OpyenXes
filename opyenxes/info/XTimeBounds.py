from datetime import datetime
from opyenxes.model.XEvent import XEvent
from opyenxes.extension.std.XTimeExtension import XTimeExtension


class XTimeBounds:
    """This class implements timestamp boundaries, which can be used to describe
    the temporal extent of a log, or of a contained trace.

    """
    def __init__(self):
        self.__first = None
        self.__last = None

    def get_start_date(self):
        """Returns the earliest timestamp of these boundaries (left bound).

        :return: The earliest timestamp of these boundaries.
        :rtype: datetime
        """
        return self.__first

    def get_end_date(self):
        """Returns the latest timestamp of these boundaries (right bound).

        :return: The latest timestamp of these boundaries.
        :rtype: datetime
        """
        return self.__last

    def is_within(self, date):
        """Checks, whether the given date is within these boundaries.

        :param date: Date to be checked.
        :type date: datetime
        :return: Whether the specified date is within these boundaries.
        :rtype: bool
        """
        if self.__first is not None:
            if date == self.__first:
                return True
            if date == self.__last:
                return True
            if self.__first < date < self.__last:
                return True
            return False
        return False

    def register(self, element):
        """Registers the given timestamp boundaries. These timestamp boundaries
        will be potentially adjusted to accomodate for inclusion of the given
        boundaries.

        :param element: Timestamp boundaries to be registered.
        :type element: `XTimeBounds` or `XEvent` or datetime
        """
        if isinstance(element, XTimeBounds):
            self.register(element.get_start_date())
            self.register(element.get_end_date())
        elif isinstance(element, XEvent):
            date = XTimeExtension().extract_timestamp(element)
            if date is not None:
                self.register(date)
        elif isinstance(element, datetime):
            if element is not None:
                if self.__first is None:
                    self.__first = element
                    self.__last = element
                elif element < self.__first:
                    self.__first = element
                elif element > self.__last:
                    self.__last = element

    def __str__(self):
        return "{} -- {}".format(str(self.__first), str(self.__last))

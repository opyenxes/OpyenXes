from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.utils.SingletonClassGenerator import XTimeExtensionMetaclass
import time
from datetime import datetime


class XTimeExtension(XExtension, metaclass=XTimeExtensionMetaclass):
    """This extension defines the Time perspective on event logs. It makes it
    possible to assign to each event a timestamp, describing when the event has
    occurred.

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Time", "time", urlparse("http://www.xes-standard.org/time.xesext"))
        factory = XFactoryRegistry().current_default()

        self.ATTR_TIMESTAMP = factory.create_attribute_timestamp("time:timestamp", 0, self)

        self.get_event_attributes().add(self.ATTR_TIMESTAMP)

        XGlobalAttributeNameMap().register_mapping("EN", "time:timestamp", "Timestamp")
        XGlobalAttributeNameMap().register_mapping("DE", "time:timestamp", "Zeitstempel")
        XGlobalAttributeNameMap().register_mapping("FR", "time:timestamp", "Horodateur")
        XGlobalAttributeNameMap().register_mapping("ES", "time:timestamp", "Timestamp")
        XGlobalAttributeNameMap().register_mapping("PT", "time:timestamp", "Timestamp")

    @staticmethod
    def extract_timestamp(event):
        """Extracts from a given event the timestamp.

        :param event: Event to be queried.
        :type event: `XEvent`
        :return: The timestamp of this event, as a datetime object (may be null
         if not defined).
        :rtype: datetime
        """
        attribute = event.get_attributes().get("time:timestamp")
        if attribute:
            return attribute.get_value()
        return -1

    def assign_timestamp(self, event, date):
        """Assigns to a given event its timestamp.

        :param event: Event to be modified.
        :type event: `XEvent`
        :param date: Timestamp, as a datetime object or as a long of
            milliseconds in UNIX time..
        :type date: datetime or int
        """
        if isinstance(date, datetime):
            aux = time.mktime(date.timetuple()) * 1000
        else:
            aux = date

        attr = self.ATTR_TIMESTAMP.clone()
        attr.set_value_millis(aux)
        event.get_attributes()["time:timestamp"] = attr

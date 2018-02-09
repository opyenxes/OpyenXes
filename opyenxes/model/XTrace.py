from opyenxes.model.XElement import XElement


class XTrace(XElement, list):
    """ A trace is an element of an XES event log structure. Traces are
    contained in logs. Any trace is a list of events. Traces describe sequences
    of events, as they have occurred during one execution of a process,
    in their given order.

    :param attributes: Map of attribute for the trace.
    :type attributes: `XAttributeMap`
    """
    def __init__(self, attributes):
        super().__init__(attributes)

    def clone(self):
        """Creates and returns a copy of this object.

        :return: A clone of this instance.
        :rtype: `XTrace`
        """
        clone = XTrace(self.get_attributes().clone())
        for event in self:
            clone.append(event.clone())

        return clone

    def insert_ordered(self, event):
        """Insert the event in an ordered manner, if timestamp information is
         available in this trace.

        :param event: the event to be inserted.
        :type event: `XEvent`
        :return: index of the inserted event.
        :rtype: int
        """
        if len(self) == 0:
            self.append(event)
            return 0
        elif "time:timestamp" not in event.get_attributes():
            self.append(event)
            return len(self) - 1
        else:
            ins_ts = event.get_attributes()["time:timestamp"].get_value()
            for i in range(len(self) - 1, -1, -1):
                my_event = self[i].get_attributes().get("time:timestamp")
                if my_event is None:
                    self.append(event)
                    return len(self) - 1

                ref_ts = my_event.get_value()
                if ins_ts >= ref_ts:
                    self.insert(i + 1, event)
                    return i + 1

            self.insert(0, event)
            return 0

    def append(self, p_object):
        """
        Add only a event object in the log.

        :param p_object: a Event object to append for the log
        :type p_object: `XEvent`
        """
        super(XTrace, self).append(p_object)

    def __hash__(self):
        return hash(super(XTrace, self))

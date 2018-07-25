"""
Anonymize a log.
All value of "resource" attribute and "org:resource" attribute will be "UNKNOWN" now:
"""

from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.data_out.XesXmlSerializer import XesXmlSerializer


path = "xes_file/general_example.xes"
with open(path) as log_file:
    log = XUniversalParser().parse(log_file)[0]

# Search in global trace attribute
for attribute in log.get_global_trace_attributes():
    if attribute.get_key() in ["Resource", "org:resource"]:
        attribute.set_value("UNKNOWN")

# Search in global event attribute
for attribute in log.get_global_event_attributes():
    if attribute.get_key() in ["Resource", "org:resource"]:
        attribute.set_value("UNKNOWN")

# Search in trace
for trace in log:
    # Search in trace attribute
    for attribute in trace.get_attributes().values():
        if attribute.get_key() in ["Resource", "org:resource"]:
            attribute.set_value("UNKNOWN")
    # Search in event
    for event in trace:
        # Search in event attribute
        for attribute in event.get_attributes().values():
            if attribute.get_key() in ["Resource", "org:resource"]:
                attribute.set_value("UNKNOWN")

# Save the new log in .xes format
with open(path[:-4] + "_anonymous.xes", "w") as file:
    XesXmlSerializer().serialize(log, file)

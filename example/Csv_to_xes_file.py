"""
Read a csv file and convert that in xes file
"""


from opyenxes.factory.XFactory import XFactory
from datetime import datetime
from opyenxes.out.XesXmlSerializer import XesXmlSerializer


def convert_line_in_event(type_for_attribute: dict, attribute_list: list):
    """Read one line and convert in a Xes Event object

    :param type_for_attribute: dictionary with the type of all attribute.
    :param attribute_list: List with the attribute in string format
    :return: An XEvent with the respective attribute
    """
    attribute_map = XFactory.create_attribute_map()
    for index in range(2, len(attribute_list)):
        attribute_string = attribute_list[index]
        attribute_type = type_for_attribute[str(index)]
        if attribute_type == "Activity" or attribute_type == "Resource":
            attribute = XFactory.create_attribute_literal(attribute_type, attribute_string)
        elif "%Y" in attribute_type:  # "date"
            attribute = XFactory.create_attribute_timestamp("time", datetime.strptime(attribute_string, attribute_type))
        else:  # Cost
            attribute = XFactory.create_attribute_discrete(attribute_type, int(attribute_string))
        attribute_map[attribute.get_key()] = attribute
    return XFactory.create_event(attribute_map)


with open("xes_file/csv_file.csv") as file:
    first_line = file.readline().split(";")
    dictionary = {}
    for i in range(len(first_line)):
        if "yyyy" in first_line[i]:
            # Convert csv date format in xes date format
            first_line[i] = first_line[i].replace("dd", "%d").\
                replace("MM", "%m").replace("yyyy", "%Y").replace("HH", "%H").\
                replace("mm", "%M")

        dictionary[str(i)] = first_line[i].strip("\n")

    first_event = file.readline().split(";")
    actual_trace = first_event[0]

    log = XFactory.create_log()
    trace = XFactory.create_trace()
    trace.append(convert_line_in_event(dictionary, first_event))

    for line in file.readlines():
        line_list = line.split(";")
        event = convert_line_in_event(dictionary, line_list)
        if line_list[0] == actual_trace:  # View the Case Id
            trace.append(event)
        else:
            log.append(trace)
            trace = XFactory.create_trace()
            trace.append(event)

# Save log in xes format
with open("xes_file/csv_log_in_xes_format.xes", "w") as file:
    XesXmlSerializer().serialize(log, file)

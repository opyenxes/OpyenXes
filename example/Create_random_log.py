"""
Create_random_log:
"""
from opyenxes.factory.XFactory import XFactory
from opyenxes.id.XIDFactory import XIDFactory
from opyenxes.data_out.XesXmlSerializer import XesXmlSerializer
import random


number_trace = 10
minimum_length_of_trace = 3
maximum_length_of_trace = 7
attributes_per_event = 4

log = XFactory.create_log()
for a in range(number_trace):
    trace = XFactory.create_trace()
    for e in range(random.randint(minimum_length_of_trace, maximum_length_of_trace)):
        event = XFactory.create_event()
        for _ in range(attributes_per_event):
            # Generate random attribute
            option = random.choice(["string", "date", "int", "float",
                                    "boolean", "id", "list", "container"])
            if option == "string":
                attribute = XFactory.create_attribute_literal(option, "UNKNOWN")
            elif option == "date":
                attribute = XFactory.create_attribute_timestamp(option, 0)
            elif option == "int":
                attribute = XFactory.create_attribute_discrete(option, 0)
            elif option == "float":
                attribute = XFactory.create_attribute_continuous(option, 0.0)
            elif option == "boolean":
                attribute = XFactory.create_attribute_boolean(option, True)
            elif option == "id":
                attribute = XFactory.create_attribute_id(option, XIDFactory.create_id())
            elif option == "list":
                attribute = XFactory.create_attribute_list(option)
            else:
                attribute = XFactory.create_attribute_container(option)
            event.get_attributes()[option] = attribute
        trace.append(event)
    log.append(trace)

# Save the random log in .xes format
with open("xes_file/random_log.xes", "w") as file:
    XesXmlSerializer().serialize(log, file)

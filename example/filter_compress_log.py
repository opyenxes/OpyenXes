"""
In this example we view take one attribute per event, for example, the Activity
and we remove the similar trace if the have the same sequence of attribute per event

if the log = [[a,b,c,d],[a,b,c],[a,b,c,d],[a,b,c,d],[a,b,e,d],[a,b,c]]
The new log will be = [[a,b,c,d],[a,b,c],[a,b,e,d]]
"""
from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.out.XesXmlGZIPSerializer import XesXmlGZIPSerializer
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


def same_trace(trace_a, trace_b, classifier):
    if len(trace_a) != len(trace_b):
        return False

    for event_a, event_b in zip(trace_a, trace_b):
        if not classifier.same_event_class(event_a, event_b):
            return False

    return True


with open("xes_file/example_compress_log.xes.gz") as file:
    logs = XUniversalParser().parse(file)

log = logs[0]
new_log = log.clone()
classifier = XEventAttributeClassifier("activity", ["Activity"])
new_log.clear()

print("The log have {} traces".format(len(log)))

for trace_a in log:
    new_log_have_this_trace = False

    index = 0
    while not new_log_have_this_trace and index < len(new_log):
        trace_b = new_log[index]

        if same_trace(trace_a, trace_b, classifier):
            new_log_have_this_trace = True

        index += 1

    if not new_log_have_this_trace:
        new_log.append(trace_a)

print("The new log have {} traces".format(len(new_log)))

with open("xes_file/new_filter_and_compress_log.xes.gz", "w") as file:
    XesXmlGZIPSerializer().serialize(new_log, file)

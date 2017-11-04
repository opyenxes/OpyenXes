from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from collections import defaultdict
from matplotlib import pylab as plt
import numpy as np


with open("xes_file/example_compress_log.xes.gz") as file:
    logs = XUniversalParser().parse(file)

classifier = XEventAttributeClassifier("Resource", ["Resource"])
people_dict = defaultdict(lambda: 0)
for log in logs:
    for trace in log:
        for event in trace:
            people = classifier.get_class_identity(event)
            people_dict[people] += 1

name_people = list(people_dict.keys())
posicion_y = np.arange(len(name_people))
units = list(map(lambda people: people_dict[people], name_people))
plt.barh(posicion_y, units, align ="center")
plt.yticks(posicion_y, name_people)
plt.xlabel('Number of activities')
plt.title("Activities done by people")
plt.show()

from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.extension.XExtensionParser import XExtensionParser
from opyenxes.extension.XExtensionManager import XExtensionManager

with open("xes_file/example_with_new_extension.xes") as file:
    logs = XUniversalParser().parse(file)

# The console will print:
"""
    > Unknown extension: http://www.xes-standard.org/meta_concept.xesext
    > Unknown extension: http://www.xes-standard.org/meta_general.xesext
"""

# We must parse the new extension, can be the link or the xml file
meta_concept = XExtensionParser().parse("http://www.xes-standard.org/meta_concept.xesext")
meta_general = XExtensionParser().parse("xes_file/meta_general.xesext.xml")

# Then we register the new extension
XExtensionManager().register(meta_concept)
XExtensionManager().register(meta_general)

# Now we can parse again
with open("xes_file/example_with_new_extension.xes") as file:
    logs = XUniversalParser().parse(file)

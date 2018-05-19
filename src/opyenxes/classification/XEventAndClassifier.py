from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


class XEventAndClassifier(XEventAttributeClassifier):
    """Composite event classifier, which can hold any number of lower-level
    classifiers, concatenated with boolean AND logic. This classifier will
    consider two events as equal, if all of its lower-level classifiers consider
    them as equal.

    :param comparators: Any number of lower-level classifiers, which are
     evaluated with boolean AND logic. If multiple lower-level classifiers use
     the same keys, this key is used only once in this classifier.
    :type comparators: list[`XEventAttributeClassifier`]
    """
    def __init__(self, comparators):
        if len(comparators) == 0:
            raise ValueError("The comparators must have at least 1 element ")
        sb = []
        keys = []
        sb.append("(")
        sb.append(comparators[0].name())

        for key in comparators[0].get_defining_attribute_keys():
            if key not in keys:
                keys.append(key)

        for i in range(1, len(comparators)):
            sb.append(" AND ")
            sb.append(comparators[i].name())

            for key in comparators[i].get_defining_attribute_keys():
                if key not in keys:
                    keys.append(key)

        sb.append(")")

        super().__init__("".join(sb), sorted(keys))

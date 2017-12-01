import itertools
import copy
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier


def gen():
    """Generator of unique id

    """
    n = 0
    while True:
        yield n
        n += 1


class Footprint:
    """Helper class thar identify all relation between the events, i.e. identify
    the direct succession, causal, parallel and choice relation in the log

    :param all_event: set with all event in the log
    :type all_event: set[str]
    :param log_object: An array with lists of string element that represent the log process
    :type log_object: list[list[str]]

    """
    def __init__(self, all_event, log_object):

        self.direct_succession = list()
        self.causal = list()
        self.choice = list()
        self.parallel = list()
        self.all_event = all_event
        self.log = log_object

        self._generate_footprint()

    def _generate_footprint(self):
        direct_followers = set()
        for trace in self.log:
            for index in range(len(trace) - 1):
                direct_followers.add((trace[index], trace[index + 1]))

        self.direct_succession = list(direct_followers)

        causal = set()
        for pair in self.direct_succession:
            if pair[::-1] not in self.direct_succession:
                causal.add(pair)

        self.causal = list(causal)

        choice = set()
        parallel = set()

        for pair in itertools.product(self.all_event, repeat=2):
            if pair not in self.direct_succession and pair[::-1] not in self.direct_succession:
                choice.add(pair)

            if pair in self.direct_succession and pair[::-1] in self.direct_succession:
                parallel.add(pair)

        self.choice = list(choice)
        self.parallel = list(parallel)


class Place:
    """Class that represent one place in the Petri Net

    :param start: Set with the events tha be before the place
    :type start: set(str)
    :param end: Set with the events that be after the place.
    :type end: set(str)
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.name = None


class AlphaAlgorithm:
    """Class that generate the Petri Net using the alpha algorithm.

    :param log_object: An array with lists of string element that represent the log process
    :type log_object: list[list[str]]
    """
    def __init__(self, log_object):
        self.gen = gen()
        self.log = log_object
        # Steps 1,2,3
        self.starting_events = set()
        self.ending_events = set()
        self.all_event = set()

        self._extract_events()

        # Generate footprint
        self.footprint = Footprint(self.all_event, self.log)

        # Calculate pairs
        self.pairs = self._build_pairs()

        # Delete non-maximal pairs and generate places from pairs
        self.places = self._generate_places()
        self.text = self._generate_text()

    @staticmethod
    def _check_one_set(one_set, not_causal):
        for pair in itertools.product(one_set, repeat=2):
            if pair not in not_causal:
                return False
        return True

    @staticmethod
    def _check_two_set(set_a, set_b, causal):
        for par in itertools.product(set_a, set_b):
            if par not in causal:
                return False
        return True

    def _build_pairs(self):
        xl = set()
        combinations_sets = set()
        for i in range(1, len(self.all_event)):
            for sets in itertools.combinations(self.all_event, i):
                combinations_sets.add(sets)

        for set_a in combinations_sets:
            if self._check_one_set(set_a, self.footprint.choice):
                for set_b in combinations_sets:
                    if self._check_one_set(set_b, self.footprint.choice) and \
                            self._check_two_set(set_a, set_b, self.footprint.causal):
                        xl.add((set_a, set_b))
        return xl

    def _generate_places(self):
        yl = copy.deepcopy(self.pairs)
        for first_transition in self.pairs:
            for second_transition in self.pairs:

                if first_transition != second_transition and\
                   set(first_transition[0]).issubset(second_transition[0]) and\
                   set(first_transition[1]).issubset(second_transition[1]):

                    yl.discard(first_transition)
        return yl

    def _extract_events(self):
        for trace in self.log:
            self.starting_events.add(trace[0])
            self.ending_events.add(trace[-1])
            self.all_event.update(trace)

    def _generate_text(self):
        aux = gen()
        next(aux)
        array_text = []
        places = list()
        places.append(Place(None, self.starting_events))
        places.append(Place(self.ending_events, None))

        for place in self.places:
            places.append(Place(*place))

        for place in places:
            name = "place_{}".format(next(self.gen))
            place.name = name
            text = 'Place "{}";'.format(name)
            if place.start is None:
                text = text.replace(";", " init {};".format(next(aux)))
            array_text.append(text)

        next(self.gen)
        for event in self.all_event:
            start = []
            end = []
            for place in places:
                if place.end and event in place.end:
                    start.append(place.name)
                elif place.start and event in place.start:
                    end.append(place.name)

            a1 = map(lambda ev: '"{}"'.format(ev), start)
            a2 = map(lambda ev: '"{}"'.format(ev), end)
            text = 'trans "t_{}"~"{}+complete" in {} out {} ;'.\
                format(next(self.gen),
                       event,
                       " ".join(a1),
                       " ".join(a2))
            array_text.append(text)

        return "\n".join(array_text)

    def __str__(self):
        return self.text

    def save(self, file_name):
        """Write the Petri Net with tpn format

        :param file_name: The name of the file to save the Petri Net
        :type file_name: str
        """
        with open(file_name + ".tpn", "w") as file:
            file.write(self.text)


if __name__ == '__main__':
    from opyenxes.data_in.XUniversalParser import XUniversalParser

    path = "xes_file/general_example.xes"
    with open(path) as log_file:
        # Parse the log
        log = XUniversalParser().parse(log_file)[0]

    # Generate the classifier
    classifier = XEventAttributeClassifier("activity", ["Activity"])

    # Convert log object in array with only the Activity attribute of the event
    log_list = list(map(lambda trace: list(map(classifier.get_class_identity, trace)), log))

    # Generate the Alpha Algorithm with the array
    alpha = AlphaAlgorithm(log_list)
    print(alpha)
    # Save the result with tpn format
    alpha.save(path[:-4] + "_AlphaAlgorithm")

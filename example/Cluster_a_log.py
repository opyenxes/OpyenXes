from opyenxes.model.XLog import XLog
from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.out.XesXmlSerializer import XesXmlSerializer
from sklearn.cluster import KMeans
from opyenxes.factory.XFactory import XFactory


if __name__ == '__main__':
    path = "xes_file/log_to_cluster.xes"
    # Parse Logs
    with open(path) as log_file:
        log = XUniversalParser().parse(log_file)[0]  # type: XLog

    # Convert log object in array with only the Activity attribute of the event
    classifier = XEventAttributeClassifier("activity", ["Activity"])
    log_list = list(map(lambda trace: list(map(classifier.get_class_identity, trace)), log))

    event_set = set()
    for trace in log_list:
        for event in trace:
            event_set.add(event)

    all_event = list(event_set)

    log_vector = []
    for trace in log_list:
        trace_vector = []
        for event in all_event:
            trace_vector.append(trace.count(event))
        log_vector.append(trace_vector.copy())

    # Constant
    NUM_CLUSTERS = 2
    MAX_ITERATIONS = 10
    INITIALIZE_CLUSTERS = 'k-means++'
    CONVERGENCE_TOLERANCE = 0.001
    NUM_THREADS = 8

    kmeans = KMeans(n_clusters=NUM_CLUSTERS,
                    max_iter=MAX_ITERATIONS,
                    init=INITIALIZE_CLUSTERS,
                    tol=CONVERGENCE_TOLERANCE,
                    n_jobs=NUM_THREADS)

    # Create the cluster with the log vector
    kmeans.fit(log_vector)

    # Create new log with the attribute for the original log
    new_logs = {}
    for i in range(len(kmeans.cluster_centers_)):
        new_log = XFactory.create_log(log.get_attributes().clone())
        for elem in log.get_extensions():
            new_log.get_extensions().add(elem)

        new_log.__classifiers = log.get_classifiers().copy()
        new_log.__globalTraceAttributes = log.get_global_trace_attributes().copy()
        new_log.__globalEventAttributes = log.get_global_event_attributes().copy()

        new_logs[str(i)] = new_log

    # Distribute the trace depending the cluster.
    for point, trace in zip(log_vector, log):
        cluster = kmeans.predict([point])[0]
        new_logs[str(cluster)].append(trace)

    # Write the new logs
    log_id = 0
    for log in new_logs.values():
        with open("xes_file/New_cluster_log_{}.xes".format(str(log_id)), "w") as file:
            XesXmlSerializer().serialize(log, file)
        log_id += 1

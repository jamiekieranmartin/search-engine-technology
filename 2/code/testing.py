def test(collections, topic_statements, benchmarks, ranks):
    """
    Test the given ranks against the benchmarks for each collection
    """
    test = {}
    # for each collection in collections
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"]
        ben, rank = benchmarks[topic], ranks[topic]

        A = {k:v for k,v in ben.items() if v == 1}

        i = 0.0
        for id in A:
            if id in rank:
                i += 1
        # calculate precision
        try:
            p = i / len(rank)
        except ZeroDivisionError:
            p = i
        # calculate recall
        try:
            r = i / len(A)
        except ZeroDivisionError:
            r = i
        # calculate f1
        try:
            f1 = (2 * r * p) / (r + p)
        except ZeroDivisionError:
            f1 = 2 * r * p
        # append to test results
        test[topic] = [p, r, f1]
    return test

def output(bl_test, lr_test):
    """
    Output the given test results for each test
    """
    file = open('..\\output\\Eresult1.dat', 'w')
    file.write('topic precision recall f1\n')
    # iterate over results and write line
    for topic, result in lr_test.items():
        precision = result[0]
        recall = result[1]
        f1 = result[2]
        file.write('{topic} {precision} {recall} {f1}\n'.format(topic=topic[1:], precision=precision, recall=recall, f1=f1))
    file.close()

    file = open('..\\output\\Eresult2.dat', 'w')
    file.write('topic precision recall f1\n')
    # iterate over results and write line
    for topic, result in bl_test.items():
        precision = result[0]
        recall = result[1]
        f1 = result[2]
        file.write('{topic} {precision} {recall} {f1}\n'.format(topic=topic[1:], precision=precision, recall=recall, f1=f1))
    file.close()

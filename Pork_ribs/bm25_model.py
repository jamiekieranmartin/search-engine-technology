import os


def get_all_topics(input):
    """Get all the topics' code and names (as queries) for BM25

    Return
    queries(dict) - A dictionary of Topic code : topic title 
    """
    xmlFile = open(input)
    xmlContent = xmlFile.read()
    lines = xmlContent.split('\n')
    xmlFile.close()

    topic_title = []
    topic_code = []
    queries = {}
    for line in lines:
        if line.startswith('<num>'):
            code = line.strip()[-4:]
            topic_code.append(code)
        elif line.startswith('<title>'):
            topic = line[7:]
            topic_title.append(topic)

    for i in range(len(topic_code)):
        queries[topic_code[i]] = topic_title[i]
    return queries


def get_topic(input, topic_code):
    """ Get topic's title given topic number
    """
    xmlFile = open(input)
    xmlContent = xmlFile.read()
    lines = xmlContent.split('\n')
    xmlFile.close()

    getCode = False
    for line in lines:
        if line.startswith('<num>'):
            code = line.strip()[-4:]
            if code == topic_code:
                getCode = True
        elif line.startswith('<title>'):
            if getCode:
                topic = line[7:]
                return topic


def BM25(listBD, df_dict):
    """Solve task3

    Parameters:
    listBD (dict) - A linked list of BowDoc
    df_dict (dict) - The document-frequency dictionary of all documents
    """

    # Queries array to contains all the queries needed to test
    result = get_all_topics('TopicStatements101-150.txt')

    for code, title in result.items():
        # Perform BM25 ranking and print to the file."
        BM25_model = discover_training(listBD, df_dict, code)
        print_result(BM25_model, code)


def discover_training(listBD, df_dict, code):
    """ Get the BM25 baseline model base on a topic's code
    """
    result = get_topic('TopicStatements101-150.txt', code)
    return listBD.BM25(result, df_dict)


def print_result(BM25_Model, topic_code):
    """ Print out the result to each file

    Parameters
    BM25_Model (dict) - BM25 dictionary
    """
    code = topic_code[-2:]
    if code[0] == '0':
        code = code[-1:]
    filename = "Task1_3\BLresult" + code + '.dat'
    benchmark_file = "Benchmark\Training" + code + '.txt'
    # Remove the existing result file
    if os.path.exists(filename):
        os.remove(filename)

    # Remove the existing benchmark file
    if os.path.exists(benchmark_file):
        os.remove(benchmark_file)

    # Open the fild corresponding to the topic number
    new_fo = open(filename, 'a')
    benchmark_fo = open(benchmark_file, 'a')

    # Loop through the BM25 baseline model to print out the result
    for i in BM25_Model:

        txt3 = "{id}:{score}\n".format(id=i[0], score=i[1])
        new_fo.write(txt3)

        # Check value =1 if score > 1.0, else it's 0
        check_value = 0
        if (float(i[1]) > 1.0):
            check_value = 1
        else:
            check_value = 0

        txt = "{topic_code} {doc_id} {check_value}\n".format(
            topic_code=topic_code, doc_id=i[0], check_value=check_value)
        benchmark_fo.write(txt)
        # Else break

    new_fo.write('\n')
    new_fo.close()
    benchmark_fo.close()


if __name__ == '__main__':
    result = get_all_topics('TopicStatements101-150.txt')

    # print(result)
    # print(result)
    for code, title in result.items():
        print(code, " ", title)

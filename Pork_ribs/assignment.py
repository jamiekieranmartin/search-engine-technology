import os
from Generate_BowDoc import getTrainingData
from Calculate_DF import getdf
from bm25_model import discover_training, print_result, get_all_topics
import time


def get_BowDoc_list():
    """ Get all BwoDoc for each topics

    Return:
    list_BDList: A list of linked list, contains all BowDoc LL for each topic
    """
    result = get_all_topics('TopicStatements101-150.txt')
    list_BDList = []
    print("Getting BowDoc List...")
    for topic_code, title in result.items():
        BDList = getTrainingData(topic_code)
        BDList.createTopicCode(topic_code)
        list_BDList.append(BDList)
    return list_BDList


def task1_3(list_BDList):
    """ Perform task 1.3
    """
    print("Calculating BM25 score...")
    for BDList in list_BDList:
        topic_code = BDList.getTopicCode()
        df_dict = getdf(BDList)
        bm25_model = discover_training(BDList, df_dict, topic_code)
        print_result(bm25_model, topic_code)
    print("Task ended.")


def get_benchmarks(topic_code):
    """ Generate benchmark file according to each topics

    Parameter:
    topic_code(string) - Topic code's number
    """
    ben = {}
    code = topic_code[-2:]
    if code[0] == '0':
        code = code[-1:]

    fileName = "Benchmark\Training" + code + ".txt"
    benFile = open(fileName)
    file_ = benFile.readlines()

    ben = {}
    for line in file_:
        line = line.strip()
        lineList = line.split()
        ben[lineList[1]] = float(lineList[2])

    benFile.close()
    return ben


def calculate_w4(list_BDList):
    theta = 3.5
    weight_list = []
    for BDList in list_BDList:
        ben = get_benchmarks(BDList.getTopicCode())
        bm25_weight = BDList.w4(ben, theta)
        weight_list.append(bm25_weight)

    return weight_list


def print_w4(ranks, topic_code):
    code = topic_code[-2:]
    if code[0] == '0':
        code = code[-1:]
    filename = "Task2_2\LRresult" + code + '.dat'
    # Remove the existing result file
    if os.path.exists(filename):
        os.remove(filename)

    fo = open(filename, 'a')
    for (d, v) in sorted(ranks.items(), key=lambda x: x[1], reverse=True):
        fo.write(d + ' ' + str(v) + '\n')
    fo.close()


# Main program
if __name__ == "__main__":
    # # Q1.1
    # # Generate a bow_Doc list base on the dataset
    # topic_code = 'R102'

    # BDList = getTrainingData(topic_code)
    # df_dict = getdf(BDList)
    # bm25_model = discover_training(BDList, df_dict, topic_code)

    # # Q1.2
    # if os.path.exists('BM25.txt'):
    #     os.remove('BM25.txt')
    # fo = open('BM25.txt', 'a')
    # for i in bm25_model:
    #     check_value = 0
    #     if (float(i[1]) > 1.0):
    #         check_value = 1
    #     else:
    #         check_value = 0

    #     txt = "{topic_code} {doc_id} {check_value}\n".format(
    #         topic_code=topic_code, doc_id=i[0], check_value=check_value)
    #     fo.write(txt)
    # fo.close()

    # Q1.3
    start_time = time.time()
    list_BDList = get_BowDoc_list()
    print("Time wasted: ", time.time() - start_time)
    task1_3(list_BDList)
    theta = 3.5

    # Q2.5
    features_list = calculate_w4(list_BDList)
    for i in range(len(features_list)):
        topic_code = list_BDList[i].getTopicCode()

        ranks = list_BDList[i].bm25Testing(features_list[i])
        print_w4(ranks, topic_code)

import os
from os.path import isfile, join
from os import listdir

from BowDocCollection import BowDocCollection


def get_training_files(id, naked=False):
    """
    Get all training sets from file
    """
    folder = 'Training{id}'.format(id=id.replace("R", ""))
    path = os.path.join('..\\input\\dataset101-150\\{folder}'.format(folder=folder))

    # naked returns files as just directory name
    if naked:
        return [f for f in listdir(path) if isfile(join(path, f))]
    # returns files with relative path
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def calculate_bm25(collections, topic_statements):
    """
    Calculate the bm25 for the given collections
    """
    scores = {}
    # iterate over collections
    for collection, topic in zip(collections, topic_statements):
        id = topic["id"]
        title = topic["title"]

        # score
        score = collection.calculate_bm25(title)

        # append sorted score
        scores[id] = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
    return scores


def output_bm25(collections, topic_statements, bl):
    """
    Output bm25 results to file
    """
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"]

        # clean file
        path = '..\\output\\Training\\Training{topic}.dat'.format(topic=int(topic[2:]))
        if os.path.exists(path):
            os.remove(path)
        file = open(path, 'a')

        # output scores
        scores = bl[topic]
        for id, score in scores.items():
            file.write('{topic} {id} {result}\n'.format(topic=topic, id=id, result=score))


def output_bl_result(collections, topic_statements, bl):
    """
    Output bl results to file
    """
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"]

        # clean file
        path = '..\\output\\BLresults\\BLresult{topic}.dat'.format(topic=int(topic[2:]))
        if os.path.exists(path):
            os.remove(path)
        file = open(path, 'a')

        # output scores
        scores = bl[topic]
        for id, score in scores.items():
            file.write('{id} {score}\n'.format(id=id, score=score))


def calculate_w4(collections, topic_statements, benchmarks):
    """
    Calculate w4 results from given collections and benchmarks
    """
    ranks = {}
    # iterate over collections
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"]

        # calculate weight and rank
        weight = collection.calculate_w4(benchmarks[topic])
        rank = collection.calculate_rankings(weight)

        # append sorted rank to ranks
        ranks[topic] = dict(sorted(rank.items(), key=lambda item: item[1], reverse=True))
    return ranks


def output_lr_result(collections, topic_statements, lr):
    """
    Output lr results to file
    """
    # iterate over collection
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"]

        # clean file
        path = '..\\output\\LRresults\\LRresult{topic}.dat'.format(topic=int(topic[2:]))
        if os.path.exists(path):
            os.remove(path)
        file = open(path, 'a')

        # write ranks to file
        ranks = lr[topic]
        for id, rank in ranks.items():
            file.write('{id} {rank}\n'.format(id=id, rank=rank))
        file.close()


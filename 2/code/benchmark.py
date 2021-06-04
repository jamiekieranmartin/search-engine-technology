import os
from os.path import isfile, join
from os import listdir


def get_benchmark_files(naked=False):
    """
    Get all benchmarks from file
    """
    path = os.path.join('..\\input\\topicassignment101-150')

    if naked:
        return [f for f in listdir(path) if isfile(join(path, f))]
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def get_benchmarks():
    """
    Parse benchmarks into topic:[id:[value]]
    """
    benchmarks = {}
    for path in get_benchmark_files():
        file = open(path, 'r')
        id = "R" + path[-7:].replace(".txt", "")

        benchmark = {}
        for line in file.readlines():
            line = line.strip().split()
            benchmark[line[1]] = float(line[2])

        benchmarks[id] = benchmark
    return benchmarks

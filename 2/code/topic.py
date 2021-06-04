from BowDocCollection import BowDocCollection
from training import get_training_files


def get_topic_statements():
    """
    Get all topic statements from file
    """
    file = open('..\\input\\TopicStatements101-150.txt', 'r')

    topic_statements = []
    topic = {}

    # iterate over lines
    for line in file.readlines():
        line = line.strip()

        # num logic
        if line.startswith("<num>"):
            topic["id"] = line.replace("<num> Number:", "").strip()

        # title logic
        if line.startswith("<title>"):
            topic["title"] = line.replace("<title>", "").strip()

        # closing logic
        if line.startswith("</top>"):
            topic_statements.append(topic)
            topic = {}

    file.close()
    return topic_statements


def get_collections(topic_statements):
    """
    Get all collections from file
    """
    collections = []
    for topic in topic_statements:
        id = topic["id"]

        # get training files and generate collection
        training_files = get_training_files(id)
        collection = BowDocCollection(training_files)

        collections.append(collection)
    return collections

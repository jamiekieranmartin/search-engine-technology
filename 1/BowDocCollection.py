from XMLParser import XMLParser
from BowDoc import BowDoc
import math


class BowDocCollection:
    """
    BowDocCollection holds a collection of BowDocs
    """

    def __init__(self, files, stopWords):
        """
        Parses given files into a BowDocCollection
        :param files: []string, list of files to parse into BowDocs
        :param stopWords: []string, list of stopWords
        """
        # Initialise collection
        self.collection = {}
        self.totalDocLength = 0
        self.averageLength = 0

        # Iterate over files and parse contents
        for file in files:
            f = open(file, 'r')
            lines = f.read()
            parsed = XMLParser(lines)

            # Get BowDoc and add to collection
            doc = BowDoc(parsed, stopWords)
            self.collection[doc.getDocId()] = doc
            self.totalDocLength += doc.getDocLen()

            f.close()
        
        # Calculate average length of BowDoc collection
        self.averageLength = math.floor(self.totalDocLength/len(self.collection))

    def displayDocInfo(self):
        """
        Returns the displayDocInfo for each BowDoc
        :return:
        """
        collection_info = ''
        for doc in self.collection.values():
            collection_info += doc.displayDocInfo()
        return collection_info


    def calculate_df(self):
        """
        Calculate the df for a BowDocCollection
        :return: dict, term:df
        """
        df = {}
        for doc in self.collection.values():
            df = doc.calculate_df(df)

        sorted_df = dict(sorted(df.items(), key=lambda item: item[1], reverse=True))

        return sorted_df

    def calculate_tfidf(self):
        """
        Calculate the tf * idf for a BowDocCollection
        :return: dict, docId:(term:tfidf)
        """
        tfidf = {}
        df = self.calculate_df()

        for id, doc in self.collection.items():
            tfidf[id] = doc.calculate_tfidf(self.collection, df)
            tfidf[id] = dict(sorted(tfidf[id].items(), key=lambda item: item[1], reverse=True)[:10])

        return tfidf

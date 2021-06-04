# Jamie Martin
# N10212361
from stemming.stemming.porter2 import stem

from XMLParser import XMLParser
from BowDoc import BowDoc
from utils import get_common_english_words

common_english_words = get_common_english_words()


class BowDocCollection:
    """
    BowDocCollection holds a collection of BowDocs
    """

    def __init__(self, files):
        """
        Parses given files into a BowDocCollection
        :param files: []string, list of files to parse into BowDocs
        """
        # Initialise collection
        self.items = {}
        self.length = 0

        # Iterate over files and parse contents
        for file in files:
            f = open(file, 'r')
            lines = f.read()
            parsed = XMLParser(lines)

            # Get BowDoc and add to collection
            doc = BowDoc(parsed)
            self.length += doc.length
            self.items[doc.id] = doc
            f.close()

    def calculate_df(self):
        """
        Calculate the df for a BowDocCollection
        :return: [term]:[df]
        """
        df = {}
        for doc in self.items.values():
            for term in doc.terms:
                if term not in df:
                    df[term] = 0
                df[term] += 1

        sorted_df = dict(sorted(df.items(), key=lambda item: item[1], reverse=True))

        return sorted_df

    def calculate_bm25(self, query):
        """
        BM25 IR model for the document
        :return: []score
        """
        k = 1.2
        b = 0.75
        N = len(self.items)
        avg = int(self.length / N)
        df = self.calculate_df()
        query = [stem(item.lower()) for item in query.split(" ") \
                 if item.lower() not in common_english_words]

        scores = {}
        for id, doc in self.items.items():
            score = doc.calculate_bm25(query, df, avg, N, k, b)
            scores[id] = score
        return scores

    def calculate_w4(self, ben, theta=3.5):
        """
        Calculate w4 of the given collection
        """
        T = {}
        ntk = {}
        # select T from positive documents and r(tk)
        for id, doc in self.items.items():
            if ben[id] > 0:
                for term in doc.terms.keys():
                    if term not in T:
                        T[term] = 0
                    T[term] += 1

            # calculate n(tk)
            for term in doc.terms.keys():
                if term not in ntk:
                    ntk[term] = 0
                ntk[term] += 1

        # calculate N and R  
        N = len(self.items)
        R = 0
        for id in ben.keys():
            if ben[id] > 0:
                R += 1

        for id, rtk in T.items():
            T[id] = ((rtk + 0.5) / (R - rtk + 0.5)) / \
                    ((ntk[id] - rtk + 0.5) / (N - ntk[id] - R + rtk + 0.5))

            # calculate the mean of w4 weights.
        mean = 0
        for id, rtk in T.items():
            mean += rtk
        if len(T) > 0:
            mean = mean / len(T)

        # return features
        return {t: r for t, r in T.items() if r > mean + theta}

    def calculate_rankings(self, features):
        """
        Calculate rankings of the w4
        """
        ranks = {}
        for id, doc in self.items.items():
            for term in features.keys():
                if term in doc.terms:
                    if id not in ranks:
                        ranks[id] = 0
                    ranks[id] += features[term]
        return ranks

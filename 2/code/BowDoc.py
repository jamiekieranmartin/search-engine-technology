# Jamie Martin
# N10212361
from stemming.stemming.porter2 import stem
import math
import string

from utils import get_common_english_words

common_english_words = get_common_english_words()


class BowDoc:
    """
    BowDoc a Bag-of-Words Document
    """

    def __init__(self, parsed):
        """
        Initialises a BowDoc using a parsed XML node
        :param parsed: dict, parsed XML node
        """
        # Get newsitem node
        node = parsed.get_by_name("newsitem")[0]
        # Set DocID using itemid attribute
        self.id = node['attributes']['itemid']
        self.terms = {}

        # Get all <p> nodes
        nodes = parsed.get_by_name("p")

        # Parse <p> content into array of strings
        strings = []
        for node in nodes:
            line = node['content'].strip()
            line = line.translate(str.maketrans('', '', string.digits)).translate(
                str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
            strings += line.split()

        # try add terms from strings
        for s in strings:
            self.add_term(s)

        # set docLen to strings length
        self.length = len(strings)

    def add_term(self, term):
        """
        Attempt to add a term to terms dict
        :param term: string, the term or string
        """
        low = stem(term.lower())
        if len(low) > 2 and low not in common_english_words:
            if low not in self.terms:
                self.terms[low] = 0
            self.terms[low] += 1

    def calculate_tf(self):
        """
        Calculates term frequency for each term in the document
        :return: dict, term:tf
        """
        tf = {}
        for k, v in self.terms.items():
            tf[k] = v / self.length
        return tf

    def calculate_bm25(self, query, df, avg, N, k, b):
        """
        BM25 IR model for the document
        :return: score, number
        """
        score = 0
        qfs = {}

        get = lambda i, j: j[i] if i in j else 0

        for q in query:
            if q not in qfs:
                qfs[q] = 0
            qfs[q] += 1

            if q in self.terms:
                n = get(q, df)
                f = self.terms[q]
                K = k * ((1 - b) + b * (self.length / avg))
                qf = qfs[q]

                # s = math.log((N - n + 0.5) / (n + 0.5)) * (((k + 1) * f) / (K + f)) * (((100 + 1) * qf) / float(100 + qf))
                # print(math.log((N - n + 0.5) / (n + 0.5)))
                # print(math.log(1.0 / ((n + 0.5) / (N - n + 0.5)), 2))

                s = math.log(1.0 / ((n + 0.5) / (N - n + 0.5)), 2) * (((k + 1) * f) / (K + f)) * (((100 + 1) * qf) / float(100 + qf))
                score += s
                # print(avg, N, K, b, q, n, f, K, qf, s)

        return score

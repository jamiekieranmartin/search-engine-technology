# Jamie Martin
# N10212361
from stemming.stemming.porter2 import stem
import math
import string


class BowDoc:
    """
    BowDoc a Bag-of-Words Document
    """

    def __init__(self, parsed, stopWords):
        """
        Initialises a BowDoc using a parsed XML node
        :param parsed: dict, parsed XML node
        :param stopWords: []string, list of stopWords
        """
        # Get newsitem node
        node = parsed.get_by_name("newsitem")[0]
        # Set DocID using itemid attribute
        self.docID = node['attributes']['itemid']
        self.terms = {}
        self.docLen = 0

        # Get all <p> nodes
        nodes = parsed.get_by_name("p")
        
        # Parse <p> content into array of strings
        strings = []
        for node in nodes:
            line = node['content'].strip()
            line = line.translate(str.maketrans('', '', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            strings += line.split()
        
        # try add terms from strings
        for s in strings:
            self.addTerm(stopWords, s)

        # set docLen to strings length
        self.setDocLen(len(strings))

    def addTerm(self, stopWords, term):
        """
        Attempt to add a term to terms dict
        :param term: string, the term or string
        """
        low = stem(term.lower())
        if len(low) > 2 and low not in stopWords:
            if low not in self.terms:
                self.terms[low] = 0
            self.terms[low] += 1
            
    def getDocId(self):
        """
        DocID Getter
        :return: string, docID
        """
        return self.docID

    def getDocLen(self):
        """
        Document Length Getter
        :return: int, length
        """
        return self.docLen

    def setDocLen(self, l):
        """
        Document length Setter
        :param l: int, length
        """
        self.docLen = l

    def displayDocInfo(self):
        """
        Displays and returns the Document Info
        :return: string, formatted document info
        """
        body = 'Doc {docID} contains {count} terms and has {words} words.\n'.format(docID=self.docID, count=len(self.terms), words=self.docLen)

        # Get term and count from sorted self.terms
        for term, count in sorted(self.terms.items(), key=lambda item: item[0], reverse=True):
            body += '{term}, {count}\n'.format(term=term, count=count)   
        body += '\n'

        print(body)
        return body

    def calculate_df(self, df={}):
        """
        Calculates document frequency for each term in the document, adding to the given df dict
        :param df: dict, term:df
        :return: dict, term:df updated
        """
        for term in self.terms:
            if term not in df:
                df[term] = 0
            df[term] += 1
        return df

    def calculate_tf(self):
        """
        Calculates term frequency for each term in the document
        :return: dict, term:tf
        """
        tf = {}
        for k, v in self.terms.items():
            tf[k] = v / self.docLen
        return tf

    def calculate_idf(self, collection, df):
        """
        Calculates idf for each term in the document
        :return: dict, term:idf
        """
        idf = {}
        for k in self.terms:
            idf[k] = math.log(len(collection) / df[k])
        return idf

    def calculate_tfidf(self, collection, df):
        """
        Calculates tfidf for each term in the document
        :return: dict, term:tfidf
        """
        tf = self.calculate_tf()
        idf = self.calculate_idf(collection, df)
        tfidf = {}
        for term in tf:
            tfidf[term] = tf[term] * idf[term]
        return tfidf

    def gi(self, df, q, N, R=0, r=0):
        """
        the query feature function
        :return: result, number
        """
        n = df[q]
        return math.log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))

    def fi(self, tf, avg, q, k1=1.2, b=0.75):
        """
        the document feature function
        :return: result, number
        """
        K = k1 * ((1 - b) + b * (self.docLen / avg))
        f_i = tf[q]
        return ((k1 + 1) * f_i) / (K + f_i)

    def BM25(self, df, q, N, avg):
        """
        BM25 IR model for the document
        :return: score, number
        """
        tf = self.calculate_tf()
        scores = 0
        q = [stem(item.lower()) for item in q.split(" ")]

        for query in q:
            if query in tf:
                scores += (self.gi(df, query, N) + self.fi(tf, avg, query))
        return scores
# Jamie Martin
# N10212361
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
            id = doc.getDocId()
            self.collection[id] = doc
            docLen = doc.getDocLen()
            self.totalDocLength += docLen

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

    def docLen(self):
        """
        Calculates the docLen for each document
        """
        body = 'Total Doc Length: {length}\n\n'.format(length=self.totalDocLength)
        body += "Docs:\n"

        for id, doc in self.collection.items():
            body += '{docID}: {length}\n'.format(docID=id, length=doc.getDocLen())

        body += '\nAverage Doc Length: {length}'.format(length=self.averageLength)
        return body

    def query(self, query):
        """
        Calculate the query for each document
        """
        df = self.calculate_df()
        avg = self.averageLength
        N = len(self.collection)
        best = []
        body = 'Average document length {length} for query: {query}\n'.format(length=avg, query=query)
        for id, doc in self.collection.items():
            score = doc.BM25(df, query, N, avg)
            if score is not 0:
                best.append({ 'id': id, 'score': score })
            body += 'Document: {docID}, Length: {length} and BM25 Score: {score}\n'.format(docID=id, length=doc.getDocLen(), score=score)

        body += '\nFor the query "{query}", three recommended relevant documents and their BM25 scores:\n'.format(query=query)
        i = 0
        for b in sorted(best, key=lambda k: k['score'], reverse=True):
            if i < 3:
                body += '{docID}: {score}\n'.format(docID=b['id'], score=b['score'])
            i += 1
        
        return body
# Import all libraries
import os
import string
import math
import copy
from BowDoc import BowDoc
from stemming.porter2 import stem


class List_BowDoc:
    # Document-frequency dictionary of all BowDoc
    df = {}
    topicID = ""

    # Linked list constructor
    def __init__(self):
        self.head = None

    def insert(self, nnode):
        """Insert a new node into the current linked list
        """
        # Temp value to hold the new node
        temp_node = nnode

        # If linkedlist is empty, init a new Head
        if self.head is None:
            self.head = temp_node
            return

        # Last one of the linkedlist is head
        last = self.head
        # Get the last node of the ll
        while (last.next):
            last = last.next
        # Point the last node to the new one
        last.next = temp_node
    # Give a BowDoc LinkedList a topic code

    def createTopicCode(self, code):
        self.topicID = code
    # Get the BD LinkedList's topic code

    def getTopicCode(self):
        return self.topicID

    def getLength(self):
        """Calculate the linked list's length and return it

        Return:
        int: Linked list's length 

        """
        curr = self.head
        count = 0
        while (curr):
            count += 1
            curr = curr.next

        return count

    def getDicById(self, ID):
        """ Get a BowDoc with matched ID

        Parameter:
        ID(string): docID of the BowDoc user wants to find. 

        Return:
        BowDoc: the BowDoc with the same ID
        """
        curr = self.head
        while (curr):
            if (curr.docID == ID):
                return curr
            curr = curr.next

    def getDocIDs(self):
        """ Get all the BowDOc from the linked list
        """

        curr = self.head
        i = 1
        while (curr):
            print("docID", i, ": ", curr.docID)
            i = i + 1
            curr = curr.next

    # With a given docID, display all the info
    def displayDocInfo(self, givenID):
        """ Display all the BowDoc's info given docID

        Parameter:
        givenID(string): docID of the BowDoc user wants to find
        """
        curr = self.head
        while (curr):
            if (curr.docID == givenID):
                curr.displayDocInfo()
                break
            curr = curr.next

    def calculate_df(self):
        """Calculates term-frequency for each term in the documents

        Return:
        dict (terms: count) - A dictionary for each term and its count value.
        """
        # Init curr as the first node of the linkedlist
        curr = self.head
        while (curr):
            # If there is no dictionary yet, copy the first 1
            if not self.df:
                self.df = copy.deepcopy(curr.terms)
                # Reset all count values to 1
                for i in self.df.keys():
                    self.df[i] = 1
            else:
                # Loop through all keys of the current term and increase / add accordingly to the main frequency-dictionary.
                for i in curr.terms.keys():
                    if i in self.df:
                        self.df[i] += 1
                    else:
                        self.df[i] = 1
            # Get the next node
            curr = curr.next
        return self.df

    def doclen(self):
        """Calculates the total length of a list of BowDoc

        Return:
        int - Total length of the list of BowDoc 
        """
        curr = self.head
        total_length = 0
        while(curr):
            total_length += curr.getDocLen()
            curr = curr.next
        return total_length

    def calculate_avdl(self):
        """ Calculate the average length of the documents

        Return:
        int -  documents' average length
        """
        return int(self.doclen() / self.getLength())

    def print_length(self):
        """Print the average length, and then print the length of each document
        """
        curr = self.head
        average_length = self.calculate_avdl()
        print("Average document's length: ", average_length)
        while (curr):
            print("Doc ID ", curr.docID, "has length of ", curr.getDocLen())
            curr = curr.next

    # Task 3.3 + 3.4
    def calculate_BM(self, n, N, f, k1, k, qf):
        """ Calculate BM25 score with given arguments

        Parameters:
        n(int) - Number of times the term appeared in N documents
        N(int) - total number of documents
        f(int) - Number of time the term appeared in the current document
        k1(double) - Default value 1.2
        k(double) 
        qf - Query frequency
        Return:
        double: BM25 score of the current query

        """
        # Calculate log part
        res1 = math.log((N-n+0.5)/(n+0.5))
        # Calculate middle part
        res2 = ((k1+1)*f) / (k+f)
        res3 = (((100 + 1) * qf) / float(100 + qf))
        return res1*res2*res3

    def BM25(self, query, general_dictionary):
        """
        Perform ranking using BM25 IR model

        Parameters:
        query(string) - The query to rank the documents
        general_dictionary(dict) - The document-frequency dictionary
        """

        # Get the list of stop words
        txtFile = open("common-english-words.txt")
        txtContent = txtFile.read()
        stop_words = txtContent.split(',')
        txtFile.close()

        # Split the query into an array
        query_split = query.split()

        # Variables for calculating BM25
        k1 = 1.2
        k2 = 100
        b = 0.75
        N = self.getLength()
        avglen = self.calculate_avdl()
        result = 0

        # Get the first element of linked list
        curr = self.head

        # Dictionary to save the result according to the document ID
        BM_dict = {}
        # Loop through each bowDoc
        while curr:
            # Result is the BM_25 score
            result = 0
            qfs = {}
            for i in query_split:
                # Convert the query word to lower case
                query_lower = stem(i.lower())
                try:
                    qfs[query_lower] += 1
                except KeyError:
                    qfs[query_lower] = 1

                BM_result = 0
                # If the term is not in stop_words then continue
                if i not in stop_words:
                    # Get the frequency of the term in all documents
                    n = general_dictionary.get(query_lower, 0)

                    # Get the frequency of the term in current document
                    f = curr.terms.get(query_lower, 0)

                    # Get qf
                    qf = qfs[query_lower]

                    # Length portion is the current doc_len divide by average length
                    length_portion = curr.getDocLen() / avglen

                    # Calculate K base on k1,b and length_portion
                    k = k1*((1-b)+b*length_portion)

                    # Perform calculating BM25 score
                    BM_result = self.calculate_BM(
                        n, N, f, k1, k, qf)
                    # Add the current term's score to the final result
                    result += BM_result
            # Add the value to the corresponding ID
            BM_dict[curr.docID] = result

            # Go to next element
            curr = curr.next

        # Sort the dictionary by values

        BM_dict = sorted(
            BM_dict.items(), key=lambda item: item[1], reverse=True)

        return BM_dict

    def w4(self, ben, theta):
        """ Calculating w4 and return a Feature dict

        Parameters:
        ben(dict) - Benchmark dictionary
        theta(float) - Default value is 3.5

        """
        curr = self.head
        T = {}
        while curr:
            if ben[curr.docID] > 0:
                for term, freq in curr.terms.items():
                    try:
                        T[term] += 1
                    except KeyError:
                        T[term] = 1
            curr = curr.next

        # Calculate n(tk)

        ntk = {}
        curr = self.head

        while curr:
            for term in curr.get_term_list():
                try:
                    ntk[term] += 1
                except KeyError:
                    ntk[term] = 1
            curr = curr.next

        # Calculate N and R
        No_docs = self.getLength()

        R = 0
        for id, fre in ben.items():
            if ben[id] > 0:
                R += 1

        for id, rtk in T.items():
            T[id] = ((rtk+0.5) / (R-rtk + 0.5)) / \
                ((ntk[id]-rtk+0.5)/(No_docs-ntk[id]-R+rtk + 0.5))

        # calculate the mean of w4 weights.
        meanW4 = 0
        for id, rtk in T.items():
            meanW4 += rtk

        if len(T) > 0:
            meanW4 = meanW4/len(T)

        # Features selection
        Features = {t: r for t, r in T.items() if r > meanW4 + theta}
        return Features

    def bm25Testing(self, features):
        ranks = {}
        curr = self.head
        while curr:
            id = curr.getDocID()
            for term in features.keys():
                if term in curr.get_term_list():
                    try:
                        ranks[id] += features[term]
                    except KeyError:
                        ranks[id] = features[term]
            curr = curr.next
        print("ranks")
        print(ranks)
        return ranks

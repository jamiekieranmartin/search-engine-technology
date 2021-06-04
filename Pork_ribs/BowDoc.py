import os
import string
import math
import copy

# BowDoc class


class BowDoc:

    # Constructor for BowDoc class
    def __init__(self, docID, terms, next=None):
        self.docID = docID
        self.terms = terms
        self.doc_len = 0
        self.next = next

    # Accessor of doc_len
    def getDocLen(self):
        return self.doc_len

    # Mutator of doc_len
    def setDocLen(self, val):
        self.doc_len = val

    # Accessor of docID
    def getDocID(self):
        return self.docID

    def addTerm(self, newTerm):
        """Add new term to dictionary or increase the frequency

        Parameter:
        newTerm(string) - the term to add to dictionary or increase frequency.
        """
        try:
            # If exist, increase the frequency
            self.terms[newTerm] += 1
        except:
            # Else create new key and made the frequency 1
            KeyError
            self.terms[newTerm] = 1

    def displayDocInfo(self):
        """Display information of the BoWDoc.
        """
        print("Doc ", self.docID, "contains", len(self.terms),
              "terms and", self.getDocLen(), "words.")
        # Loop through the terms dict
        for i in self.terms.items():
            print(i[0], ":", i[1])

    def displaySorted(self, output_file):
        """Print the information of each BowDoc, with the dictionary got sorted descending into a file

        Parameter:
        output_file(string) - The filename for output file
        """

        # Open the new file
        f = open(output_file, 'a')

        txt1 = "Doc {docID} contains {term_counts} terms and {doc_len} words.\n".format(
            docID=self.docID, term_counts=len(self.terms), doc_len=self.getDocLen())
        f.write(txt1)

        # Print the term and frequency in descending order
        for i in sorted(self.terms.items(), key=lambda item: item[1], reverse=True):
            txt2 = "{term}: {count}\n".format(term=i[0], count=i[1])
            f.write(txt2)
        f.close()

    def get_term_list(self):
        """Get sorted list of all terms occurring in the document."""
        return sorted(self.terms.keys())

import os
import string
from stemming.porter2 import stem
from BowDoc import BowDoc
from List_BowDoc import List_BowDoc


def parse_doc(input, stops):
    """ Parse the document to get the dictionary

    Parameters:
    input(string) - Input file name
    stops(string) - Stop-words' file name

    Return 
    BowDoc - A new BowDoc contains the current file docID and its ictionary
    """
    # Read bag of words file and get all the content
    txtFile = open(stops)
    txtContent = txtFile.read()
    stop_words = txtContent.split(',')
    txtFile.close()

    # Read XML file and get all the content
    xmlFile = open(input)
    xmlContent = xmlFile.read()
    lines = xmlContent.split('\n')
    xmlFile.close()

    # Get itemID
    itemid = ""
    # Variable to count the number of words
    doc_len = 0
    # Variable to check if we should perform tokenize or not
    tokenize = False
    # Init new BoW object
    newBoW = None

    # Iterate line by line to tokenize the file
    for line in lines:
        # Find the position of the text '<text>' in the line
        if line.find("itemid") != -1:
            itemid = line.split("=")[1].split("\"")[1]
            newBoW = BowDoc(itemid, {})
        else:
            pos = line.find('<text>')
            # If <text> exists, start tokenize after this line
            if pos != -1:
                tokenize = True
                continue
            else:
                # Else check if it's </text>,finish tokenize
                if line.find('</text>') != -1:
                    tokenize = False
                    break

            if tokenize:
                # Preprocess text
                line = line.strip()
                line = line.replace('<p>', '').replace('</p>', '')
                line = line.translate(str.maketrans('', '', string.digits)).translate(
                    str.maketrans(string.punctuation, ' '*len(string.punctuation)))

                # Find terms and call addTerm
                for i in line.split():
                    doc_len += 1
                    term = i.lower()
                    term = stem(term)
                    if len(term) > 2 and term not in stop_words:
                        newBoW.addTerm(term)
    # Assign doc_len to the BoW doc
    newBoW.setDocLen(doc_len)

    return newBoW

# Function to perform the task 1 solver


def getBDList():
    """ Generate a list of BowDoc

    Return:
    List_BowDoc - A linked list of all BowDocs
    """
    # Get directory name
    directory = "dataset101-150"
    # Stop file's name
    stops_file = "common-english-words.txt"
    # Init an empty BowDoc Linked List
    BDList = List_BowDoc()

    # Delete the file if exists.
    if os.path.exists('HieuNghiaHuynh_Q1.txt'):
        os.remove('HieuNghiaHuynh_Q1.txt')

    # Loop through each files in the directory which ends in xml
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('xml'):
                # fname = directory + "/" + subdir + "/" + filename
                print(subdir)
                fname = os.path.join(subdir, filename)
                # Perform parse doc to get the dictionary
                item = parse_doc(fname, stops_file)
                # Print to file in sorted order ( sort descending base on the frequency)
                item.displaySorted()
                # Insert the BowDoc into BowDoc list
                BDList.insert(item)
    return BDList


def getTrainingData(topic_code):
    """ Generate a list of BowDoc
    Parameters:
    topic_code: The topic number 

    Return:
    List_BowDoc - A linked list of all BowDocs
    """
    # Get directory name
    directory = "dataset101-150"
    # Stop file's name
    stops_file = "common-english-words.txt"
    # Init an empty BowDoc Linked List
    BDList = List_BowDoc()

    # Loop through each files in the directory which ends in xml
    for subdir, dirs, files in os.walk(directory):
        if ((subdir[-3:] == topic_code[-3:]) & (subdir.find('Training') != -1)):
            for filename in files:
                if filename.endswith('xml'):
                    # fname = directory + "/" + subdir + "/" + filename
                    fname = os.path.join(subdir, filename)
                    # Perform parse doc to get the dictionary
                    item = parse_doc(fname, stops_file)
                    # Print to file in sorted order ( sort descending base on the frequency)
                    # item.displaySorted('training.txt')
                    # Insert the BowDoc into BowDoc list
                    BDList.insert(item)
            break
    return BDList


if __name__ == '__main__':
    result = getTrainingData('R102')
    print("hello")
# result.getDocIDs()

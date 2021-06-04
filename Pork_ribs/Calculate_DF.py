import os


def getdf(result1):
    """ Generate document_frequency dictionary

    Parameters:
    result1(List_BowDoc)

    Return
    dict (terms: frequency) - A document-frequency dictionary for all documents
    """
    # Task 2.1
    # Get length of the dictionary
    n = result1.getLength()

    # Call out function to calculate the term frequency
    res = result1.calculate_df()

    # Delete the file if exists.
    # if os.path.exists('HieuNghiaHuynh_Q2_1.txt'):
    #     os.remove('HieuNghiaHuynh_Q2_1.txt')

    # Open and write to the file
    # new_fo = open('HieuNghiaHuynh_Q2_1.txt', 'a')
    # txt = "There are {numDoc} documents in this data set and contains {y} terms.\n".format(
    #     numDoc=n, y=len(res))
    # new_fo.write(txt)

    # Print out the result in descending order
    # for i in sorted(res.items(), key=lambda item: item[1], reverse=True):
    #     txt2 = "{term}: {count}\n".format(term=i[0], count=i[1])
    #     new_fo.write(txt2)
    # new_fo.close()

    # Task 2.2

    # Delete the file if exists.
    # if os.path.exists('HieuNghiaHuynh_Q2_2.txt'):
    #     os.remove('HieuNghiaHuynh_Q2_2.txt')

    # Call out function to calculate the tf*idf of docID 741299
    # result1.calculate_all_weight()

    # Return a dictionary of document-frequency
    return res

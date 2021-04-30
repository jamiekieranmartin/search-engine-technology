# Jamie Martin
# N10212361
from BowDocCollection import BowDocCollection
from os.path import isfile, join
from os import listdir


def write_to_file(file, body):
    """
    Opens file, writes body to it, and then close file
    """
    file = open(join('./output', file), 'w')
    file.write(body)
    file.close()


if __name__ == "__main__":
    # --- SETUP ---

    # Get stop words list
    file = open('./common-english-words.txt', 'r')
    stopWords = file.read().split(',')
    file.close()

    # Get files list for parsing
    _dir = './input'
    files = [join(_dir, f) for f in listdir(_dir) if isfile(join(_dir, f))]

    # --- Q1 ---

    print('\n--- Q1 ---\n')

    collection = BowDocCollection(files, stopWords)
    collection_info = collection.displayDocInfo()
    write_to_file('jamie_martin_Q1.txt', collection_info)

    # --- Q2_1 ---

    print('\n--- Q2_1 ---\n')

    df = collection.calculate_df()
    
    body = 'There are {docCount} documents in this data set and contains {terms} terms.\n'.format(docCount=len(collection.collection), terms=len(df))
    for term, count in df.items():
        body += '{term}: {count}\n'.format(term=term, count=count)

    print(body)
    write_to_file('jamie_martin_Q2_1.txt', body)

    # --- Q2_2 ---

    print('\n--- Q2_2 ---\n')

    tfidf = collection.calculate_tfidf() 

    body = ''
    for id, doc_tfidf in tfidf.items():
        body += 'Document {docId} contains {terms} terms.\n'.format(docId=id, terms=len(collection.collection[id].terms))
        for term, value in doc_tfidf.items():
            body += '{term}: {value}\n'.format(term=term, value=value)
        body += '\n'

    print(body)  
    write_to_file('jamie_martin_Q2_2.txt', body)

    # --- Q3_1 ---

    print('\n--- Q3_1 ---\n')
    body = """
# Default Variables

qf = 1
k1 = 1.2
k2 = 100
b = 0.75
R = 0 
r = 0 

# Note

- R and r are equal to zero as there is no relevance information

- As k2 = 100 and qf = 1, the third section of the formula can be calculated as such: (100+1)*1 / (100+1) = 101 / 101 = 1

# gi

gi is the query feature function. Here we utilise and calculate:

    - ni, the frequency of the query term in all documents

    - N, the total number of documents

# fi

fi is the document feature function. Here we utilise and calculate:

    - fi, the frequency of the term in the current document

    - K, the K base, comprises of:

        - the average length of all documents

        - the current documents length

    """
    write_to_file("jamie_martin_Q3_1.txt", body)
   
    # --- Q3_2 ---

    print('\n--- Q3_2 ---\n')

    body = collection.docLen()
    print(body)
    write_to_file("jamie_martin_Q3_2.txt", body)

    # --- Q3_3 ---

    print("\n--- Q3_3 ---\n")

    query = "This British fashion"
    body = collection.query(query)
    print(body)
    write_to_file("jamie_martin_Q3_3.txt", body)

    # --- Q3_4 ---
    
    body = collection.query("This British fashion")
    body += "\n"
    body += collection.query("All fashion awards")
    body += "\n"
    body += collection.query("The stock markets")
    body += "\n"
    body += collection.query("The British-Fashion Awards")
    write_to_file("jamie_martin_Q3_4.txt", body)


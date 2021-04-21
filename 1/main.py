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

    print('--- Q1 ---')

    collection = BowDocCollection(files, stopWords)
    collection_info = collection.displayDocInfo()
    write_to_file('jamie_martin_Q1.txt', collection_info)

    # --- Q2_1 ---

    print('--- Q2_1 ---')

    df = collection.calculate_df()
    
    body = 'There are {docCount} documents in this data set and contains {terms} terms.\n'.format(docCount=len(collection.collection), terms=len(df))
    for term, count in df.items():
        body += '{term}: {count}\n'.format(term=term, count=count)

    print(body)
    write_to_file('jamie_martin_Q2_1.txt', body)

    # --- Q2_2 ---

    print('--- Q2_2 ---')

    tfidf = collection.calculate_tfidf() 

    body = ''
    for id, doc_tfidf in tfidf.items():
        body += 'Document {docId} contains {terms} terms.\n'.format(docId=id, terms=len(collection.collection[id].terms))
        for term, value in doc_tfidf.items():
            body += '{term}: {value}\n'.format(term=term, value=value)
        body += '\n'

    print(body)  
    write_to_file('jamie_martin_Q2_2.txt', body)
   
    # --- Q3 ---

    print('--- Q3 ---')

    print("Total Doc Length:", collection.totalDocLength)

    print("\nDocs:")

    for id, doc in collection.collection.items():
            print('{docID}: {length}'.format(docID=id, length=doc.getDocLen()))

    print("\nAverage Doc Length:", collection.averageLength)

    df = collection.calculate_df()

    query = ["British", "fashion"]
    print("\nBM25 Query:", query)
    for id, doc in collection.collection.items():
        score = doc.BM25(collection, df, query)
        print('{docID}: {score}'.format(docID=id, score=score))

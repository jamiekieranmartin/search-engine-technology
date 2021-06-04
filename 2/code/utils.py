

def get_common_english_words():
    """
    Get all common English words from file
    """
    file = open('..\\input\\common-english-words.txt', 'r')
    common_english_words = file.read().split(',')
    file.close()
    return common_english_words
def find(word, words_iter):
    """An Elasticsearch killer
    
    Args:
    word (str): word to fuzzy find in given words_iter
    words_iter (iterable): many words to search within

    Returns:
    (str) one of words_iter that best matches given word
    """
        return max((w for w in words_iter if len(w)<=(len(word)+1)), key=lambda x: len(set(x).intersection(word)))

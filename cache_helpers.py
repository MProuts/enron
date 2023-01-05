def _cache_file_path(word):
    word = _encode(word)
    word_path = '/'.join([*word])
    return f"cache/{word}.csv"

def _encode(word):
    return word.lower().replace("/", "|")

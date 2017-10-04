import string
from collections import defaultdict

def word_count(text):
    text = text.lower()
    result = {}

    for char in string.punctuation:
        text = text.replace(char, ' ')

    for word in text.split():
        if word not in result:
            result[word] = 0
        result[word] += 1
    return result


def word_count_better(text):
    text = text.lower()
    result = defaultdict(int)

    for char in string.punctuation:
        text = text.replace(char, ' ')

    for word in text.split():
        result[word] += 1
    return result


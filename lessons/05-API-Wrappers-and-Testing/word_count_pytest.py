import pytest

from word_count import word_count

def test_count_one_word():
    assert {'word': 1} ==  word_count('word')

def test_count_one_of_each():
    expected = {'one': 1, 'of': 1, 'each': 1}
    result = word_count('one of each')
    
    assert expected == result

def test_count_multiple_occurences():
    expected = {'one': 1, 'fish': 4, 'two': 1, 'red': 1, 'blue': 1}
    result = word_count('one fish two fish red fish blue fish')

    assert expected == result


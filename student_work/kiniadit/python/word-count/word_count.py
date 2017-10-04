import re
def word_count(words):
	# replace all punctuations with whitespaces 
    words = re.sub('[_\W]+',' ',words)
    # convert to uppercase, remove all trailing whitespaces
    # and then split into an array
    word_array = words.lower().strip().split()
    # get unique elements by converting into a set
    output = {}
    for word in set(word_array):
	    output[word] = word_array.count(word)
    return output

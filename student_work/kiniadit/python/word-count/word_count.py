import re
def word_count(word):
	# replace all punctuations with whitespaces 
    word = re.sub('[_\W]+',' ',word)
    # convert to uppercase, remove all trailing whitespaces
    # and then split into an array
    word_array = word.lower().strip().split()
    # get unique elements by converting into a set
    output = {}
    for word in set(word_array):
	    output[word.lower()] = word_array.count(word)
    return output

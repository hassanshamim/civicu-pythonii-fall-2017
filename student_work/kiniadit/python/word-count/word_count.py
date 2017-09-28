import re
def word_count(word):
	# replace all punctuations with whitespaces 
    word = re.sub('[_\W]+',' ',word)
    # convert to uppercase, remove all trailing whitespaces
    # and then split into an array
    word_array = word.upper().strip().split()
    # get unique elements by converting into a set
    word_array_unique = list(set(word_array))
    output = {}
    for x in range(0,len(word_array_unique)):
	    output[word_array_unique[x].lower()] = word_array.count(word_array_unique[x].upper())
    return output

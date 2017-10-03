import re

# Count the words in a string. Return a dictionary with the word as
# the key and the number of ocurrences of the word as the value. Words
# are separated by whitespace or punctuation and are case insensitive.
#
# for example:  word_count("apple apple_orange,Apple-OrAnGe")
# would return: {"apple:3, orange:2"}
#

def word_count(text):
    
    # Replace all punctuation with whitespace.
    # Literally, replace any "non-word" characters (\W) or underscores (_) with a blank space
    text = re.sub('[\W_]', ' ', text)

    # Set all characters to lowercase for case insensitive comparisons
    text = text.lower()

    # Split the text on whitespace into a list of words
    split_text = text.split()

    #
    # Create a dictionary of word occurrence counts
    # {<word>:<occurrences of word in input text>}
    #

    # Initialize the empty dictionary
    result = {}

    # Loop through each word in the text
    for word in split_text:
        # Check if this is the first occurrence of the string
        if word not in result:
            # This is the first occurrence, add to the dictionary
            result[word] = 1
        else:
            # This is a repeat occurrence, increment the occurrence count
            result[word] += 1

    return result


#print (word_count('a,b,a,c'))

import string

def is_isogram(input_text):
    input_text = input_text.lower()
    for letter in input_text:
        if letter in string.whitespace: continue
        if letter == '-': continue
        if input_text.count(letter) > 1: return False
    
    return True

print (is_isogram("letter"))

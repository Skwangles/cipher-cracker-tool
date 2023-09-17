import nltk
from nltk.corpus import words 

def index_of_coincidence(input):
    """Calculates the IoC"""

    if not input.isalpha():
        print("Called IoC on non-alpha string")
        return None

    # Sum occurances of letters
    letters = {}
    for i in input:
        if i in letters:
            letters[i] += 1
        else:
            letters[i] = 1

    # Calculate using algorithm from class
    sigma_f = 0
    for f in letters.items():
        sigma_f += f*(f - 1)
    big_n = len(input)
    return sigma_f/(big_n * (big_n - 1))


#store the set of words globally so we dont have to spend ages getting them each time
english_words = None 

def get_english_percent(input):
    """Calculates the percentage of english words in a text"""

    if not input:
        print("Missing input text to calculate english word %")
        return None

    #if our global set of english words isnt available yet, go get them
    global english_words
    if not english_words:
        try:
            nltk.data.find('corpora/words.zip')
        except LookupError:
            nltk.download('words')

        english_words = set(words.words())
    

    input_words = input.split()    
        
    #search our text for english words
    english_word_count = sum(1 for word in input.split() if word.lower() in english_words)
    return round((english_word_count / len(input_words)) * 100, 2)
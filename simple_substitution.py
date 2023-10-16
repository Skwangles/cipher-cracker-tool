import random
import string
from alive_progress import alive_bar
from utils import *
from nltk.corpus import words 

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_empty():
    
    return {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': [],
        'G': [],
        'H': [],
        'I': [],
        'J': [],
        'K': [],
        'L': [],
        'M': [],
        'N': [],
        'O': [],
        'P': [],
        'Q': [],
        'R': [],
        'S': [],
        'T': [],
        'U': [],
        'V': [],
        'W': [],
        'X': [],
        'Y': [],
        'Z': []
        }



english_words = None

if not english_words:
    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        nltk.download('words')

    english_words = set(words.words())

word_patterns = {}


def get_pattern_of_unique(word):
    letters = {}
    output = ""
    num = 0
    separator = "|"
    for letter in word:
        if letter not in letters:
            num += 1
            letters[letter] = num
        output += separator + str(letters[letter]) # e.g. "1|2|3|4..."
    return output



#Generate key if one is not supplied
def generate_key():
    alphabet = list(string.ascii_lowercase)
    shuffled = random.sample(alphabet, len(alphabet))
    return dict(zip(alphabet, shuffled))


def encrypt(text, key):
    """Encrypt the plain text using the key"""
    if not text:
        return "Missing required arguments for this function"
    
    alphabet = get_alphabet()
    
    text = text.upper()
    key = key.upper()

    # Validate the key
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Key must be a permutation of the English alphabet")

    encrypted_text = ""
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            encrypted_text += key[index]
        else:
            encrypted_text += char

    return encrypted_text


def decrypt(cypher_text, key):
    """Decrypts the cypher text using the key"""
    if not cypher_text:
        return "Missing required arguments for this function"
    
    alphabet = get_alphabet()
    
    cypher_text = cypher_text.upper()
    key = key.upper()

    # Validate the key
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Key must be a permutation of the English alphabet")

    decrypted_text = ""
    for char in cypher_text:
        if char in key:
            index = key.index(char)
            decrypted_text += alphabet[index]
        else:
            decrypted_text += char

    decrypted_text = decrypted_text.lower()

    return decrypted_text

def crack(cypher_text):
    """Cracks the cypher text, returning the key"""       
    if not cypher_text:
        return "Missing required arguments for this function"    
    
    # Frequency order
    english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    mapping = get_empty()
    
    
    cypher_text = cypher_text.upper().replace("[^A-Z\s]", "")
    
    # first pass - find words that could match each 'word' in the cypher text
    encrypted_words = cypher_text.split(" ")
    
    # check longest words first as they have the most information
    encrypted_words = sorted(encrypted_words, key=len, reverse=True)
    
    for c_word in encrypted_words:
        pattern = get_pattern_of_unique(c_word)
        
        if pattern not in word_patterns:
            continue
        
        if len(word_patterns[pattern]) == 1:
            # we have found the word, so add it to the mapping
            for i in range(len(c_word)):
                mapping[c_word[i]] = [word_patterns[pattern][0][i]]
            continue
        
        single_word_map = get_empty()
        with alive_bar(len(word_patterns[pattern])) as bar:
            for possible_word in word_patterns[pattern]:
                for i in range(len(c_word)):
                    if c_word[i] in single_word_map:
                        letter = possible_word[i]
                        if letter not in single_word_map[c_word[i]]:
                            single_word_map[c_word[i]].append(letter)
                bar()
        mapping = addGuessesToMap(mapping, single_word_map)
    
    mapping = collapse_solved_letters(mapping)
    print(mapping)
    
    decrypted = ""
    for letter in cypher_text:
        if letter.upper() in mapping:
            if len(mapping[letter.upper()]) > 1 or len(mapping[letter.upper()]) == 0:
                decrypted += "*"
            else:
                decrypted += mapping[letter.upper()][0]
        else:
            decrypted += letter

    return decrypted


def collapse_solved_letters(mapping):
    unsolved_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with alive_bar(len(unsolved_letters)) as bar:
        while unsolved_letters and any(len(mapping[letter]) == 1 for letter in unsolved_letters):
            letters_with_1 = [letter for letter in unsolved_letters if len(mapping[letter]) == 1]
            
            for letter in letters_with_1:
                if len(mapping[letter]) != 1:
                    continue
                
                bar()
                
                solved_letter = mapping[letter][0]
                
                unsolved_letters = unsolved_letters.replace(letter, "")
                
                # remove solved letter from all other mappings
                for key in unsolved_letters:
                    if key == letter:
                        continue
                    
                    if solved_letter in mapping[key]:
                        mapping[key].remove(solved_letter) 
    return mapping
    

def count_of_items_with_1(mapping):
    count = 0
    for key in mapping:
        if len(mapping[key]) == 1:
            count += 1
    return count
            
def check_if_any_match(mapping, letter, others_with_1):
    output = []
    for other in others_with_1:
        if letter in mapping[other]:
            output.append(other)
    return output
    
def addGuessesToMap(root_map, single_map):
    """Reduces the root_map to only contain letters that are in both root_map and single_map"""
    intersection = get_empty()
    for key in root_map:
        if key not in single_map:
            intersection[key] = root_map[key]
            continue
        
        for letter in root_map[key]:
            if letter in single_map[key]:
                intersection[key].append(letter)
        
        if len(intersection[key]) == 0:
            # root_map and single_map have no letters in common - join them
            intersection[key] = root_map[key] + single_map[key]
        
    return intersection





# store the set of words and what they look like globally so we dont have to spend ages getting them each time
for word in english_words:
    pattern = get_pattern_of_unique(word)
    if pattern not in word_patterns:
        word_patterns[pattern] = [word.upper()]
    else:
        word_patterns[pattern].append(word.upper())


if __name__ == "__main__":
    text = """English is an Indo-European language and belongs to the West Germanic group of the Germanic languages.[15] Old English originated from a Germanic tribal and linguistic continuum along the Frisian North Sea coast, whose languages gradually evolved into the Anglic languages in the British Isles, and into the Frisian languages and Low German/Low Saxon on the continent. The Frisian languages, which together with the Anglic languages form the Anglo-Frisian languages, are the closest living relatives of English. Low German/Low Saxon is also closely related, and sometimes English, the Frisian languages, and Low German are grouped together as the Ingvaeonic (North Sea Germanic) languages, though this grouping remains debated.[12] Old English evolved into Middle English, which in turn evolved into Modern English.[16] Particular dialects of Old and Middle English also developed into a number of other Anglic languages, including Scots[17] and the extinct Fingallian dialect and Yola language of Ireland.[18]

Like Icelandic and Faroese, the development of English in the British Isles isolated it from the continental Germanic languages and influences, and it has since diverged considerably. English is not mutually intelligible with any continental Germanic language, differing in vocabulary, syntax, and phonology, although some of these, such as Dutch or Frisian, do show strong affinities with English, especially with its earlier stages.[19]

Unlike Icelandic and Faroese, which were isolated, the development of English was influenced by a long series of invasions of the British Isles by other peoples and languages, particularly Old Norse and Norman French. These left a profound mark of their own on the language, so that English shows some similarities in vocabulary and grammar with many languages outside its linguistic clades—but it is not mutually intelligible with any of those languages either. Some scholars have argued that English can be considered a mixed language or a creole—a theory called the Middle English creole hypothesis. Although the great influence of these languages on the vocabulary and grammar of Modern English is widely acknowledged, most specialists in language contact do not consider English to be a true mixed language.[20][21]

English is classified as a Germanic language because it shares innovations with other Germanic languages such as Dutch, German, and Swedish.[22] These shared innovations show that the languages have descended from a single common ancestor called Proto-Germanic. Some shared features of Germanic languages include the division of verbs into strong and weak classes, the use of modal verbs, and the sound changes affecting Proto-Indo-European consonants, known as Grimm's and Verner's laws. English is classified as an Anglo-Frisian language because Frisian and English share other features, such as the palatalisation of consonants that were velar consonants in Proto-Germanic (see Phonological history of Old English § Palatalization).[23]

History
Main article: History of English
Overview of history
The earliest varieties of an English language, collectively known as Old English or "Anglo-Saxon", evolved from a group of North Sea Germanic dialects brought to Britain in the 5th century. Old English dialects were later influenced by Old Norse-speaking Viking settlers and invaders, starting in the 8th and 9th centuries. Middle English began in the late 11th century after the Norman Conquest of England, when considerable Old French, especially Old Norman French, and Latin-derived vocabulary was incorporated into English over some three hundred years.[24][25]

Early Modern English began in the late 15th century with the start of the Great Vowel Shift and the Renaissance trend of borrowing further Latin and Greek words and roots, concurrent with the introduction of the printing press to London. This era notably culminated in the King James Bible and the works of William Shakespeare.[26][27] The printing press greatly standardised English spelling,[citation needed] which has remained largely unchanged since then, despite a wide variety of later sound shifts in English dialects.

Modern English has spread around the world since the 17th century as a consequence of the worldwide influence of the British Empire and the United States. Through all types of printed and electronic media in these countries, English has become the leading language of international discourse and the lingua franca in many regions and professional contexts such as science, navigation, and law.[4] Its modern grammar is the result of a gradual change from a typical Indo-European dependent-marking pattern with a rich inflectional morphology and relatively free word order to a mostly analytic pattern with little inflection and a fairly fixed subject–verb–object word order.[28] Modern English relies more on auxiliary verbs and word order for the expression of complex tenses, aspects and moods, as well as passive constructions, interrogatives, and some negation.

Proto-Germanic to Old English
Main article: Old English

The opening of Beowulf, an Old English epic poem handwritten in half-uncial script between 975 AD and 1025 AD: Hƿæt ƿē Gārde/na ingēar dagum þēod cyninga / þrym ge frunon... ("Listen! We of the Spear-Danes from days of yore have heard of the glory of the folk-kings...")
The earliest form of English is called Old English or Anglo-Saxon (c. 550–1066). Old English developed from a set of West Germanic dialects, often grouped as Anglo-Frisian or North Sea Germanic, and originally spoken along the coasts of Frisia, Lower Saxony and southern Jutland by Germanic peoples known to the historical record as the Angles, Saxons, and Jutes.[29] From the 5th century, the Anglo-Saxons settled Britain as the Roman economy and administration collapsed. By the 7th century, this Germanic language of the Anglo-Saxons became dominant in Britain, replacing the languages of Roman Britain (43–409): Common Brittonic, a Celtic language, and British Latin, brought to Britain by the Roman occupation.[30][31][32] At this time, these dialects generally resisted influence from the then-local Brittonic and Latin languages. England and English (originally Ænglaland and Ænglisc) are both named after the Angles.[33]

Old English was divided into four dialects: the Anglian dialects (Mercian and Northumbrian) and the Saxon dialects, Kentish and West Saxon.[34] Through the educational reforms of King Alfred in the 9th century and the influence of the kingdom of Wessex, the West Saxon dialect became the standard written variety.[35] The epic poem Beowulf is written in West Saxon, and the earliest English poem, Cædmon's Hymn, is written in Northumbrian.[36] Modern English developed mainly from Mercian, but the Scots language developed from Northumbrian. A few short inscriptions from the early period of Old English were written using a runic script.[37] By the 6th century, a Latin alphabet was adopted, written with half-uncial letterforms. It included the runic letters wynn ⟨ƿ⟩ and thorn ⟨þ⟩, and the modified Latin letters eth ⟨ð⟩, and ash ⟨æ⟩.[37][38]

Old English is essentially a distinct language from Modern English and is virtually impossible for 21st-century unstudied English-speakers to understand. Its grammar was similar to that of modern German: nouns, adjectives, pronouns, and verbs had many more inflectional endings and forms, and word order was much freer than in Modern English. Modern English has case forms in pronouns (he, him, his) and has a few verb inflections (speak, speaks, speaking, spoke, spoken), but Old English had case endings in nouns as well, and verbs had more person and number endings.[39][40][41] Its closest relative is Old Frisian, but even some centuries after the Anglo-Saxon migration, Old English retained considerable mutual intelligibility with other Germanic varieties. Even in the 9th and 10th centuries, amidst the Danelaw and other Viking invasions, there is historical evidence that Old Norse and Old English retained considerable mutual intelligibility,[42] although probably the northern dialects of Old English were more similar to Old Norse than the southern dialects. Theoretically, as late as the 900s AD, a commoner from certain (northern) parts of England could hold a conversation with a commoner from certain parts of Scandinavia. Research continues into the details of the myriad tribes in peoples in England and Scandinavia and the mutual contacts between them.[42]

The translation of Matthew 8:20 from 1000 shows examples of case endings (nominative plural, accusative plural, genitive singular) and a verb ending (present plural):

Foxas habbað holu and heofonan fuglas nest
Fox-as habb-að hol-u and heofon-an fugl-as nest-∅
fox-nom.pl have-prs.pl hole-acc.pl and heaven-gen.sg bird-nom.pl nest-acc.pl
"Foxes have holes and the birds of heaven nests"""
    key = generate_key()
    key = "".join(key[letter] for letter in key)
    print("Key:", key)
    encrypted = encrypt(text, key)
    print("Encrypted:", encrypted)
    decrypted = decrypt(encrypted, key)
    print("Decrypted:", decrypted)
    cracked = crack(encrypted)
    print("Cracked:", cracked)
    print("Cracked %:", get_english_percent(cracked))
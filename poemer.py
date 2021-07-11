import json
import random
from collections import defaultdict

with open('kosztol.txt', encoding='utf8') as file:
    text = file.read().lower()

with open('ottlik.txt', encoding='utf8') as file:
    text2 = file.read().lower()

text = text + text2

sentences = text.replace('!', '.').replace('?', '.').split('.')

book = defaultdict(list)

ignore_words = ['kosztolányi', 'dezső', 'alakok', 'tartalom', 'bába', '-']

vowels = 'aáeéiíuúüűöőoó'

consonants = ['b', 'c', 'cs', 'd', 'dz', 'dzs', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 'sz', 't', 'ty', 'v', 'w', 'x', 'y', 'z', 'zs']

def get_vowels_from_word(word):
    vowels_in_word = []
    for char in word:
        if char in vowels:
            vowels_in_word.append(char)
    return vowels_in_word


def process_sentence(sentence:str):
    first = 'VERY_FIRST_WORD'
    for word in sentence.lower().split():
        word = word.strip(',').lower().strip(':').strip('"').strip()
        if not word:
            continue
        if word in ignore_words or word.isdigit() or '(' in word or ')' in word:
            continue

        book[first].append(word)
        first = word.lower()


for sentence in sentences:
    process_sentence(sentence.strip().lower())


def generate_sentence(model:dict, first_word=None):
    sentence = []
    first = first_word or 'VERY_FIRST_WORD'
    while sum([len(t) for t in sentence]) < 30:
        try:
            second = random.choice(model[first])
            sentence.append(second)
            first = second
        except IndexError:
            break
    result = " ".join(sentence)
    return result


def get_last_n_vowels(text, n=2):
    last_n_vowels = []
    for char in text[::-1]:
        if char in vowels:
            last_n_vowels.append(char)
            if len(last_n_vowels) == n:
                break
    last_n_vowels.reverse()
    return last_n_vowels


def get_last_n_consonants(text, n):
    last_n_cons = []
    for char in text[::-1]:
        if char in consonants:
            last_n_cons.append(char)
            if len(last_n_cons) == n:
                break
    last_n_cons.reverse()
    return last_n_cons


def rhymes_with(text1, text2, n=2):
    if not text1 or not text2:
        return False
    vowels_match = (get_last_n_vowels(text1, n) == get_last_n_vowels(text2, n))
    consonants_match = (get_last_n_consonants(text1, n) == get_last_n_consonants(text2, n))
    last_word1, last_word2 = text1.split()[-1], text2.split()[-1]
    return vowels_match and consonants_match and (last_word1 != last_word2)


ignore_first_words = ['a']

def generate_poem(model, nr_of_lines=4):
    poem = []
    start_sentence = generate_sentence(model)
    poem.append(start_sentence)
    while True:
        if len(poem) >= nr_of_lines:
            break

        first_word = poem[-1].split()[-1]

        possible_sentence = generate_sentence(model, first_word=first_word)
        if rhymes_with(possible_sentence, poem[-1], n=2):
            poem.append(possible_sentence)
            poem.append(generate_sentence(model))
    return "\n".join(poem)


# print(generate_poem(book))

def get_rhyming_word(word, n=3):
    words = text.split()
    random.shuffle(words)
    for word2 in words:
        if rhymes_with(word, word2, n=n):
            return word2


import nltk
import random
import string
from nltk.corpus import wordnet


def get_stopwords():
    return nltk.corpus.stopwords.words('portuguese')

def synonym_replace(sentence, n):
    new_sentence = sentence.copy()
    random_tokens = list(set([token for token in sentence if token not in get_stopwords()]))
    random.shuffle(random_tokens)
    num_swaps = 0
    for token in random_tokens:
        synonyms = find_synonyms(token)
        if len(synonyms) >= 1:
            synonym = random.choice(synonyms)
            new_sentence = [synonym if word == token else word for word in new_sentence]
            num_swaps += 1
        if num_swaps >= n:
            break
    
    return new_sentence

def find_synonyms(token):
    synonyms = set()
    for syn in wordnet.synsets(token, lang='por'):
        for lem in syn.lemmas('por'):
            synonym = lem.name().replace('_', ' ').replace('-', ' ').lower()
            synonym = ''.join([char for char in synonym if char in string.ascii_lowercase])
            synonyms.add(synonym)
    if token in synonyms:
        synonyms.remove(token)
    return list(synonyms)

def random_insertion(sentence, n):
    new_sentence = sentence.copy()
    for _ in range(n):
        add_word(new_sentence)
    return new_sentence

def add_word(sentence):
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = random.choice(sentence)
        synonyms = find_synonyms(random_word)
        counter += 1
        if counter >= 10:
            return
    random_synonym = synonyms[0]
    idx = random.randint(0, len(sentence)-1)
    sentence.insert(idx, random_synonym)

def random_swap(sentence, n):
    new_sentence = sentence.copy()
    for _ in range(n):
        new_sentence = swap_words(new_sentence)
    return new_sentence

def swap_words(sentence):
    i = j = random.randint(0, len(sentence)-1)
    counter = 0
    while i == j:
        j = random.randint(0, len(sentence)-1)
        counter += 1
        if counter > 3:
            return sentence
    sentence[i], sentence[j] = sentence[j], sentence[i]
    return sentence

def random_deletion(sentence, p):
    if len(sentence) == 1:
        return sentence

    new_sentence = []
    for token in sentence:
        r = random.uniform(0, 1)
        if r > p:
            new_sentence.append(token)

    if len(new_sentence) == 0:
        return random.choice(sentence)

    return new_sentence

def eda(sentence, alpha=0.1, num_aug=9):
    tokens = sentence.split()
    extra_sentences = []
    num_per_tec = int(num_aug / 4) + 1
    n = max(1, int(alpha * len(tokens)))

    for _ in range(num_per_tec):
        extra_sentences.append(' '.join(synonym_replace(tokens, n)))
        extra_sentences.append(' '.join(random_insertion(tokens, n)))
        extra_sentences.append(' '.join(random_swap(tokens, n)))
        extra_sentences.append(' '.join(random_deletion(tokens, alpha)))

    random.shuffle(extra_sentences)
    extra_sentences = extra_sentences[:num_aug]
    extra_sentences.append(sentence)
    
    return extra_sentences

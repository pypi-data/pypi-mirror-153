import cmudict
import math
from pathlib import Path
from qary.config import DATA_DIR

import random
import pandas as pd
import re
from scipy.sparse import dok_matrix
from tqdm import tqdm  # show progress bar


df = pd.DataFrame(cmudict.entries(), columns=['word', 'phones'])
df['exact_rhyme'] = df.phones.apply(list.copy)
df['strong_rhyme'] = df.phones.apply(list.copy)
df['vowel_rhyme'] = df.phones.apply(list.copy)

vowels = ('A', 'E', 'I', 'O', 'U')


def first_consonant_removal(phones_lists):
    """ opening consonants removal

    >>> first_consonant_removal([['B', 'AW1', 'T'],['K', 'AH0', 'Z']])
    [['AW1', 'T'], ['AH0', 'Z']]
    """
    for phone_list in phones_lists:
        for i, phone in enumerate(phone_list):
            i -= i   # in order to always evaluate the first index
            if phone_list[i].startswith(vowels):
                break
            else:
                phone_list.remove(phone_list[i])

    return phones_lists


def phones_lists_to_exact_rhyme(phones_lists=df.exact_rhyme):
    """ first consonant removal, accent removal and syllable tagging

    >>> phones_lists_to_exact_rhyme([['B', 'AW1', 'T'],['K', 'AH0', 'Z']])
    [['AW_1', 'T_1'], ['AH_1', 'Z_1']]
    """
    phones_lists = first_consonant_removal(phones_lists)  # remove first consonants in place

    for phone_list in phones_lists:
        syllable = 1
        for i, phone in enumerate(reversed(phone_list)):
            if phone.startswith(vowels):
                phone_list[-(i + 1)] = phone[:-1] + '_' + str(syllable)
                syllable += 1
            else:
                phone_list[-(i + 1)] = phone + '_' + str(syllable)
    return phones_lists


def phones_lists_to_strong_rhyme(phones_lists=df.strong_rhyme):
    """ consonant removal (save for last syllable consonants), accent removal and syllable tagging

    >>> phones_lists_to_strong_rhyme([['Z', 'UW1', 'G', 'AA0', 'N', 'AA0', 'V']])
    [['UW_3', 'AA_2', 'AA_1', 'V_1']]
    """
    for phone_list in phones_lists:
        syllable = 1
        remove_counter = 0
        for i, phone in enumerate(reversed(phone_list)):
            if phone_list[-(i + 1) + remove_counter].startswith(vowels):
                phone_list[-(i + 1) + remove_counter] = phone[:-1] + '_' + str(syllable)
                syllable += 1
            elif not phone_list[-(i + 1) + remove_counter].startswith(vowels) and syllable < 2:
                phone_list[-(i + 1)] = phone + '_' + str(syllable)
            else:
                phone_list.remove(phone_list[-(i + 1) + remove_counter])
                remove_counter += 1

    return phones_lists


def phones_lists_to_vowel_rhyme(phones_lists=df.vowel_rhyme):
    """ consonant removal, accent removal and syllable tagging

    >>> phones_lists_to_vowel_rhyme([['B', 'AW1', 'T'],['K', 'AH0', 'Z']])
    [['AW_1'], ['AH_1']]
    """
    for phone_list in phones_lists:
        syllable = 1
        remove_counter = 0
        for i, phone in enumerate(reversed(phone_list)):
            if phone_list[-(i + 1) + remove_counter].startswith(vowels):
                phone_list[-(i + 1) + remove_counter] = phone[:-1] + '_' + str(syllable)
                syllable += 1
            else:
                phone_list.remove(phone_list[-(i + 1) + remove_counter])
                remove_counter += 1
    return phones_lists


df.exact_rhyme = phones_lists_to_exact_rhyme()
df.strong_rhyme = phones_lists_to_strong_rhyme()
df.vowel_rhyme = phones_lists_to_vowel_rhyme()


def word_search(source, target):
    for idx, word in enumerate([source, target]):
        if word in list(df.word) and idx == 0:
            source_vector = list(df.iloc[df.word.eq(source).idxmax(), 5:])  # series-to-vector of first source word occurrence
        elif word in list(df.word) and idx == 1:
            target_vector = list(df.iloc[df.word.eq(target).idxmax(), 5:])  # series-to-vector of first target word occurrence
        else:
            for i in range(len(word)):
                if word[:i + 1] in list(df.word) and word[i + 1:] in list(df.word):
                    left_word = df.loc[df.index[df.word == word[:i + 1]][0], 'exact_rhyme']
                    right_word = [df.loc[df.index[df.word == word[i + 1:]][0], 'phones'][0] + '_x'] + \
                        df.loc[df.index[df.word == word[i + 1:]][0], 'exact_rhyme']
                    conjunction = left_word + right_word
                    # Redoing the syllables for the conjunction
                    syllable = 1
                    for i, phone in enumerate(reversed(conjunction)):
                        if phone.startswith(vowels):
                            conjunction[-(i + 1)] = phone[:-1] + str(syllable)
                            syllable += 1
                        else:
                            conjunction[-(i + 1)] = phone[:-1] + str(syllable)
                    break
            vector = []
            for column in df.columns[5:]:
                if column in conjunction:
                    vector.append(1)
                else:
                    vector.append(0)
            if idx == 0:
                source_vector = vector
            else:
                target_vector = vector
    return source_vector, target_vector


def cosine_similarity(source, target):
    source_vector, target_vector = word_search(source, target)

    dot_prod = 0
    for i, v in enumerate(source_vector):
        dot_prod += v * target_vector[i]

        mag_1 = math.sqrt(sum([x**2 for x in source_vector]))
        mag_2 = math.sqrt(sum([x**2 for x in target_vector]))

        score = dot_prod / (mag_1 * mag_2)
    return round(score, 2)


def vowel_dictionary(phones_lists=df.vowel_rhyme):
    vowel_dict = {' '.join(k): [] for k in phones_lists}
    for idx, vows in enumerate(tqdm(phones_lists, desc="Constructing 'vowel' Dictionary", leave=False)):
        vowel_dict[' '.join(vows)].append(df.word[idx])
    return vowel_dict


def strong_dictionary(phones_lists=df.strong_rhyme):
    strong_dict = {' '.join(k): [] for k in phones_lists}
    for idx, vows in enumerate(tqdm(phones_lists, desc="Constructing 'strong' Dictionary", leave=False)):
        strong_dict[' '.join(vows)].append(df.word[idx])
    return strong_dict


def exact_dictionary(phones_lists=df.exact_rhyme):
    exact_dict = {' '.join(k): [] for k in phones_lists}
    for idx, vows in enumerate(tqdm(phones_lists, desc="Constructing 'exact' Dictionary", leave=False)):
        exact_dict[' '.join(vows)].append(df.word[idx])

    return exact_dict


def rhyme_dict(dict_type='strong'):
    if dict_type == 'exact':
        dictionary = exact_dictionary()
    elif dict_type == 'strong':
        dictionary = strong_dictionary()
    elif dict_type == 'vowel':
        dictionary = vowel_dictionary()
    else:
        raise ValueError("Invalid dictionary type; choose between 'exact', strong' or 'vowel' dict_type")
        return
    return dictionary


def rhymer(source, dict_type='strong'):
    """
    A dictionary of rhyming words. .keys() are the pnones according to dict_type (see below) and .values() are
    the words that adhere to the phones pattern

    Parameters
    ----------
    source: str, word to be rhymed with
    dict_type: str, dictionary of rhyming words to be created, default 'strong'
            'exact' => creates dict of words with all consonants, except the intial one, and vowels that rhyme with source
            'strong' => creates dict of words with all vowels and trailing consonants that rhyme with source
            'vowel' => creates dict of words with all vowels that rhyme with source
    """
    dictionary = rhyme_dict(dict_type)  # constructing the rhyme dictionary
    if type(dictionary) is not dict:
        return
    phones_type = f'{dict_type}_rhyme'
    phones = ' '.join(df.loc[df.index[df.word == source][0], phones_type])  # finding the 'dict_type' phones pattern
    candidates = dictionary[phones]  # finding the rhyming words
    candidates.remove(source)  # removing the 'source' word from the list

    return candidates


def rhyme_finder(source, scores=False, threshold=0.5):
    """
    Creates a sorted list of tuples, (rhyming_word, rhyme_score), of vowel_rhyme candidates using an exact_rhyme,
    cosine similarity threshold score

    Parameters
    ----------
    source: str, word used to generate rhyme candidates
    scores: bool, True => threshold applied with accompanied score, False => no threshold applied, default False
    threshold: float, minimum score needed to be included in the list (only applied for scores=True), default 0.5
    """
    vows = ' '.join(df[df.word == source].vowel_rhyme.values[0])
    candidates = vow_dict[vows]
    if scores:
        finalists = []
        for target in tqdm(candidates, desc="Scoring rhyme candidates", leave=False):
            score = cosine_similarity(source, target)
            if score >= threshold:
                finalists.append((target, score))
        finalists.sort(reverse=True, key=lambda x: x[1])
        finalists.remove((source, 1.0))
        candidates = finalists
    return candidates


def tokenizer(corpus):
    corpus = re.sub(r"[^\w\d'\s]+", '', corpus)  # Removing punctuation except apostrophes
    corpus = corpus.lower()
    corpus = corpus.replace('\t', ' ')
    corpus = corpus.replace('\n', ' </stop> ')  # Stop tokens
    corpus = corpus.strip().split()
    return corpus


myfile = open(Path(DATA_DIR) / 'rap' / 'rap_corpus.txt')
corpus = myfile.read()
words = tokenizer(corpus)
myfile.close()


def prior_word_matrix(words, n=1):
    word_set = list(set(words))
    word_dok = {word: i for i, word in enumerate(word_set)}
    if n > 1:
        n_grams = [' '.join(words[i:i + n]) for i, _ in enumerate(words[:-n + 1])]
    else:
        n_grams = [' '.join(words[i:i + n]) for i, _ in enumerate(words)]

    sets_count = len(list(set(n_grams)))
    prior_word_matrix = dok_matrix((sets_count, len(word_set)))

    n_grams_set = list(set(n_grams))
    n_grams_dok = {word: i for i, word in enumerate(n_grams_set)}

    for i, word in enumerate(n_grams[-1:n:-1]):
        n_grams_idx = n_grams_dok[word]
        prior_word_idx = word_dok[list(reversed(words))[i + n]]
        prior_word_matrix[n_grams_idx, prior_word_idx] += 1

    return prior_word_matrix, n_grams_dok, word_set


def word_before_n_gram(word_sequence, n=1):
    p_matrix, n_grams_dok, word_set = prior_word_matrix(words, n)
    index = n_grams_dok[word_sequence]
    prior_word_vector = p_matrix[index]
    probability = prior_word_vector / prior_word_vector.sum()  # [1, 0, 0, 2, 1] --> [0.25, 0, 0, 0.5, 0.25]

    return random.choices(word_set, probability.toarray()[0])  # selects column associated word according to
    # probability vector, eg. [0.25, 0, 0, 0.5, 0.25]


def stochastic_chain(seed, clean=True, min_length=5, max_length=10, seed_length=1):
    if min_length > max_length:
        raise ValueError("min_length cannot exceed _max_length")
        return
    current_words = seed.split(' ')
    if len(current_words) != seed_length:
        raise ValueError(f'wrong number of words, expected {seed_length}')

    sentence = seed
    dirty = ['fuck', 'shit', 'bitch', 'nigga', 'niggas', 'pussy', 'dick']

    if not clean:
        for _ in range(max_length - len(current_words)):
            next_word = word_before_n_gram(' '.join(current_words), seed_length)
            if next_word[0] == '</stop>' and len(sentence.split()) >= min_length:
                break
            else:
                sentence = next_word[0] + ' ' + sentence
                current_words = current_words[::-1]  # reverse the word order
                current_words = next_word + current_words[1:]
    else:
        for _ in range(max_length - len(current_words)):
            next_word = word_before_n_gram(' '.join(current_words), seed_length)
            if next_word in dirty:
                print('DIRTY!')
                continue
            elif next_word[0] == '</stop>' and len(sentence.split()) >= min_length:
                break
            else:
                sentence = next_word[0] + ' ' + sentence
                current_words = current_words[::-1]  # reverse the word order
                current_words = next_word + current_words[1:]
    if len(sentence.split()) > min_length:  # prevents n-grams from being truncated
        return sentence.replace('</stop>', '')
    else:
        return sentence

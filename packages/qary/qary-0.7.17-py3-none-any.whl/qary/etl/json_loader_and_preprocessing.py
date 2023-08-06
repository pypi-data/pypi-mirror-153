"""process words and add them to a json file then to gzip  """

import gzip
import json
from pathlib import Path

from tqdm import tqdm
from collections import Counter

from qary.constants import DATA_DIR
from qary.spacy_language_model import nlp


def process_words(filepath):
    r'''extract words as keys and word count as values

    >>> filepath = Path(DATA_DIR, 'testsets', 'unit-tests-data.gz')
    >>> process_words(filepath)
    >>> f = Path(DATA_DIR, 'corpora', 'unit-tests-data-processed.gz')
    >>> filepath = Path(DATA_DIR, 'testsets', 'unit-test-data.txt')
    >>> process_words(filepath)
    >>> k = Path(DATA_DIR, 'corpora', 'unit-test-data-processed.gz')
    >>> f.unlink()
    >>> k.unlink()
    '''

    file_name = Path(str(filepath)).stem
    words_filepath = Path(DATA_DIR, 'corpora', file_name + '-processed' + '.json')

    words = prep_filetype(filepath)

    batchsize = 100000
    for i in tqdm(range(0, len(words), batchsize)):
        vocabulary_words = Counter()
        batch = words[i:i + batchsize]
        for word in tqdm(batch):
            word = word.replace('_', ' ')
            title_words = [
                token.text for token in nlp(word) if not token.like_num and token.is_alpha and token.is_ascii]
            vocabulary_words += Counter(title_words)
        if words_filepath.is_file():
            with open(words_filepath, 'r') as vocab:
                vocab = json.load(vocab)
            with open(words_filepath, 'w') as more_vocab:
                new_vocab = Counter(vocab) + Counter(vocabulary_words)
                json.dump(new_vocab, more_vocab, indent=2)
        else:
            with open(words_filepath, 'w') as vocab:
                json.dump(vocabulary_words, vocab, indent=2)
    json_to_gzip(words_filepath)
    words_filepath.unlink()


def prep_filetype(filepath):
    r""" read the contents of a file and return a str (.txt) or list of lines (.gz)

    >>> filepath = Path(DATA_DIR, 'testsets', 'unit-tests-data.gz')
    >>> prep_filetype(filepath)[0][1:13]
    'Hello World!'
    >>> filepath = Path(DATA_DIR, 'testsets', 'unit-test-data.txt')
    >>> prep_filetype(filepath)[:12]
    'Hello World!'
    """

    if filepath.suffix == ".txt":
        with open(filepath) as fin:
            words = fin.read()
            return words
    if filepath.suffix == ".gz":
        with gzip.open(filepath) as fin:
            words = fin.read()
            words = words.decode().split('\n')
            return words


def json_to_gzip(json_filepath):
    r""" encode and compress json file

    >>> JSON_FILEPATH = Path(DATA_DIR, 'corpora', 'data.json')
    >>> GZIP_FILEPATH = Path(DATA_DIR, 'corpora', 'data.gz')
    >>> with open(JSON_FILEPATH, "w") as file: json.dump({"Hello": "World"}, file)
    >>> json_to_gzip(JSON_FILEPATH)
    >>> GZIP_FILEPATH.exists(); JSON_FILEPATH.unlink(); GZIP_FILEPATH.unlink()
    True
    """

    file_name = Path(str(json_filepath)).stem
    gzip_filepath = Path(DATA_DIR, 'corpora', file_name + '.gz')
    with open(json_filepath, 'rb+') as file:
        jsn = json.load(file)
        jsns = json.dumps(jsn)
        encoded_json = jsns.encode('utf-8')
        compressed_json = gzip.compress(encoded_json)

    with gzip.open(gzip_filepath, 'wb') as file:
        file.write(compressed_json)

""" String manipulation and hashing utilities for indexing Wikipedia pages and titles """
import gzip
import hashlib
from pathlib import Path
import re
import json

import numpy as np
import pandas as pd
from slugify import slugify  # noqa

from qary.config import DATA_DIR
from qary.spacy_language_model import nlp


def simple_tokenize(s: str):
    r""" Regular expression tokenizer from nlpia.ch2

    >>> ' '.join(simple_tokenize("Can't say goodbye... yet."))
    "Can't say goodbye . . . yet ."
    """
    return list(re.findall(r'\w+(?:\'\w+)?|[^\w\s]', s))


def normalize_wikititle(title: str):
    r""" Case folding and whitespace normalization for wikipedia cache titles (keys)

    >>> normalize_wikititle("\n _Hello_\t\r\n_world_!  _\n")
    'hello world !'
    """
    return re.sub(r'[\s_]+', ' ', title.title()).strip().lower()


def capitalize_acronyms(text: str):
    r""" Find acronyms and capitalize them

    >>> capitalize_acronyms("aye cap'n my ai captain")
    "aye cap'n my AI captain"
    """


def capitalize_acronyms(text: str):
    toks = nlp(text)
    toks_info = []
    for t in toks:
        d = {}
        for k in dir(t):
            d[str(k)] = str(getattr(t, k, ''))
        toks_info.append(d)
    # FIXME:
    json.dump([
        dict([
            (k, v[:70]) for (k, v) in d.items()
        ]) for d in toks_info
    ], indent=4)
    return toks_info

    # https://raw.githubusercontent.com/krishnakt031990/Crawl-Wiki-For-Acronyms/master/AcronymsFile.csv


def squash_wikititle(title: str, lowerer=str.lower):
    r""" Lowercase and remove all non-alpha characters, including whitespace

    >>> squash_wikititle("_Hello \t g00d-World_ !!!")
    'hellogdworld'
    """
    return re.sub(r'[^a-z]', '', lowerer(str(title)))


def normalize_name(s, lower=True, underscores=True, strip=True):
    r""" String normalizer to create variable name(ish) str (.lower .strip .replace \s=>_

    >>> normalize_name(' a-a . ! ')
    'a_a_._!'
    """
    if lower:
        s = str.lower(s)
    if strip:
        s = str.strip(s)
    if underscores:
        s = re.sub(r'[\s-]', '_', s)
    return s


def normalize_keys(turns_list_raw=None):
    """ Normalize the keys of a raw turns list (typically from a human-edited yaml file)

    1. Lowercase all keys in all dicts
    2. Strip whitespace from beginning and end of all keys in all dicts
    3. Replace all spaces (' ') with underscords ('_') in all keys in all dicts
    4. Rename the 'nlp' key to 'match_method'

    `turns_list_raw` must be mutable in place (list of dicts, rather than tuple of dicts)

    >>> normalize_keys(turns_list_raw=[dict(state='State Name', nlp='EXACT'), {' State  ': 'ID_01', ' NLP ': None}])
    [{'state': 'State Name', 'match_method': 'EXACT'},
     {'state': 'ID_01', 'match_method': None}]
    """
    for i, turn in enumerate(turns_list_raw):
        if not turn:  # possibility of empty list values
            continue
        turn = {(key or '').lower().strip().replace(' ', '_'): value for key, value in turn.items()}
        if 'nlp' in turn:
            turn['match_method'] = turn['nlp']
            del turn['nlp']
        turns_list_raw[i] = turn
    return turns_list_raw


def md5(s: str, num_bytes=8, dtype=np.uint64):
    r""" Like builtin hash but consistent across processes and accepts custom dtype (default npuint64)

    >>> md5('helloworld')
    6958444691603744019
    >>> md5(b'helloworld')
    6958444691603744019
    >>> md5('hello world')
    14810798070885308281
    >>> md5('Hello world')
    4747398888332172685
    >>> type(_)
    <class 'numpy.uint64'>
    >>> md5('Hello world', num_bytes=4, dtype=np.uint32)
    3659505037
    >>> md5('Hello world', num_bytes=5, dtype=np.uint32)
    3659505037
    >>> type(_)
    <class 'numpy.uint32'>
    >>> md5('Hello world', num_bytes=5, dtype=np.uint64)
    149688393101
    >>> md5('Hello world', num_bytes=4, dtype=np.uint64)
    3659505037
    """
    s = s if isinstance(s, bytes) else s.encode()
    s = str(s).encode()
    hasher = hashlib.md5()
    hasher.update(s)
    # md5.digest() is 16-byte hex representation in raw bytes object like b'^\xb6;\xbb\xe0...
    # this truncates it to the num_bytes LSBs
    hex_digest = hasher.digest()[::-1][:num_bytes]
    digest_dtype = dtype(
        np.sum(np.fromiter(
            (dtype(c) * dtype(256)**dtype(i) for i, c in enumerate(hex_digest)),
            dtype=dtype)))
    return digest_dtype


def hashed_titles_series(titles, dtype=np.uint32):
    """ Ensure titles are in np.array, normalize each title, alphabetize,

    Essentially:
        titles = titles.sort_values().unique()
        hashes = np.array([md5(t) for t in titles]).astype(dtype)
        return pd.Series(titles, index=hashes)

    >>> hashed_titles_series(['Hello', 'g00d-World!'])
    1609046494713271862       hello
    15478009694767029955    gdworld
    dtype: object
    >>> md5(squash_wikititle('!!HELLO!!')) in _.index
    True
    """
    if hasattr(titles, 'columns'):
        titles = titles[titles.columns[0]]
    if hasattr(titles, 'values'):
        titles = titles.values
    titles = np.array(titles)
    titles = np.array([squash_wikititle(str(t)) for t in titles])
    title_hashes = np.fromiter((md5(title) for title in titles), dtype=np.uint64, count=len(titles))
    return pd.Series(titles, index=title_hashes)


def read_hashes(
        filepath=Path(DATA_DIR, 'corpora', 'wikipedia', 'wikipedia-titles-alphaonly-hashed.uint64.npy.gz')):
    with gzip.open(filepath, 'rb') as fin:
        hashesread = np.load(fin)
    return hashesread

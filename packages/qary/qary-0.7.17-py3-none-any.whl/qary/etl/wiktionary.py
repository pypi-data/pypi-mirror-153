""" Download wiktionary slang words glossary """
import os
from datetime import datetime as Datetime
from datetime import date as Date
import requests

import pandas as pd

from qary.constants import DATA_DIR


def scrape_slang(url='https://bestlifeonline.com/2010s-slang/'):
    return requests.get(url).text


def find_latest_index(lang='en', date='20200101'):
    if isinstance(date, (Datetime, Date)):
        date = f'{date.year}{date.month}{date.day}'
    return f'https://dumps.wikimedia.org/{lang}wiktionary/{date}/' \
        f'{lang}wiktionary-{date}-pages-articles-multistream-index.txt.bz2'


def load_english_index(path='{lang}wiktionary-{date}-pages-articles-multistream-index.txt.bz2',
                       lang='en', date='20200101'):
    if '{' in path:
        path = path.format(lang=lang, date=date)
    for p in [path, os.path.join(DATA_DIR, path), find_latest_index]:
        p = p() if callable(p) else p
        try:
            return pd.read_csv(p, sep=':')
        except IOError:
            pass


def get_page_ids(word, url='https://en.wiktionary.org/w/api.php', params=None):
    """ Get the page ID for a word, -1 if page/word doesn't exist

    TODO: search titles with: action=query&list=search&srsearch=Nelson%20Mandela&utf8=&format=json

    >>> get_page_ids('testnotaword')
    []
    """
    default_params = dict(
        action='query',
        format='json',
        list='search',
        # utf8=True,
    )
    default_params.update(dict(title=str(word)))
    default_params.update(params or {})
    resp = requests.get(url, params=default_params)
    js = resp.json()
    if isinstance(js, dict):
        return list(js.get('query', {}).get('pages', {}).keys())
    else:
        return []

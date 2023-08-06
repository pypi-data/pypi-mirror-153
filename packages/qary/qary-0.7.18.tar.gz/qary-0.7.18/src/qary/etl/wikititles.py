import gzip
from pathlib import Path

from tqdm import tqdm
import pandas as pd
import numpy as np
# FIXME: use nessvec wikicrawl
# from wikipediaapi import Wikipedia

from qary.spacy_language_model import load
from qary.config import DATA_DIR, QUESTION_STOPWORDS
from qary.etl.netutils import download_if_necessary
from qary.etl import utils

import logging
log = logging.getLogger(locals().get('__name__', ''))

nlp = load('en_core_web_md')
EXCLUDE_HEADINGS = ['See also', 'References', 'Bibliography', 'External links']
TOPIC_TITLES = {
    'chatbot': ['Chatbot', 'ELIZA', 'Turing test', 'AIML', 'Chatterbot', 'Loebner prize', 'Chinese room'],
}


class WikiNotFound:
    text = ''
    summary = ''


def read_and_hash_titles(filepath=None, chunksize=100000, numchunks=None):
    """ Numpy crashing due to unit32() on NaNs in wikipedia titles

    >>> hashes = read_and_hash_titles(chunksize=1000, numchunks=8)
    >>> hashes.shape
    (8000,)
    >>> utils.md5('fu') in hashes
    True
    """
    if filepath is None:
        filepath = 'wikipedia-titles-alphaonly'
    filepath = download_if_necessary(filepath)
    hashes = []
    for i, chunk in enumerate(tqdm(pd.read_csv(filepath, chunksize=chunksize))):
        titles = tuple(chunk.dropna()[chunk.columns[0]].astype(str))
        hashes += list(
            utils.md5(utils.squash_wikititle(str(title))) for title in titles)
        if numchunks is not None and i >= numchunks - 1:
            break
    return np.array(hashes, dtype=np.uint64)


def save_hashes(hashes=None,
                dest_filepath=Path(DATA_DIR, 'corpora', 'wikipedia', 'wikipedia-titles-alphaonly-hashed.uint64.npy.gz')):
    r""" Save a compressed set of hashed Wikipedia titles to be used later to predict whether an n-gram is a valid title

    >>> dest = Path(DATA_DIR, 'doctest-save-hashes.uint64.npy.gz')
    >>> str(save_hashes(hashes='1 2 3 123456789'.split(), dest_filepath=dest)).endswith(str(dest))
    True
    """
    hashes = np.fromiter((np.uint64(h) for h in hashes), dtype=np.uint64)
    with gzip.open(dest_filepath, 'wb') as fout:
        np.save(fout, hashes)
    return dest_filepath


def elastic_results_as_page_dict(results):
    see_also_links = []
    return {}
    return dict(
        title=results['title'],
        text=results['text'],
        summary=results['summary'],
        see_also_links=see_also_links)


def guess_topic(query=None):
    """ Use hard coded TOPIC_TITLES dict to infer a topic based on the last word in a question

    >>> guess_topic('What ELIZA?')
    'chatbot'
    >>> guess_topic('What are ChatboTs ? ')
    'chatbot'
    >>> guess_topic('Where did you get the name Qary?')
    """
    if query and isinstance(query, str):
        query = query.lower().strip().strip('?').strip().rstrip('s')
        for topic, titles in TOPIC_TITLES.items():
            for title in titles:
                if query.endswith(title.strip().lower()):
                    return topic


class ArticleCache(dict):
    pass


# wikiscraper = WikiScraper()
# scrape_article_texts = wikiscraper.scrape_article_texts


def count_nonzero_vector_dims(self, strings, nominal_dims=1):
    r""" Count the number of nonzero values in a sequence of vectors

    Used to compare the doc vectors normalized as Marie_Curie vs "Marie Curie" vs "marie curie",
    and found that the spaced version was more complete (almost twice as many title words had valid vectors).

    >> count_nonzero_vector_dims(df[df.columns[0]].values[:100]) / 300
    264.0
    >> df.index = df['page_title'].str.replace('_', ' ').str.strip()
    >> count_nonzero_vector_dims(df.index.values[:100]) / 300
    415.0
    """
    tot = 0
    for s in strings:
        tot += (pd.DataFrame([t.vector for t in nlp(s)]).abs() > 0).T.sum().sum()
    return tot


def list_ngrams(token_list, n=3, sep=' '):
    r""" Return list of n-grams from a list of tokens (words)

    >>> ','.join(list_ngrams('Hello big blue marble'.split(), n=3))
    'Hello,Hello big,Hello big blue,big,big blue,big blue marble,blue,blue marble,marble'
    >>> ','.join(list_ngrams('Hello big blue marble'.split(), n=3, sep='_'))
    'Hello,Hello_big,Hello_big_blue,big,big_blue,big_blue_marble,blue,blue_marble,marble'
    """
    if isinstance(token_list, str):
        token_list = [tok.text for tok in nlp(token_list)]
    ngram_list = []

    for i in range(len(token_list)):
        for j in range(n):
            if i + j < len(token_list):
                ngram_list.append(sep.join(token_list[i:i + j + 1]))

    return ngram_list


def count_ignorable_words(text, ignore=QUESTION_STOPWORDS, min_len=2):
    r""" Count the number of words in a space-delimitted string that are not in set(words)

    >>> count_ignorable_words('what a hello world in')
    3
    >>> count_ignorable_words('what a hello world in', ignore=['what'], min_len=1)
    2
    >>> count_ignorable_words('what a hello world in', ignore=['what'], min_len=0)
    1
    """
    return sum(1 for w in text.split() if w in ignore or len(w) <= min_len)


# def parse_sentences(title, sentences, title_depths, see_also=True, exclude_headings=(), d=0, depth=0, max_depth=3):

#     return sentences, title_depths

# class WikiIndex():
#     """ CRUFT: Semantic and trigram index for wikipedia page titles

#     Uses too much RAM and is too slow.
#     """
#     _url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz'

#     def __init__(self, url=None, refresh=False, **pd_kwargs):
#         self._url = url or self._url
#         self.df_titles = self.load(url=self._url, refresh=refresh, **pd_kwargs)
#         # self.title_slug = self.df_titles.to_dict()
#         # self.df_vectors = pd.DataFrame(nlp(s).vector for s in self.df_titles.index.values)
#         # self.vectors = dict(zip(range(len(self.df_titles)), ))
#         self.title_row = dict(zip(self.df_titles.index.values, range(len(self.df_titles))))
#         # AttributeError: 'tuple' object has no attribute 'lower
#         # self.title_row.update({k.lower(): v for (k, v) in tqdm(self.title_row.items()) if k.lower() not in self.title_row})
#         # self.df_vectors = self.compute_vectors()

#     def compute_vectors(self, filename='wikipedia-title-vectors.csv.gz'):
#         log.warning(f'Computing title vectors for {len(self.df_titles)} titles. This will take a while.')
#         filepath = Path(DATA_DIR, filename)
#         start = sum((1 for line in gzip.open(filepath, 'rb')))
#         total = len(self.df_titles) - start
#         vec_batch = []
#         with gzip.open(filepath, 'ta') as fout:
#             csv_writer = csv.writer(fout)
#             csv_writer.writerow(['page_title'] + [f'x{i}' for i in range(300)])
#             for i, s in tqdm(enumerate(self.df_titles.index.values[start:]), total=total):
#                 vec = [s] + list(nlp(str(s)).vector)  # s can sometimes (rarely) be a float because of pd.read_csv (df_titles)
#                 vec_batch.append(vec)
#                 if not (i % 1000) or i == total - 1:
#                     csv_writer.writerows(vec_batch)
#                     print(f"wrote {len(vec_batch)} rows")
#                     try:
#                         print(f'wrote {len(vec_batch), len(vec_batch[0])} values')
#                     except IndexError:
#                         pass
#                     vec_batch = []
#         time.sleep(1)
#         dtypes = {f'x{i}': pd.np.float16 for i in range(300)}
#         dtypes.update(page_title=str)
#         self.df_vectors = pd.read_csv(filepath, dtype=dtypes)
#         return self.df_vectors

#     def load(
#             self,
#             url='https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz',
#             refresh=False,
#             **pd_kwargs):
#         url_dir, filename = os.path.split(url)
#         filepath = Path(DATA_DIR, 'corpora', 'wikipedia', filename)
#         df = None
#         if not refresh:
#             try:
#                 df = pd.read_csv(filepath, dtype=str)
#             except (IOError, FileNotFoundError):
#                 log.info(f'No local copy of Wikipedia titles file was found at {filepath}')
#         if not len(df):
#             log.warning(f'Starting download of entire list of Wikipedia titles at {url}...')
#             df = pd.read_table(url, dtype=str)  # , sep=None, delimiter=None, quoting=3, engine='python')
#             log.info(f'Finished downloading {len(df)} Wikipedia titles from {url}.')

#         df.columns = ['page_title']
#         if df.index.name != 'natural_title':
#             df.index = list(df['page_title'].str.replace('_', ' ').str.strip())
#             df.index.name == 'natural_title'
#             df.to_csv(filepath, index=False, compression='gzip')
#             log.info(f'Finished saving {len(df)} Wikipedia titles to {filepath}.')
#         self.df_titles = df
#         return self.df_titles

#     def find_similar_titles(self, title=None, n=1):
#         """ Takes dot product of a doc vector with all wikipedia title doc vectors to find closest article titles """
#         if isinstance(title, str):
#             vec = nlp(title).vector
#         else:
#             vec = title
#         vec /= pd.np.linalg.norm(vec) or 1.
#         dot_products = vec.dot(self.df_vectors.values.T)
#         if n == 1:
#             return self.df_titles.index.values[dot_products.argmax()]
#         sorted(dot_products, reverse=True)

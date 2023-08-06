import logging
from qary import spacy_language_model

log = logging.getLogger(__name__)
nlp = spacy_language_model.nlp

try:
    assert nlp._meta['vectors']['width'] == 300  # len(nlp('word vector').vector) < 300:
except AssertionError:
    log.warning(f"SpaCy Language model ({nlp._meta['name']}) doesn't contain 300D word2vec word vectors.")
    nlp = spacy_language_model.nlp = spacy_language_model.load('en_core_web_md')
assert nlp._meta['vectors']['width'] == 300


def iou(a, b):
    """ Crude character vector overlap measure of string similarity

    >>> iou('Hello', 'World')
    0.285...
    """
    a, b = set(a.lower().strip()), set(b.lower().strip())
    return len(a & b) / len(a | b)


def bleu(text, reference_text, weight1=0.25, weight2=0.25, weight3=0.25, weightL=0.25):
    """Compute the BLEU similarity between a text string and a reference text.

    All the different weights are for different N-grams. E.g.weight1 for unigram.
    Both the texts must have at least four words. Otherwise the BLEU score is zero.
    The full-stops matter

    FIXME: need NLTK (or external BLEU package) to get these scores right
    >> bleu('I visited the park and enjoyed.', 'I visited the park and had fun ')
    0.6148
    >> bleu('','')
    0
    >> bleu('','I am happy')
    0
    >> bleu('I visited', 'I visited the park and had fun ')
    0.0
    >> bleu('I am happy and contented', 'I am happy and joyous')
    0.6687
    >> bleu('I am going to visit the park and have fun.','I am going to visit.')
    0.3672
    >> bleu('I am going to visit the park and have fun.','I am going to visit')
    0.3508
    """

    doc = nlp(text)
    reference_doc = nlp(reference_text)

    tokens = [token.text for token in doc]
    reference_tokens = [token.text for token in reference_doc]

    # FIXME: pure python BLEU score?
    bleu_score = sum([t == r for (t, r) in zip(tokens, reference_tokens)]) / max([1, len(tokens), len(reference_tokens)])
    return round(bleu_score, 4)


def overlapping_words(tokens, reference_tokens):
    count = 0
    extra_list = []
    for word1 in tokens:
        if word1 in reference_tokens:
            count += 1
            extra_list.append(word1)
    for word2 in reference_tokens:
        if word2 not in extra_list and word2 in tokens:
            count += 1
    return count


def lemmatize(text):
    return [tok.lemma_ for tok in nlp(text)]


def rouge1(text, reference_text):
    """Compute the ROUGE similarity between a text string and a reference text with unigram.

    Case doesn't matter, full-stop doesn't matter.
    Both the texts can be anything except blanks and punctuations as long as the reference text has it.
    A character, number can also be considered as a word if it's in the reference text.
    >>> rouge1('police killed the gunman', 'police kill the gunman')
    1.0
    >>> rouge1('police killed the gunman', 'the gunman was killed by the police')
    0.7273
    >>> rouge1('police killed the gunman', 'gunman killed the police')
    1.0
    >>> rouge1('police killed the gunman', 'police is killing the gunman')
    0.8889
    >>> rouge1('police killed the gunman.', 'police killed the gunman')
    1.0
    >>> rouge1('police killed the gunman', 'POLICE killed the gunman')
    1.0
    >>> rouge1('police killed the gunman', 'police killed the')
    0.8571
    >>> rouge1('police killed the gunman', 'police killed')
    0.6667
    >>> rouge1('police killed the gunman', '')
    0.0
    >>> rouge1('police killed the gunman', 'police')
    0.4
    >>> rouge1('', '')
    0.0
    >>> rouge1('?', '?')
    0.0
    """
    doc = nlp(text)
    reference_doc = nlp(reference_text)
    tokens = [token.text for token in doc]
    reference_tokens = [token.text for token in reference_doc]
    punctuations = '''!()-[]{};:'"r"\",<>./?@#$%^&*_~'''
    tokens = [lemmatize(word.lower()) for word in tokens if word not in punctuations]
    reference_tokens = [lemmatize(word.lower()) for word in reference_tokens if word not in punctuations]
    count = overlapping_words(tokens, reference_tokens)
    try:
        recall = count / len(reference_tokens)
    except ZeroDivisionError:
        recall = 0.0
    try:
        precision = count / len(tokens)
    except ZeroDivisionError:
        precision = 0.0
    try:
        fmeasure = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        fmeasure = 0.0
    return round(fmeasure, 4)


def score(reply, stmt=None, **kwargs):
    """ Compute word2vec docvec cosine similarity (fall back to character IOU)

    >>> score('Hello world!', 'Goodbye big earth!') > .5
    True
    """
    global nlp
    nlp = kwargs.get('nlp', nlp)
    if kwargs is None or nlp is None or not stmt or not reply:
        return 0.0

    reply_doc, stmt_doc = nlp(str(reply)), nlp(str(stmt))

    if not reply_doc or not stmt_doc or not reply_doc.has_vector or not stmt_doc.has_vector:
        # FIXME: levenshtien would be better or fuzzywuzzy
        return iou(reply, stmt)

    cos_sim = reply_doc.similarity(stmt_doc)
    log.debug(f'cos_sim={cos_sim}')
    return cos_sim


class Doc:
    global nlp

    def __init__(self, text='', nlp=nlp):
        """ Create a Doc object with an API similar to spacy.Doc

        >>> d = Doc('Hello')
        >>> len(d.vector)
        300
        >>> d.doc.similarity(d.doc) > .99
        True
        """
        self.nlp = nlp if nlp is not None else self.nlp
        self.text = text
        self.doc = nlp(text)
        self.vector = self.doc.vector

    def similarity(self, other_doc):
        """ Similarity of self Doc object meaning to the meaning of another Doc object

        >>> doc = Doc('USA')
        >>> doc.similarity(Doc('United States'))
        0.5...
        """
        if hasattr(other_doc, 'vector_norm'):
            return self.doc.similarity(other_doc)
        else:
            return self.doc.similarity(getattr(other_doc, 'doc', other_doc))


def similarity(text1, text2):
    """ Similarity between two natural language texts (words, phrases, documents) 1 = 100%, -1 = -100%

    >>> similarity('Hello', 'hello') > 0.99
    True
    >>> .8 > similarity('Hello!', 'Hi?') > 0.75
    True
    """
    return Doc(text1).similarity(Doc(text2).doc)

    # log.debug(f"vector1 for text1 {vector1}")
    # question_vector /= np.linalg.norm(question_vector)
    # log.debug(f"faq['question_vectors'].shape is {self.faq['question_vectors'].shape}")
    # question_similarities = self.faq['question_vectors'].dot(question_vector.reshape(-1, 1))

# 1) create doctest in the historybot
# 2) run pytest
# 3) modularise reply method of historybot
# 4) rerun pytests
# 5) doctest for random_reply function
# 6) rerun pytests and debug
# 7) refactor random_reply self to parsed_dialog
# 8) rerun pytests and debug
import logging
import random
import regex
# from nltk.cluster.util import cosine_distance
from qary import spacy_language_model as slm

import torch
from transformers import BertModel, BertTokenizer
import sentence_transformers as st
import numpy as np
import pandas as pd
from collections import abc
import spacy
from qary.chat.understanders import check_match
from qary.chat.dialog import get_nxt_cndn_match_mthd_dict

log = logging.getLogger(__name__)
# BERT_TOKENIZER = tokenizer_class.from_pretrained(pretrained_weights)
# BERT_MODEL = model_class.from_pretrained(pretrained_weights)
# fix this


def is_vector(x):
    try:
        return isinstance(x[0], (float, int))
    except IndexError:
        return False


class TransformerDoc:  # (spacy.Doc):
    """ A container to mimic the spacy.Doc object , mainly for the .vector API

    TODO: create a modified nlp pipeline that uses other embeddings like sentence_transfomers
    """

    def __init__(self, text=None, doc=None, nlp=None, vector=None, **kwargs):
        super().__init__()
        self.text = text
        self.doc = None
        self.nlp = None
        self.vector = vector
        if nlp is not None and callable(nlp):
            self.nlp = nlp
        if doc is not None and not isinstance(doc, str):
            self.doc = doc
        if text is not None:
            if isinstance(text, str):
                pass
            elif isinstance(text, (spacy.tokens.doc.Doc, TransformerDoc)):
                self.doc = self.text
                self.text = text.text
            else:
                self.text = str(text)
        if self.doc is None and self.nlp is not None and isinstance(self.text, str):
            self.doc = self.nlp(self.text)
        try:
            self.vector = self.doc.vector
        except AttributeError:
            if hasattr(self.doc, '__len__') and len(self.doc) and isinstance(self.doc[0], float):
                self.vector = self.doc
                del self.doc

    # def __new__(self, *args, **kwargs):
    #     vector, text = None, None
    #     args = list(reversed(args))
    #     while args:
    #         arg = args.pop()
    #         if is_vector(arg):
    #             vector = arg
    #         else:
    #             text = str(arg)
    #     self.text = kwargs.pop('text') if 'text' in kwargs else text
    #     self.vector = kwargs.pop('vector') if 'vector' in kwargs else vector
    #     return self

    #     # text = None
    #     # for arg in args:
    #     #     if not is_vector(arg):
    #     #         text = str(arg)
    #     # text = kwargs.pop('text') if 'text' in kwargs else text
    #     if self.text is not None:
    #         return str(self.text)
    #     else:
    #         return super().__new__(str)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text


class BertEncoder:

    def __init__(self, name='bert-base-multilingual-cased'):
        """ Initialize a BERT tokenizer and model """
        self.tokenizer = BertTokenizer.from_pretrained(name)
        self.model = BertModel.from_pretrained(name)

    def encode(self, text):
        """ Encode text as a 762-D vector

        >>> encoder = BertEncoder()
        >>> v1 = encoder("Emotions completely transform us as people, "
        ...              "and good bots can transform our emotions for the better.").vector
        >>> v2 = encoder("AI is good at giving people strong addictive emotional reactions. "
        ...              "Emotions completely change humans.").vector
        >>> len(v1)
        768
        >>> float(v1.dot(v2) / np.linalg.norm(v1) / np.linalg.norm(v2))
        0.9...
        """
        text = str(text)
        input_ids = torch.tensor([self.tokenizer.encode(text)])
        with torch.no_grad():
            output_tuple = self.model(input_ids)
        doc = TransformerDoc(text=text, vector=output_tuple[0][0][0])
        doc.vector = output_tuple[0][0][0]
        return doc

    def __call__(self, *args, **kwargs):
        return self.encode(*args, **kwargs)

    def text_similarity(self, text1, text2):
        v1 = self.encode(text1).vector
        v2 = self.encode(text2).vector

        ratio = (v1.dot(v2) / np.linalg.norm(v1) / np.linalg.norm(v2)).item()
        return ratio

        # modularise this function, into a class and inherit from there
        # look up 'super()'
        # timeit
        # create a dataset and check accuracies of each model


class AnyNLP:
    def __init__(self, nlp='spacy'):
        if not isinstance(nlp, AnyNLP):
            if callable(nlp):
                self.nlp = nlp
            else:
                self.nlp = get_nlp(nlp)

    def encode(self, doc):
        if isinstance(doc, str):
            self.text = doc
            self.doc = self.nlp(doc)
        else:
            self.text = doc.text
            self.doc = doc
        return self.doc.vector

    def __call__(self, text):
        return TransformerDoc(text=self.nlp(text), encoder=self.encode)


def get_nlp(nlp='spacy'):
    """ return an NLP pipeline with an API similar to the object returned by `spacy.load('en_core_web_md')`

    >>> nlp = get_nlp()
    >>> len(nlp('hi').vector)
    300

      > nlp = get_nlp('sentence_transformers')
      > len(nlp('hi').vector)
    368
    """
    if isinstance(nlp, str):
        nlp = nlp.strip().lower()
        if nlp.startswith('spac'):
            nlp = slm.nlp
            if nlp._meta['vectors']['width'] < 300:  # len(nlp('word vector').vector) < 300:
                log.warning(
                    f"SpaCy Language model ({slm.nlp._meta['name']}) doesn't contain 300D word2vec word vectors.")
                nlp = slm.nlp = slm.load('en_core_web_md')
        elif nlp.startswith('bert'):
            nlp = BertEncoder()
        else:
            nlp = st.SentenceTransformer('paraphrase-MiniLM-L6-v2')
    if isinstance(nlp, st.SentenceTransformer):
        nlp = nlp.encode  # returns a non Doc object, a vector
    return AnyNLP(nlp)


def is_regex(s):
    r""" Does the string contain regex-like characters and compile to a regular expression?

    >>> is_regex('[whatever](http://whatever.com)')
    regex.Regex(...)
    >>> is_regex('Hello Regex!')
    >>> is_regex('Hello Regex!\\')
    False
    """
    if '\\' in s or '[' in s or '|' in s or '.*' in s:
        try:
            return regex.compile(s)
        except (TypeError, regex._regex_core.error):
            return False


def replace(s, mapping=None):
    """ Like str.replace, but accepts a dictionary mapping regexes or strings to new strings """
    if not mapping:
        return s
    for k in mapping:
        if getattr(getattr(k, '__class__', k), '__name__', k) == 'Pattern':
            s = k.sub(mapping[k], s)
            continue
        k_isregex = is_regex(s)
        if k_isregex:
            k_isregex.sub(mapping[k], s)
            continue
        s.replace(k, mapping[k])


def unique_slugs(texts, lower=str.lower, strip=str.strip, replace={' ', ''}):
    """ Create a short, unique, human-readable summary for each of the texts provided """
    lower = lower if callable(lower) else str
    strip = strip if callable(strip) else str
    replace = replace if isinstance(replace, (abc.Mapping, pd.Series)) else str
    slugs = list(texts)
    for i, t in enumerate(texts):
        t = strip(str.replace(strip(lower(t)), replace))
        sluglen = min(len(t), 16)
        while sluglen < len(t) and t[:sluglen] in slugs:
            sluglen += 1
        if t[:sluglen] not in slugs:
            slugs[i] = t[:sluglen]
    return slugs


def get_similarity(texts1, texts2):
    model = st.SentenceTransformer('paraphrase-MiniLM-L6-v2')
    texts1 = [texts1] if isinstance(texts1, str) else texts1
    texts2 = [texts2] if isinstance(texts2, str) else texts2
    embeddings1 = model.encode(texts1, convert_to_tensor=True)
    embeddings2 = model.encode(texts2, convert_to_tensor=True)
    return pd.DataFrame(data=st.util.pytorch_cos_sim(embeddings1, embeddings2).numpy(),
                        index=unique_slugs(texts1),
                        columns=unique_slugs(texts2)
                        )


class DialogManager:
    def __init__(self):
        pass

    def random_reply(self,
                     skill,
                     statement,
                     dialog_tree_end_bot_statements,
                     dialog_tree_end_state_names,
                     welcome_state_name,
                     default_bot_username,
                     exit_bot_statements,
                     exit_state_turn_dict,
                     compose_statement):
        r""" Generates random replies for the dialog
        Except for the welcome state, all other states are mere recordings of the quiz responses
        """
        DIALOG_TREE_END_STATE_NAMES = dialog_tree_end_state_names
        DIALOG_TREE_END_BOT_STATEMENTS = dialog_tree_end_bot_statements
        WELCOME_STATE_NAME = welcome_state_name
        DEFAULT_BOT_USERNAME = default_bot_username
        EXIT_BOT_STATEMENTS = exit_bot_statements
        EXIT_STATE_TURN_DICT = exit_state_turn_dict
        if statement in DIALOG_TREE_END_BOT_STATEMENTS:
            statement = None

        # First check to see if we are in the time before the welcome state
        if skill.state in DIALOG_TREE_END_STATE_NAMES:
            # First figure out the welcome state name using a magical special WELCOME_STATE_NAME string
            # as the key. This will allow you to access the actual welcome turn
            skill.state = skill.turns[WELCOME_STATE_NAME]
            skill.current_turn = skill.turns[skill.state]
            index = 0
            if len(skill.current_turn['bot']) >= 1:
                index = random.randint(0, len(skill.current_turn['bot']) - 1)
            response = compose_statement(skill.current_turn['bot'][index])
        else:
            nxt_cndn = skill.current_turn['next_condition']

            nxt_cndn_match_mthd_dict = get_nxt_cndn_match_mthd_dict(nxt_cndn)
            # for match_method_keyword in ['EXACT', '']
            match_found = False
            for next_state_option in nxt_cndn_match_mthd_dict['EXACT']:
                match_found = check_match(statement, next_state_option, 'EXACT')
                if match_found:
                    break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['LOWER']:
                    match_found = check_match(statement, next_state_option, 'LOWER')
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['CASE_SENSITIVE_KEYWORD']:
                    match_found = check_match(
                        statement, next_state_option, 'CASE_SENSITIVE_KEYWORD'
                    )
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['KEYWORD']:
                    match_found = check_match(statement, next_state_option, 'KEYWORD')
                    if match_found:
                        break
            if not match_found:
                for next_state_option in nxt_cndn_match_mthd_dict['NORMALIZE']:
                    match_found = check_match(statement, next_state_option, 'NORMALIZE')
                    if match_found:
                        break
            if not match_found:
                index_with_highest_ratio = 0
                highest_ratio = 0
                index = 0
                for next_state_option in nxt_cndn_match_mthd_dict['SPACY']:

                    doc1 = slm.nlp(str(statement))
                    doc2 = slm.nlp(str(next_state_option[0]))
                    ratio = doc1.vector.dot(doc2.vector) / np.linalg.norm(doc1.vector) / np.linalg.norm(doc2.vector)
                    if (ratio >= highest_ratio):
                        highest_ratio = ratio
                        index_with_highest_ratio = index
                    index += 1
                if(highest_ratio > 0.5):
                    skill.state = nxt_cndn_match_mthd_dict['SPACY'][index_with_highest_ratio][1]
                    match_found = True
            if not match_found:
                index_with_highest_ratio = 0
                highest_ratio = 0
                index = 0
                if len(statement) > 15:
                    for next_state_option in nxt_cndn_match_mthd_dict['BAG-OF-WORDS']:
                        ratio = sentence_similarity(statement, next_state_option[0], None)
                        if (ratio >= highest_ratio):
                            highest_ratio = ratio
                            index_with_highest_ratio = index
                            index += 1
                if len(statement) <= 15:
                    for next_state_option in nxt_cndn_match_mthd_dict['BAG-OF-WORDS']:

                        doc1 = slm.nlp(str(statement))
                        doc2 = slm.nlp(str(next_state_option[0]))
                        ratio = doc1.vector.dot(doc2.vector) / np.linalg.norm(doc1.vector) / np.linalg.norm(doc2.vector)
                        if (ratio >= highest_ratio):
                            highest_ratio = ratio
                            index_with_highest_ratio = index
                            index += 1
                if(highest_ratio > 0.55):
                    skill.state = nxt_cndn_match_mthd_dict['BAG-OF-WORDS'][index_with_highest_ratio][1]
                    match_found = True
            if not match_found:
                model_class = BertModel
                tokenizer_class = BertTokenizer
                pretrained_weights = 'bert-base-multilingual-cased'
                tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
                model = model_class.from_pretrained(pretrained_weights)

                index_with_highest_ratio = 0
                highest_ratio = 0
                index = 0
                for next_state_option in nxt_cndn_match_mthd_dict['BERT']:

                    input_ids = torch.tensor([tokenizer.encode(str(statement))])
                    with torch.no_grad():
                        output_tuple = model(input_ids)
                        last_hidden_states = output_tuple[0]

                    input_ids1 = torch.tensor([tokenizer.encode(str(next_state_option[0]))])
                    with torch.no_grad():
                        output_tuple1 = model(input_ids1)
                        last_hidden_states1 = output_tuple1[0]

                    ratio = (
                        last_hidden_states[0][0].dot(last_hidden_states1[0][0])
                        / np.linalg.norm(last_hidden_states[0][0])
                        / np.linalg.norm(last_hidden_states1[0][0])
                    ).item()
                    if (ratio >= highest_ratio):
                        highest_ratio = ratio
                        index_with_highest_ratio = index
                    index += 1
                if(highest_ratio > 0.5):
                    skill.state = nxt_cndn_match_mthd_dict['BERT'][index_with_highest_ratio][1]
                    match_found = True
            if not match_found:
                skill.state = nxt_cndn_match_mthd_dict[None][0][1]

            skill.current_turn = skill.turns.get(skill.state, EXIT_STATE_TURN_DICT)
            index = 0
            if len(skill.current_turn.get(DEFAULT_BOT_USERNAME, EXIT_BOT_STATEMENTS)) >= 1:
                index = random.randint(0, len(skill.current_turn.get(DEFAULT_BOT_USERNAME, EXIT_BOT_STATEMENTS)) - 1)
            response = compose_statement(skill.current_turn.get(DEFAULT_BOT_USERNAME, EXIT_BOT_STATEMENTS)[index])

        return [(1.0, response)]

    # sentence transformers
    # create BERT vector
    # create your own cosine distance function


def cosine_similarity(v1, v2):
    np.array(v1).dot(np.array(v2)) / np.linalg.norm(v1) / np.linalg.norm(v2)


def cosine_distance(v1, v2):
    1.0 - cosine_similarity(v1, v2)


# incorporate nlp and .text bag of words similarity


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

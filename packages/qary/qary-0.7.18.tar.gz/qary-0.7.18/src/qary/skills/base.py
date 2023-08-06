""" Base classes for chatbot skills answering questions and executing rule-based dialog """
from copy import copy
import logging
import os
import uuid
from collections import namedtuple, abc
import zipfile

import pandas as pd
# from multiprocessing import cpu_count

from qary.etl.netutils import download_if_necessary
from qary.config import MIDATA_URL, MIDATA_QA_MODEL_DIR, DEFAULT_SKILL_CONFIDENCE, CLI_ARGS  # , USE_CUDA
from qary.etl.fileutils import LARGE_FILES
from qary.etl.nesting import dict_merge


log = logging.getLogger(__name__)

# tuple to hold confidence, text, and bot-name
BotReply_fields = ('confidence', 'text', 'skill', 'context')
BotReply = namedtuple('BotReply', BotReply_fields)  # noqa
BotReply.__new__.__defaults__ = (None,) * len(BotReply_fields)


def normalize_replies(replies):
    """ Make sure a list of replies includes score and text. TODO: confidences sum to 1

    >>> normalize_replies(['hello world']) == [BotReply(confidence=DEFAULT_SKILL_CONFIDENCE, text='hello world')]
    True
    >>> normalize_replies([])
    []
    >>> normalize_replies([BotReply()]) == [BotReply()]
    True
    >>> normalize_replies([(1, 'one')]) == [BotReply(1, 'one')]
    True
    >>> normalize_replies([(1, 'one'), BotReply(2.0, 'two')]) == [BotReply(1, 'one'), BotReply(2.0, 'two')]
    True
    """
    if isinstance(replies, BotReply):
        replies = [replies]
    elif isinstance(replies, str):
        replies = [(DEFAULT_SKILL_CONFIDENCE, replies)]
    elif isinstance(replies, (tuple, list)):
        if len(replies) == 1 and isinstance(replies[0], str):
            replies = [(DEFAULT_SKILL_CONFIDENCE, replies[0])]
        elif len(replies) == 2:
            if (isinstance(replies[0], (float, int)) and isinstance(replies[1], str)):
                replies = [BotReply(replies[0], replies[1])]
            elif (isinstance(replies[1], (float, int)) and isinstance(replies[0], str)):
                replies = [BotReply(replies[1], replies[0])]
    else:
        raise RuntimeError(
            f"The conversation manager requires a list or tuple of possible replies. Received {type(replies)}")
    # TODO: this sorting is likely unnecessary, redundant with sort happening within CLIBot.reply()
    normalized_replies = []
    for r in replies:
        if isinstance(r, BotReply):
            normalized_replies.append(r)
        elif isinstance(r, dict):
            normalized_replies.append(BotReply(**r))
        else:
            normalized_replies.append(BotReply(*r))
    return normalized_replies


class Replies(list):
    """ WIP: Container for 2-tuples of scored replies (strings)

    TODO:
        - override __getitem__ to return None when empty
        - validate method to make sure 2-tuples of float, str
        - normalize method to ensures scores add up to 1
        - softmax to improve likelihood of best replies
        - sort method?
    """
    pass


class ContextDict(dict):
    """ WIP: Container for context dict attributes for bots

    ContextDict.merge should use dict_merge

    SEE: https://stackoverflow.com/a/3233356/623735
    """

    def merge(self, other):
        dict_merge(self, other)

    def dict_merge(self, other):
        dict_merge(self, other)


class ContextSeries(pd.Series):
    """ WIP: Container for nested json-like object used to keep track of bot context

    API should be identical to ContextDict for .__getitem__
    dict-like object that iterates through the values of a mapping (like a Series)
    rather than the keys.
    """

    def __init__(self, obj, *args, dtype='O', **kwargs):
        super().__init__(obj, *args, dtype=dtype, **kwargs)

    def __iter__(self):
        for k, v in self.items():
            yield v


def update_dict(d, u):
    """ SEE: https://stackoverflow.com/a/3233356/623735 """
    for k, v in u.items():
        if isinstance(v, abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class EmptyRepliesBot:
    # def __init__(self, **kwargs):
    #     super().__init__()

    def reply(self, statement, context=None):
        """ Chatbot "main" function to respond to a user command or statement

        >>> bot = EmptyRepliesBot()
        >>> bot.reply('Hi')
        []
        """
        return []


class HiBot(EmptyRepliesBot):
    def reply(self, statement, context=None):
        """ Chatbot "main" function to respond to a user command or statement

        >>> bot = HiBot()
        >>> bot.reply('Hi')
        [(1.0, 'Hi!')]
        """
        s = statement.lower().strip().split()
        if s and s[0] in ('hi', 'hello', 'howdy', 'helo', 'yo'):
            return [(1.0, 'Hi!')]
        return []


class ContextBaseSkill:
    """ Manages self.context attribute with update_, reset_ and reply(context=...) methods

    >>> default_context = {'cli_args': {'config': None, 'debug': True, 'nickname': 'qary',
    ...     'num_top_replies': 10, 'use_cuda': False, 'persist': True, 'bots': ['glossary', 'faq', 'eliza'],
    ...     'verbosity': None, 'loglevel': 30, 'spacy_lang': 'en_core_web_md', 'wiki_title_max_words': 3,
    ...     'semantic': 1.0, 'spell': 0.2, 'words': [], 'qa_model': 'albert-large-v2-0.2.0',
    ...     'domains': None, 'glossary_domains': None, 'quiz_domains': None}}
    >>> conbot = ContextBaseSkill()
    >>> conbot.context == default_context
    True
    >>> default_context.update({'init': 'init_value'})
    >>> conbot = ContextBaseSkill({'init': 'init_value'})
    >>> conbot.context == default_context
    True
    >>> conbot.update_context({'new': 'new_value', 'cli_args': None, 'args': None, 'kwargs': None})
    {'cli_args': None, 'init': 'init_value', 'new': 'new_value', 'args': None, 'kwargs': None}
    >>> conbot.context
    {'cli_args': None, 'init': 'init_value', 'new': 'new_value', 'args': None, 'kwargs': None}
    >>> conbot.update_context({'init': 'updated_existing', 'new': {'inner': 'new_innards'}})
    {'cli_args': None, 'init': 'updated_existing', 'new': {'inner': 'new_innards'}, 'args': None, 'kwargs': None}
    >>> conbot.context
    {'cli_args': None, 'init': 'updated_existing', 'new': {'inner': 'new_innards'}, 'args': None, 'kwargs': None}
    >>> conbot.reply('Hi', context={'new': {'inner_reply': 'new_inner_reply'}})
    []
    >>> conbot.context['init']
    'updated_existing'
    >>> conbot.context['new']
    {'inner': 'new_innards', 'inner_reply': 'new_inner_reply'}
    """

    def __init__(self, context=None, cli_args=CLI_ARGS, *args, **kwargs):
        # FIXME: ContextBaseSkill should only handle context, nothing else
        self.context = {}
        self.update_context(kwargs or {})
        try:
            cli_args = vars(cli_args)
        except AttributeError:
            cli_args = dict(cli_args or {})
        self.update_context(context={'cli_args': cli_args})
        if isinstance(context, str):
            log.warning("Deprecated API: `context` should be a nested dictionary. Texts belong at `context['doc']['text']`).")
            self.update_context({'doc': {'text': str(context)}})
        elif context and len(context):
            self.update_context(dict(context))
        super().__init__()

    def update_context(self, context=None):
        # defensive programming in case of: skill.context = None | ''
        self.context = getattr(self, 'context', {}) or {}
        if not isinstance(self.context, (abc.Mapping, ContextDict)):
            log.error(f'self.context is not a dict! self.context: {self.context}')
            self.context = dict(self.context)

        log.warning(f"Updating self.context using context: {repr(context)[:61]}...")
        if isinstance(context, str):
            context = {'doc': {'text': context}}
        context = {} if not context else dict(context)

        dict_merge(self.context, context)
        log.debug(f"Updated self.context: {repr(self.context)[:60]}")
        return self.context

    def reset_context(self, context=None):
        self.context = {k: copy(self.context[k]) for k in self.context if k in ['cli_args', 'args', 'kwargs']}
        log.info(f"Reset self.context to self.context={repr(self.context)[:60]} before updating with {repr(context)[:60]}")
        self.update_context(context=context)
        return self.context

    def reply(self, statement, context=None):
        """ Chatbot "main" function to respond to a user command or statement

        >>> s = ContextBaseSkill()
        >>> s.reply('Hi', context={'new': 'context'})
        []
        >>> s.context['new']
        'context'
        >>> list(s.context.keys())
        ['cli_args', 'new']
        """
        log.warning(f'base.ContextBaseSkill context={context}')
        self.update_context(context=context)
        return []


class HistoryBot:
    """ Remembers the history of every user statement and bot response string

    >>> histbot = HistoryBot()
    >>> histbot.history
    []
    >>> histbot.update_history('Hi')
    1
    >>> histbot.history
    [{'statement': 'Hi', 'possible_statements': (), 'agent': None}]
    >>> histbot.update_history('Hello', agent='human')
    2
    >>> histbot.history
    [{'statement': 'Hi', 'possible_statements': (), 'agent': None},
     {'statement': 'Hello', 'possible_statements': (), 'agent': 'human'}]
    """

    def __init__(self, history=None, **kwargs):
        super().__init__(**kwargs)
        self.history = history or []

    def update_history(self, statement=None, possible_statements=None, agent=None):
        """ Append convo history with a statement/reply, the possibilities it was chosen from, and an agent (bot/user) name """
        self.history.append(dict(
            statement=statement,
            possible_statements=tuple(possible_statements or []),
            agent=agent))
        return len(self.history)

    def reset_history(self, statement=None, possible_statements=None, agent=None):
        """ Reset conversation history to a single statement/reply

        Resets the conversation history to the last interaction:
            - a single most recent reply
            - the possibile Skill replies list that the reply was chosen from
            - the Skills that created the list of possible replies
        """
        self.history = []
        if statement or possible_statements or agent:
            self.update_history(
                statement=statement,
                possible_statements=possible_statements,
                agent=agent)
        return len(self.history)


class TransformerBot(HistoryBot, ContextBaseSkill):
    """ Base Skill class that maintains context and load transformer models.  """

    def __init__(self, context=None, cli_args=CLI_ARGS, history=None, **kwargs):
        super().__init__(context=context, cli_args=CLI_ARGS, history=history, **kwargs)

    def load_model(self, args):
        self.transformer_loggers = []
        for name in log.root.manager.loggerDict:
            if (len(name) >= 12 and name[:12] == 'transformers') or name == 'qary.skills.qa.utils':
                self.transformer_loggers.append(log.getLogger(name))
                self.transformer_loggers[-1].setLevel(log.ERROR)

        qa_model = args.qa_model
        url_str = f"{MIDATA_URL}/{MIDATA_QA_MODEL_DIR}/{qa_model}.zip"
        log.warning(f"Attempting to download url: {url_str}")
        model_dir = os.path.dirname(LARGE_FILES['albert-large-v2']['path'])
        model_type = qa_model.split('-')[0].lower()
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)

        if not all((
            os.path.exists(os.path.join(model_dir, 'config.json')),
            os.path.exists(os.path.join(model_dir, 'pytorch_model.bin')),
            os.path.exists(os.path.join(model_dir, 'tokenizer_config.json')),
            os.path.exists(os.path.join(model_dir, 'version.json')),
            any((model_type == 'bert' and os.path.exists(os.path.join(model_dir, 'vocab.txt'))),
                (model_type == 'albert' and os.path.exists(os.path.join(model_dir, 'spiece.model')))),
        )):
            zip_local_path = download_if_necessary(
                url=LARGE_FILES['albert-large-v2']['url'],
                path=LARGE_FILES['albert-large-v2']['path'])
            with zipfile.ZipFile(zip_local_path, 'r') as zip_file:
                zip_file.extractall(os.path.dirname(LARGE_FILES['albert-large-v2']['path']))
            os.remove(zip_local_path)

    def encode_transformer_input(self, statement, context=None):
        """ Convert statement and context strings into nested dict format compatible with [AL]BERT transformer

        >>> bot = TransformerBot()
        >>> encoded = bot.encode_transformer_input('statement', 'context')
        >>> encoded[0]['qas'][0]['question']
        'statement'
        >>> encoded[0]['context']
        'context'
        """
        if context is None:
            context = self.context
        if isinstance(context, str):
            # TODO try/except on [] instead of get to provide deprecation warnings
            text = context
            super().update_context({'doc': {'text': text}})
        else:
            super().update_context(context)
        text = self.context['doc']['text']
        encoded = [{
            'qas': [{
                'id': str(uuid.uuid1()),
                'question': statement
            }],
            'context': text}]
        return encoded

    def decode_transformer_output(self, output):
        """ Extract reply string from the transformer model's prediction output (nested dict)

        >>> bot = TransformerBot()
        >>> bot.decode_transformer_output([{'id': 'unique_id', 'answer': 'response', 'probability': 0.75}])
        (0.75, 'response')
        """
        return output[0]['probability'], output[0]['answer']

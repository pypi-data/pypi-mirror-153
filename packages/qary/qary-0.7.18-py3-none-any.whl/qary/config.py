""" Merge default configuration values for qary from a text file with command line args, and constants.* """
try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping
from decimal import Decimal
import datetime
import logging
import os
from pytz import timezone
import string
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import spacy  # noqa
import configargparse
from environment import Environment
import django.conf

from qary import __version__
from qary.constants import HOME_DIR, BASE_DIR  # noqa
from qary.constants import *

# TODO: Do Django SECRET_KEY and any AWS/RASA/DO keys need to be integrated into env here?
env = Environment(spacy_lang=str, loglevel=int, name=str)

LOGLEVEL = logging.ERROR

DIALOG_TREE_END_STATE_NAMES = (None, False, 0, '', ''.encode(), '0', 'none', 'None')
DIALOG_TREE_END_BOT_STATEMENTS = (None, 'none', )
WELCOME_STATE_NAME = '__WELCOME__'
FINISH_STATE_NAME = '__FINISH__'
DEFAULT_STATE_NAME = '__default__'
DEFAULT_BOT_USERNAME = 'bot'
EXIT_STATE_NAME = None
EXIT_BOT_STATEMENTS = ['Session is already over! Type "quit" to exit or press "Enter" for a new session']
EXIT_STATE_TURN_DICT = {'state': EXIT_STATE_NAME, DEFAULT_BOT_USERNAME: EXIT_BOT_STATEMENTS}

MIDATA_DOMAINNAME = 'tan.sfo2.digitaloceanspaces.com'
MIDATA_URL = f'https://{MIDATA_DOMAINNAME}'
MIDATA_QA_MODEL_DIR = 'midata/public/models/qa'
MIDATA_QA_MODEL_DIR_URL = f'{MIDATA_URL}{MIDATA_QA_MODEL_DIR}'
ARTICLES_URL = f'{MIDATA_URL}/midata/public/corpora/wikipedia/articles_with_keywords.pkl'

USE_CUDA = False
MAX_TURNS = 10000
DEFAULT_SKILL_CONFIDENCE = .667


DEFAULT_CONFIG = {
    'name': 'bot',
    'persist': 'False',  # Yes, yes, 1, Y, y, T, t
    'bots': 'glossary',  # glossary,qa,parul,eliza,search_fuzzy'
    'spacy_lang': 'en_core_web_md',
    'use_cuda': USE_CUDA,
    'loglevel': 0,  # 0 allows the user to set a value 10-50 (lower more verbose)
    'num_top_replies': 10,
    'self_score': '.5',
    'semantic_score': '.5',
    'debug': True,
    'wiki_title_max_words': 4,
    'score_weights': '{"spell": .25, "semantic": .5}',
    'qa_model': 'albert-large-v2-0.2.0',
}
DEFAULT_CONFIG.update(env.parsed)

LOGLEVELS = [
    logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.FATAL]
# LOG_LEVELS = [         10,           20,              30,            40,            50]
LOGLEVEL_NAMES = 'DEBUG INFO WARNING ERROR FATAL'.split()
LOGLEVEL_ABBREVIATIONS = [s[:4].lower() for s in LOGLEVEL_NAMES]
LOGLEVEL_ABBR_DICT = dict(zip(LOGLEVEL_ABBREVIATIONS, LOGLEVELS))
# this is the LOGLEVEL for the top of this file, once CLI_ARGS and .ini file are read, it will change
LOGLEVEL = getattr(env, 'loglevel', DEFAULT_CONFIG.get('loglevel', logging.WARNING))
USE_CUDA = getattr(env, 'use_cuda', DEFAULT_CONFIG.get('use_cuda', USE_CUDA))


LOGGING_FORMAT = '%(asctime)s.%(msecs)d %(levelname)-4s %(filename)s:%(lineno)d %(message)s'
LOGGING_DATEFMT = '%Y-%m-%d:%H:%M:%S'
LOGGING_LEVEL = logging.ERROR
logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOGGING_DATEFMT,
    level=LOGGING_LEVEL)
log = logging.getLogger(__name__)
root_logger = logging.getLogger()

log.info(f'Running {__name__} version {__version__} ...')


# TZ constants
DEFAULT_TZ = timezone('UTC')

MAX_LEN_FILEPATH = 1023  # on OSX `open(fn)` raises OSError('Filename too long') if len(fn)>=1024

ROUNDABLE_NUMERIC_TYPES = (float, int, Decimal, bool)
FLOATABLE_NUMERIC_TYPES = (float, int, Decimal, bool)
BASIC_NUMERIC_TYPES = (float, int)
NUMERIC_TYPES = (float, int, Decimal, complex, str)  # datetime.datetime, datetime.date
NUMBERS_AND_DATETIMES = (float, int, Decimal, complex, str)
SCALAR_TYPES = (float, int, Decimal, bool, complex, str)  # datetime.datetime, datetime.date
# numpy types are derived from these so no need to include numpy.float64, numpy.int64 etc
DICTABLE_TYPES = (Mapping, tuple, list)  # convertable to a dictionary (inherits Mapping or is a list of key/value pairs)
VECTOR_TYPES = (list, tuple)
PUNC = str(string.punctuation)

# synonyms for "count"
COUNT_NAMES = ['count', 'cnt', 'number', 'num', '#', 'frequency', 'probability', 'prob', 'occurences']
# 4 types of

BIG_DATASETS_MANIFEST_URL = 'https://gitlab.com/tangibleai/qary/-/raw/main/src/qary/data/datasets.yml?inline=false'
log.debug(f'BIG_DATASETS_MANIFEST_URL={BIG_DATASETS_MANIFEST_URL}')

HOME_DATA_DIR = HOME_DIR / '.qary-data'
DATA_DIR = HOME_DATA_DIR
log.warning(f'DATA_DIR=HOME_DATA_DIR={HOME_DATA_DIR}')

DEFAULT_DIALOG_FILEPATH = Path(DATA_DIR) / 'writing/ogden-script.v2.dialog.yml'


# FIXME: functions like this should not be in constants.py
def parse_args(args):
    """Parse command line parameters using qary.ini for the default values

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """

    parser = configargparse.ArgParser(
        default_config_files=[
            '~/qary.ini',
            os.path.join(DATA_DIR, '*.ini'),
        ],
        description="Command line bot application. Try `$ bot how do you work?`")
    parser.add('-c', '--config', required=False, is_config_file=True,
               help="Config file path (default: ~/qary.ini)")
    parser.add_argument(
        '-d', '--debug',
        help="Set DEBUG logging level and raise more exceptions immediately.",
        dest="debug",
        default=str(DEFAULT_CONFIG['debug'])[0].lower() in 'fty1p',
        action='store_true')
    parser.add_argument(
        '--version',
        action='version',
        version='qary {ver}'.format(ver=__version__))
    parser.add_argument(
        '--name',
        default=None,  # DEFAULT_CONFIG['name'],
        dest="nickname",
        help="IRC nick or CLI command name for the bot",
        type=str,
        metavar="STR")
    parser.add_argument(
        '-n',
        '--num_top_replies',
        default=None,  # DEFAULT_CONFIG['num_top_replies'],
        dest="num_top_replies",
        help="Limit on the number of top (high score) replies that are randomly selected from.",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-u',
        '--use_cuda',
        help="Use CUDA and GPU to speed up transformer inference.",
        dest='use_cuda',
        default=USE_CUDA,
        action='store_true')
    parser.add_argument(
        '-p',
        '--persist',
        help="DEPRECATED: Don't exit. Retain language model in memory and maintain dialog until user says 'exit' or 'quit'",
        dest='persist',
        default=str(DEFAULT_CONFIG['persist'])[0].lower() in 'fty1p',
        action='store_true')
    parser.add_argument(
        '-b',
        '--bots',
        default=None,  # DEFAULT_CONFIG['bots'],  # None so config.ini can populate defaults
        dest="bots",
        help="Comma-separated list of bot personalities to load. Defaults: pattern,parul,search_fuzzy,time,eliza",
        type=str,
        metavar="STR")
    parser.add_argument(
        '-s',
        '--skills',
        default=None,  # DEFAULT_CONFIG['bots'],  # None so config.ini can populate defaults
        dest="bots",
        help="Comma-separated list of bot personalities to load. Defaults: pattern,parul,search_fuzzy,time,eliza",
        type=str,
        metavar="STR")
    parser.add_argument(
        '-q',
        '--quiet',
        dest="verbosity",
        help="Quiet: set loglevel to ERROR",
        action='store_const',
        const=logging.ERROR)
    parser.add_argument(
        '-qq',
        '--very_quiet',
        dest="verbosity",
        help="Very quiet: set loglevel to FATAL",
        action='store_const',
        const=logging.FATAL)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="verbosity",
        help="Verbose: set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very_verbose',
        dest="verbosity",
        help="Verty verbose: set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    parser.add_argument(
        '-l',
        '--loglevel',
        dest="loglevel",
        help="Raw integer loglevel (10=debug, 20=info, 30=warn, 40=error, 50=fatal)",
        type=int,
        default=0)  # DEFAULT_CONFIG['loglevel'])
    parser.add_argument(
        '--spacy_lang',
        default=None,  # None allows ini to set default
        dest="spacy_lang",
        help="SpaCy language model: en_core_web_sm, en_core_web_md, or en_core_web_lg",
        type=str,
        metavar="STR")
    parser.add_argument(
        '--wiki_title_max_words',
        default=DEFAULT_CONFIG['wiki_title_max_words'],
        dest="wiki_title_max_words",
        help='Maximum n-gram length (in tokens) for wikipedia article title guesses.',
        type=int,
        metavar="INT")
    parser.add_argument(
        '--semantic',
        type=float,
        default=1.0,
        dest='semantic',
        metavar='FLOAT',
        help='set weight of the semantic quality score')
    parser.add_argument(
        '--spell',
        type=float,
        default=0.2,
        dest='spell',
        metavar='FLOAT',
        help='set weight of the spell quality score')
    parser.add_argument(
        'words',
        type=str,
        nargs='*',
        help="Words to pass to bot as an utterance or conversational statement requiring a bot reply or action.")
    parser.add_argument(
        '--qa_model',
        help="Select which model qa_bots will use",
        dest='qa_model',
        default=DEFAULT_CONFIG['qa_model'],
        type=str,
        metavar='STR')
    parser.add_argument(
        '--domains',
        '--faq_domains', '--faq-domains', '--faq_domain', '--faq-domain', '--faq',
        help="Input file keywords (domain names) for FAQ skill. For example 'data,life'.",
        type=str,
        metavar='STR')
    parser.add_argument(
        '--glossary_domains', '--glossary-domains', '--glossary_domain', '--glossary-domain', '--glossary',
        help="Input file keywords (domain names) for Glossary skill. For example 'data,dsdh,ucsd,nlpia'.",
        type=str,
        metavar='STR')
    parser.add_argument(
        '--quiz_domains', '--quiz-domains', '--quiz_domain', '--quiz-domain', '--quiz',
        help="Input file keywords (domain names) for Quiz skill. For example 'intern,python'.",
        type=str,
        metavar='STR')
    parsed_args = parser.parse_args(args)

    return parsed_args


def setup_logging(loglevel=LOGLEVEL):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    global LOGLEVEL, log, root_logger

    logformat = '%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    logdatefmt = "%Y-%m-%d%H:%M:%S"
    root_logger.setLevel(loglevel)
    logging.basicConfig(level=loglevel)
    # FIXME: this doesn't seem to change things, the original format and level set at top of file rules
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt=logdatefmt)
    # set the root logger to the same log level
    logging.getLogger().setLevel(loglevel)


def parse_argv(argv=sys.argv):
    """ Parse the command line args and ini file. Business logic to resolve conflicting arg values """
    global BOT, USE_CUDA, log

    new_argv = []
    if len(argv) > 1:
        command_line_path = str(argv[0]).lower().strip()
        if command_line_path.endswith('qary') or command_line_path.endswith('bot'):
            new_argv.extend(list(argv[1:]))
    else:
        log.info(f"It doesn't look like you're running this as a command line application. sys.argv: {argv}")
    args = parse_args(args=new_argv)

    # consolidate the 2 synonymous args, loglevel and verbosity, by using the minimum of the 2
    #   loglevel may be set by the ini file or the command line arg loglevel
    #   verbosity may only be set by the command line args -v/verbose -qq -vv and -q/quiet
    #   The more verbose of the 2 (lower loglevel value) wins

    loglevel = min(args.loglevel or 0, args.verbosity or 0) or logging.WARNING
    setup_logging(loglevel=loglevel)
    log.debug(f'RAW CLI_ARGS (including config file): {vars(args)}')
    args.loglevel = loglevel

    # strip quotes in case ini file incorrectly uses single quotes that become part of the str
    args.nickname = str(args.nickname).strip().strip('"').strip("'")
    args.bots = 'glossary,qa' if getattr(args, 'bots', getattr(args, 'skills', None)) is None else args.bots
    args.bots = [m.strip() for m in args.bots.split(',')]
    log.debug(f"Building a BOT with: {args.bots}")

    USE_CUDA = args.use_cuda

    return args


try:
    # This will fail if another application (like gunicorn) imports qary and redirects stdin without
    # running it as a command line app
    print()  # can't log anything until we know what the user's log level is.
    # print(f"sys.argv: {sys.argv}")
    CLI_ARGS = parse_argv(argv=sys.argv)
except Exception as e:  # noqa
    log.info(e)
    log.info('Unable to parse command line arguments. Are you trying to import this into gunicorn?')
    # Workaround for the bug when Django app tries to import qary.config:
    # `usage: gunicorn [-h] [-c CONFIG] ... gunicorn: error: unrecognized arguments
    CLI_ARGS = vars(parse_argv(argv=[]))


LOGLEVEL = CLI_ARGS.loglevel or LOGLEVEL


# handler = logging.handlers.TimedRotatingFileHandler(os.path.join(LOG_DIR, 'qary.config.log'), when='midnight')
# handler.setLevel(logging.INFO)
# log.addHandler(handler)


LANGS = ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']
LANGS_ABBREV = 'en enmd enlg'.split()
LANGS += 'de_core_news_sm de_core_news_md de_trf_bertbasecased_lg'.split()
LANGS_ABBREV += 'de demd delg'.split()
LANGS_ABBREV = dict(zip(LANGS_ABBREV, LANGS))

LANG = getattr(CLI_ARGS, 'spacy_lang', None) or DEFAULT_CONFIG.get('spacy_lang') or LANGS[0]
log.info(f'LANG=spacy_lang={LANG}')

ASCII_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPER = ASCII_LOWER.upper()


# clibot.py
DEFAULT_SKILLS = ['pattern']  # 'search_fuzzy', 'parul', 'eliza', 'glossary', 'qa'

SKILLS = CLI_ARGS.bots

if isinstance(CLI_ARGS.domains, str):
    FAQ_DOMAINS = DOMAINS = CLI_ARGS.domains.split(',')
else:
    FAQ_DOMAINS = DOMAINS = ('python-data-science',)
if isinstance(CLI_ARGS.glossary_domains, str):
    GLOSSARY_DOMAINS = CLI_ARGS.glossary_domains.split(',')
else:
    GLOSSARY_DOMAINS = ('',)
if isinstance(CLI_ARGS.quiz_domains, str):
    QUIZ_DOMAINS = CLI_ARGS.quiz_domains.split(',')
else:
    QUIZ_DOMAINS = ('',)

FAQ_MIN_SIMILARITY = 0.85
FAQ_MAX_NUM_REPLIES = 3

TFHUB_USE_MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder-large/3"

# # templates for medical sentences
# SENTENCE_SPEC_PATH = os.path.join(DATA_DIR, 'medical_sentences.json')
# SENTENCE_SPEC = json.load(open(SENTENCE_SPEC_PATH, 'r'))


# Universal Sentence Encoder's TF Hub module for creating USE Embeddings from
USE = None


def set_django_settings(settings=None):
    DATABASES = {
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
        'postgres': {
            'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
            'USER': os.environ.get('SQL_USER', 'user'),
            'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
            'HOST': os.environ.get('SQL_HOST', 'localhost'),
            'PORT': os.environ.get('SQL_PORT', '5432'),
        }
    }
    DATABASES['default'] = DATABASES['sqlite']
    settings = {'DATABASE_' + k: v for (k, v) in DATABASES['default'].items()}
    settings['TIME_ZONE'] = 'America/Los_Angeles'
    try:
        django.conf.settings.configure(**settings)
    except RuntimeError:  # RuntimeError('Settings already configured.')
        pass
    return django.conf.settings


django_settings = set_django_settings()


uri_schemes_popular = ['http', 'https', 'telnet', 'mailto',
                       'udp', 'ftp', 'ssh', 'git', 'apt', 'svn', 'cvs', 'hg',
                       'smtp', 'feed',
                       'example', 'content',
                       'gtalk', 'chrome-extension',
                       'bitcoin'
                       ]

# these may not all be the sames isinstance types, depending on the env
FLOAT_TYPES = tuple([t for t in set(np.sctypeDict.values()) if t.__name__.startswith('float')] + [float])
FLOAT_DTYPES = tuple(set(np.dtype(typ) for typ in FLOAT_TYPES))
INT_TYPES = tuple([t for t in set(np.sctypeDict.values()) if t.__name__.startswith('int')] + [int])
INT_DTYPES = tuple(set(np.dtype(typ) for typ in INT_TYPES))
NUMERIC_TYPES = tuple(set(list(FLOAT_TYPES) + list(INT_TYPES)))
NUMERIC_DTYPES = tuple(set(np.dtype(typ) for typ in NUMERIC_TYPES))

DATETIME_TYPES = [t for t in set(np.sctypeDict.values()) if t.__name__.startswith('datetime')]
DATETIME_TYPES.extend([datetime.datetime, pd.Timestamp])
DATETIME_TYPES = tuple(DATETIME_TYPES)

DATE_TYPES = (datetime.datetime, datetime.date)

# matrices can be column or row vectors if they have a single col/row
VECTOR_TYPES = (list, tuple, np.matrix, np.ndarray)
MAPPING_TYPES = (Mapping, pd.Series, pd.DataFrame)

# These are the valid dates for all 3 datetime types in python (and the underelying integer nanoseconds)
INT_MAX = INT64_MAX = 2 ** 63 - 1
INT_MIN = INT64_MIN = - 2 ** 63
UINT_MAX = UINT64_MAX = - 2 ** 64 - 1

INT32_MAX = 2 ** 31 - 1
INT32_MIN = - 2 ** 31
UINT32_MAX = - 2 ** 32 - 1

INT16_MAX = 2 ** 15 - 1
INT16_MIN = - 2 ** 15
UINT16_MAX = - 2 ** 16 - 1

# Pandas timestamps can handle nanoseconds? but python datetimestamps cannot.
MAX_TIMESTAMP = pd.Timestamp('2262-04-11 23:47:16.854775', tz='utc')
MIN_TIMESTAMP = pd.Timestamp(datetime.datetime(1677, 9, 22, 0, 12, 44), tz='utc')
ZERO_TIMESTAMP = pd.Timestamp('1970-01-01 00:00:00', tz='utc')

# to_pydatetime() rounds to microseconds, ignoring 807 nanoseconds available in other MAX TIMESTAMPs
MIN_DATETIME = MIN_TIMESTAMP.to_pydatetime()
MAX_DATETIME = MAX_TIMESTAMP.to_pydatetime()
MIN_DATETIME64 = MIN_TIMESTAMP.to_datetime64()
MAX_DATETIME64 = MAX_TIMESTAMP.to_datetime64()
INF = np.inf
NAN = np.nan
NAT = pd.NaT


# str constants
MAX_CHR = MAX_CHAR = chr(127)
APOSTROPHE_CHARS = "'`’"
# Monkey patch so import from constants if you want this:
string.unprintable = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0e\x0f' \
    '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f'
ASCII_UNPRINTABLE_CHRS = string.unprintable  # ''.join(chr(i) for i in range(128) if chr(i) not in string.printable)

NULL_VALUES = set(['0', 'None', 'null', "'", ""] + ['0.' + z for z in ['0' * i for i in range(10)]])
# if datetime's are 'repr'ed before being checked for null values sometime 1899-12-30 will come up
NULL_REPR_VALUES = set(['datetime.datetime(1899, 12, 30)'])
# to allow NULL checks to strip off hour/min/sec from string repr when checking for equality
MAX_NULL_REPR_LEN = max(len(s) for s in NULL_REPR_VALUES)

PERCENT_SYMBOLS = ('percent', 'pct', 'pcnt', 'pt', r'%')
FINANCIAL_WHITESPACE = ('Flat', 'flat', ' ', ',', '"', "'", '\t', '\n', '\r', '$')
FINANCIAL_MAPPING = (('k', '000'), ('M', '000000'))

# pugnlp.constants
#####################################################################################

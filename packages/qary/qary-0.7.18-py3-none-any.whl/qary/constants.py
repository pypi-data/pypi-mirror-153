""" Hard coded configuration values such as HOME_DIR and DATA_DIR that never change """
import logging
from pathlib import Path
import sys

# FIXME: why is this here?
import spacy  # noqa

from qary import __version__  # noqa
from qary.data.constants.nltk_stopwords_english import STOPWORDS


log = logging.getLogger(__name__)


sys.path = [str(Path(__file__).parent)] + sys.path


HOME_DIR = Path.home()
PACKAGE_DIR = QARY_DIR = Path(__file__).resolve().absolute().parent
SRC_DIR = QARY_DIR.parent
REPO_DIR = BASE_DIR = SRC_DIR.parent
if SRC_DIR.name == 'src':
    REPO_DIR = SRC_DIR.parent
else:
    REPO_DIR = BASE_DIR = SRC_DIR = QARY_DIR

STOPWORDS_DICT = dict(zip(STOPWORDS, [1] * len(STOPWORDS)))
QUESTIONWORDS = set('who what when were why which how'.split() + ['how come', 'why does', 'can i', 'can you', 'which way'])
QUESTION_STOPWORDS = QUESTIONWORDS | STOPWORDS

""" Hard coded configuration values such as HOME_DIR and DATA_DIR that never change """
import logging
from pathlib import Path
import sys

# FIXME: why is this here?
import spacy  # noqa

from qary import __version__


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


DATA_MANIFEST_URL = 'https://gitlab.com/tangibleai/qary/-/raw/main/src/qary/data/datasets.yml?inline=false'
print(f'DATA_MANIFEST_URL={DATA_MANIFEST_URL}')
DATA_DIR = Path.home() / '.qary-data'
print(f'DATA_DIR={DATA_DIR}')

HOME_DIR = Path.home()
log.debug(f'Running {__name__} version {__version__} ...')
LOGLEVEL = logging.ERROR

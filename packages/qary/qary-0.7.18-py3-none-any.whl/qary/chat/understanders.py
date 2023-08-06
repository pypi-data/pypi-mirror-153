""" Processes *.dialog.v2.yml files to define Finite State Machine rules """
# from qary.chat.dialog import TurnsPreparation, compose_statement, load_dialog_turns
import logging

from ..etl.utils import squash_wikititle, normalize_wikititle, slugify, simple_tokenize
from ..spacy_language_model import tokenize

from . import matchers

log = logging.getLogger(__name__)


def check_match(statement, next_state_option, match_condition):
    """ Return the next

    Args:
      statement (str): actual human statement at this dialog turn
      next_state_option (tuple) = (possible_statement_of_intent, destination_state_name)

    >>> check_match(' Yes! ', ('yes', 'q1_normalize'), match_condition='normalize')
    (True, 'q1_normalize')
    """
    intent, next_state = next_state_option
    statement = str(statement or '')

    ######################################################
    # FIXME: move to preprocessing functions in module containing load_dialog_script preprocessing:
    match_condition = match_condition.upper().strip()

    # Special cases for reverse compatability with v2 of convoscript spec
    # v2 convoscript used by Jose in quiz.py test examples
    if match_condition in 'KEYWORD LOWER'.split():
        match_condition = 'KEYWORD_LOWER'
        log.warning('DEPRECATED: Use KEYWORD_LOWER instead of KEYWORD or LOWER for case insensitive KEYWORD match.')
    elif match_condition == 'NORMALIZE':
        match_condition = 'KEYWORD_NORMALIZE'
        log.warning('DEPRECATED: Use EXACT_NORMALIZE or KEYWORD_NORMALIZE instead of NORMALIZE.')
    elif match_condition == 'CASE_SENSITIVE_KEYWORD':
        match_condition = 'KEYWORD_EXACT'
        log.warning('DEPRECATED: Use KEYWORD_EXACT instead of CASE_SENSITIVE_KEYWORD.')
    next_state = next_state_option[1]

    # preprocessing
    statement, intent = statement.strip(), intent.strip()
    match_condition_tokens = match_condition.split('_')
    if 'LOWER' in match_condition_tokens:
        statement, intent = statement.lower(), intent.lower()
    if 'NORMALIZE' in match_condition_tokens:
        statement, intent = [normalize_wikititle(s) for s in (statement, intent)]
    if 'SLUGIFY' in match_condition_tokens:
        statement, intent = [slugify(s) for s in (statement, intent)]
    if 'SQUASH' in match_condition_tokens:
        statement, intent = [squash_wikititle(s) for s in (statement, intent)]
    if 'TOKENIZE' in match_condition_tokens:
        statement = [tokenize(s) for s in (statement, intent)]
    if any(s in match_condition_tokens for s in 'SIMPLETOKENIZE RETOKENIZE REGEXTOKENIZE'.split()):
        statement = [simple_tokenize(s) for s in (statement, intent)]

    #
    #######################################################

    # condition matching
    if getattr(matchers, (match_condition_tokens[0] or 'default').lower().strip())(statement, intent):

        return True, next_state

    return False, '__finish__'

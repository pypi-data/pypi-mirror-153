""" Rule-based (intent recognition and templated responses) chatbot dialog engine for quizzes """
import logging

from qary.config import QUIZ_DOMAINS
from qary.init import maybe_download
# from qary.skills.base import ContextBaseSkill

from qary.chat import dialog
from qary.chat.dialog import generate_domain_filepaths, get_nxt_cndn_match_mthd_dict
from qary.chat.understanders import check_match
from qary.config import WELCOME_STATE_NAME
# import TurnsPreparation, compose_statement, load_dialog_turns

# FIXME: dialog.TurnsPreparation is incompatible with the local one defined here
# from qary.chat.dialog import TurnsPreparation

# FIXME: make this a config option
# INTERN_QUIZ = os.path.join(DATA_DIR, 'yes_no/intern_quiz.yml')
INTERN_QUIZ = generate_domain_filepaths(
    domains=QUIZ_DOMAINS, prefix='', suffix='.input.dialog', ext='.yml')
INTERN_QUIZ = maybe_download(filename='testsets/dialog_parser.input.dialog.yml')


log = logging.getLogger(__name__)


class Skill:
    r"""Skill for Quiz"""

    def __init__(self, datafile=None, turns_list=None, use_nlp=False):
        """If datafile is not given, the turns list of dicts can directly be passed to seed the data
        This would be useful for testing purposes and such
        """
        self.datafile = datafile
        self.turns = {}
        self.turns_input = turns_list
        self.use_nlp = use_nlp
        # if turns is passed, then you should not set the datafile
        if not turns_list:
            datafile = datafile or INTERN_QUIZ
            self.turns_input = dialog.load_dialog(datafile)

        if self.turns_input:
            # Do more complex operations using the helper '_TurnsPreparation' class
            turns_preparation = dialog.TurnsPreparation(turns_list=self.turns_input, use_nlp=self.use_nlp)
            self.turns = turns_preparation.prepare_turns()
        else:  # some sort of error
            log.error('An empty turns_list was passed to quiz.Skill.__init__()')
        self.state = None
        self.current_turn = None
        return

    def find_next_state(self, statement, method, nxt_cndn_match_mthd_dict):
        for next_state_option in nxt_cndn_match_mthd_dict[method]:
            match_response = check_match(
                statement, next_state_option, method
            )

            match_found = match_response[0]
            self.state = match_response[1]

            if match_found:
                return match_found

    def reply(self, statement, context=None):
        r"""Except for the welcome state, all other states are mere recordings of the quiz responses

        Examples:
            #TODO
        """
        if statement in [None, 'none']:
            statement = None

        # First check to see if we are in the time before the welcome state
        if self.state in (None, False, 0, '', ''.encode(), '0', 'none', 'None'):
            # First figure out the welcome state name using a magical special '__WELCOME__' string
            # as the key. This will allow you to access the actual welcome turn
            self.state = self.turns[WELCOME_STATE_NAME]
            self.current_turn = self.turns[self.state]
            response = '\n'.join(self.current_turn['bot'])
        else:
            nxt_cndn = self.current_turn['next_condition']
            nxt_cndn_match_mthd_dict = get_nxt_cndn_match_mthd_dict(nxt_cndn)
            # for match_method_keyword in ['EXACT', '']
            match_found = False

            for matcher in 'EXACT LOWER CASE_SENSITIVE_KEYWORD KEYWORD NORMALIZE'.split():
                match_found = self.find_next_state(statement, matcher, nxt_cndn_match_mthd_dict)
                if match_found:
                    break

            if not match_found:
                self.state = nxt_cndn_match_mthd_dict[None][0][1]
            self.current_turn = self.turns.get(self.state or '', None) or None
            if self.current_turn:
                response = self.current_turn.get('bot') or ''
                if not isinstance(response, str):
                    response = '\n'.join(response)
            else:
                response = (
                    'Session is already over! Type "quit" to exit or press "Enter" for a '
                    'new session'
                )
        return [(1.0, response)]

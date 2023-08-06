""" Rule-based chatbot (FSM) for administering adaptive quizzes """
import logging
from pathlib import Path

from qary.config import DATA_DIR
from qary.skills.base import ContextBaseSkill
from qary.chat.dialog import TurnsPreparation, compose_statement, load_dialog_turns
from qary.chat.intents import Intents
from qary.chat.understanders import check_match
from qary.chat.dialog import get_nxt_cndn_match_mthd_dict

from qary.config import DIALOG_TREE_END_STATE_NAMES
from qary.config import DIALOG_TREE_END_BOT_STATEMENTS

from qary.config import WELCOME_STATE_NAME
from qary.config import DEFAULT_BOT_USERNAME
from qary.config import EXIT_STATE_TURN_DICT
from qary.config import EXIT_BOT_STATEMENTS

log = logging.getLogger(__name__)


class Skill(ContextBaseSkill):
    r"""Skill for Quiz"""

    def __init__(self,
                 datafile=Path(DATA_DIR) / 'life_coach' / 'burns-cognitive-distortion-emotion-journal-test.v2.dialog.yml',
                 turns_list=None, use_nlp=True):
        """ If datafile is not given, the turns list of dicts can directly be passed to seed the data
        """
        super().__init__()
        self.fuzzy_intents = Intents()
        self.datafile = datafile
        self.turns = {}
        self.use_nlp = use_nlp
        # if turns is passed, then you should not set the datafile
        if turns_list:
            self.turns_input = turns_list
        else:
            self.turns_input = load_dialog_turns(datafile)
        if self.turns_input:
            # Do more complex operations using the helper '_TurnsPreparation' class
            turns_preparation = TurnsPreparation(turns_list=self.turns_input, use_nlp=self.use_nlp)
            self.turns = turns_preparation.prepare_turns()
        else:  # some sort of error
            log.error('An empty turns_list and/or datafile was passed to quiz.Skill.__init__()')
        self.state = ''  # State names must be strings
        self.current_turn = {}  # None or empty dict used to indicate start of quiz that bot says something first?
        return

    def reply(self, statement, context=None):
        r"""Except for the welcome state, all other states are mere recordings of the quiz responses
        """
        log.warning(f'self.current_turn={context}')
        responses = super().reply(statement, context=context)
        statement = str(statement)
        if statement in DIALOG_TREE_END_BOT_STATEMENTS:
            statement = None

        # First check to see if we are in the time before the welcome state
        if self.state in DIALOG_TREE_END_STATE_NAMES:
            # First figure out the welcome state name using a magical special WELCOME_STATE_NAME string
            # as the key. This will allow you to access the actual welcome turn
            self.state = self.turns[WELCOME_STATE_NAME]
            #self.current_turn = self.turns[self.state]
            self.current_turn = self.state
            response_text = compose_statement(self.current_turn['bot'])
            return responses + [(1.0, response_text)]

        nxt_cndn = self.current_turn['next_condition']
        log.warning(f'self.current_turn={self.current_turn}')
        nxt_cndn_match_mthd_dict = get_nxt_cndn_match_mthd_dict(nxt_cndn)
        log.warning(f'nxt_cndn_match_mthd_dict={nxt_cndn_match_mthd_dict}')
        # for match_method_keyword in ['EXACT', '']
        match_found_next_state = (False, '__default__')
        log.warning(f'nxt_cndn_match_mthd_dict["EXACT"]={nxt_cndn_match_mthd_dict["EXACT"]}')
        for next_state_option in nxt_cndn_match_mthd_dict['EXACT']:
            match_found_next_state = check_match(statement, next_state_option, 'EXACT')
            log.warning(f'next_state_option={next_state_option}')
            if match_found_next_state[0]:
                break
        if not match_found_next_state[0]:
            for next_state_option in nxt_cndn_match_mthd_dict['LOWER']:
                match_found_next_state = check_match(statement, next_state_option, 'LOWER')
                if match_found_next_state[0]:
                    break
        if not match_found_next_state[0]:
            for next_state_option in nxt_cndn_match_mthd_dict['CASE_SENSITIVE_KEYWORD']:
                match_found_next_state = check_match(
                    statement, next_state_option, 'CASE_SENSITIVE_KEYWORD'
                )
                if match_found_next_state[0]:
                    break
        if not match_found_next_state[0]:
            for next_state_option in nxt_cndn_match_mthd_dict['KEYWORD']:
                match_found_next_state = check_match(statement, next_state_option, 'KEYWORD')
                if match_found_next_state[0]:
                    break
        if not match_found_next_state[0]:
            for next_state_option in nxt_cndn_match_mthd_dict['NORMALIZE']:
                match_found_next_state = check_match(statement, next_state_option, 'NORMALIZE')
                if match_found_next_state[0]:
                    break
        if not match_found_next_state[0]:
            for next_state_option in nxt_cndn_match_mthd_dict['FUZZY_KEYWORD']:
                log.warning(f'next_state_option={next_state_option}')
                match_found_next_state = check_match(statement, next_state_option, 'FUZZY_KEYWORD')
                log.warning(f'match_found_next_state={match_found_next_state}')
                if match_found_next_state[0]:
                    break
        match_found, self.state = match_found_next_state
        if not match_found:
            self.state = nxt_cndn_match_mthd_dict[None][0][1]
        self.current_turn = self.turns.get(self.state, EXIT_STATE_TURN_DICT)
        response_text = compose_statement(self.current_turn.get(DEFAULT_BOT_USERNAME, EXIT_BOT_STATEMENTS))

        return responses + [(1.0, response_text)]

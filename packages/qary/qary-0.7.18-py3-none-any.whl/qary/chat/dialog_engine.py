# dialog_engine.py


from .understanders import check_match
from ..config import DIALOG_TREE_END_STATE_NAMES
from ..config import DIALOG_TREE_END_BOT_STATEMENTS
from ..config import WELCOME_STATE_NAME
from ..config import DEFAULT_BOT_USERNAME
from ..config import EXIT_STATE_TURN_DICT
from ..config import EXIT_BOT_STATEMENTS

from .dialog import compose_statement


class DialogStateMachine():

    end_state_names = (None, False, 0, '', ''.encode(), '0', 'none', 'None')
    end_user_statements = ('quit', 'exit')
    end_bot_statements = (None, 'none', )
    welcome_state_name = WELCOME_STATE_NAME

    def compute_next_state(self, statement, context=None):
        responses = super().reply(statement, context=context)
        statement = str(statement)
        if statement in self.end_bot_statements:  # FIXME: this logic seems weird, match user statement not bot statement
            statement = None

        # First check to see if we are in the time before the welcome state
        if self.state in self.end_state_names:
            # First figure out the welcome state name using a magical special WELCOME_STATE_NAME string
            # as the key. This will allow you to access the actual welcome turn
            self.state = self.turns[WELCOME_STATE_NAME]
            # print(self.state)
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

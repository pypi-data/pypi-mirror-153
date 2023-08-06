""" Yes/no game to solve brain teaser puzzles such as the cat lady problem

About 50% accuracy using SpaCy md model for intent recognition on yes/no questions from user.

"""
import logging
import os
import numpy as np

from qary.chat.dialog_parse import DialogTurns
from qary.config import DATA_DIR
from qary.config import FINISH_STATE_NAME
from qary.chat.v2 import WELCOME_STATE_NAME

from qary.etl.faqs import normalize_docvectors
from qary.spacy_language_model import nlp


MULTIPLE_CATS_PRBLM = os.path.join(DATA_DIR, 'yes_no/multiple_cats_problem.txt')
INTERN_QUIZ = os.path.join(DATA_DIR, 'yes_no/intern_quiz.txt')
MIN_SIMILARITY = 0.7

log = logging.getLogger(__name__)


def vector_dict(statements, keys=None):
    """Borrowed from glossaries.py"""
    statements = [str(t) if t else '' for t in statements]
    keys = statements if keys is None else list(keys)
    vector_list = []
    log.info(f'Computing doc vectors for {len(statements)} statements...')
    for k, term in zip(keys, statements):
        vec = nlp(
            term
        ).vector  # s can sometimes (rarely) be a float because of pd.read_csv (df_titles)
        vec /= np.linalg.norm(vec) or 1.0
        mask_zeros = np.abs(vec) > 0
        if mask_zeros.sum() < len(mask_zeros):
            log.debug(f'BAD VEC: {term} [0]*{mask_zeros.sum()}')
        vector_list.append((k, vec))

    # TODO: make sure this isn't needed
    # mask = np.array([bool(stmt) and (len(str(stmt).strip()) > 0) for stmt, _ in vector_list])
    docvectors = [vector for statement, vector in vector_list]
    vectors_norm = normalize_docvectors(docvectors)
    vector_list_new = []
    for (statement, _), vector in zip(vector_list, vectors_norm):
        vector_list_new.append((statement, vector))
    # vector_list_new = np.array([qv for qv, m in zip(question_vectors, mask) if m])
    return dict(vector_list_new)


class Skill:
    r"""Skill for factqest type scenarios"""

    def __init__(self, datafile=None):
        """ """
        global nlp
        self.nlp = nlp
        datafile = datafile or MULTIPLE_CATS_PRBLM
        dialog_turns = DialogTurns(datafile)
        dialog_turns.parse_dialog_lines()
        self.turns = dialog_turns.turns
        player_replies = ['\n'.join(turn['player']) for turn in self.turns]
        self.player_replies_vector = np.array(list(vector_dict(player_replies).values()))
        self.state = ''
        return

    def reply(self, statement, context=None):
        r"""Suggest responses to a user statement string according to a quest script

        >>> s = Skill()
        >>> s.reply(None) # doctest: +ELLIPSIS
        [(1.0, 'A woman went on ...Ready?')]
        >>> s.reply('Yes') # doctest: +ELLIPSIS
        [(1.0, 'Great! Ask me your first question...puzzle.')]
        >>> s.reply('Did the cat go missing and have babies and came back?') # doctest:+ELLIPSIS
        [(1.0, 'It appears that ...questions?')]
        >>> s.reply('Did he think that the lady would recognize her cat among these 8 cats?') # doctest: +ELLIPSIS
        [(1.0, 'Yes.\nKudos! ...crack another one.')]
        """
        if not self.state and self.state is not None:
            response = '\n'.join(self.turns[0]['bot'])
            self.state = WELCOME_STATE_NAME
        elif self.state == WELCOME_STATE_NAME:
            self.state = 'play'
            if statement.lower().strip()[0] == 'y':
                response = '\n'.join(self.turns[1]['bot'])
            elif statement.lower().startswith('no'):
                self.state = None
                response = 'Exiting, bye!'
            else:
                response = 'Please answer yes or no'
        else:
            question_vector = self.nlp(statement).vector
            question_vector /= np.linalg.norm(question_vector)
            question_similarities = self.player_replies_vector.dot(question_vector.reshape(-1, 1))
            mask = np.array(question_similarities).flatten() >= MIN_SIMILARITY
            if sum(mask) >= 1:
                idx = question_similarities.argmax()
                turn = self.turns[idx]
                if turn['state'].lower().strip().strip('_') == FINISH_STATE_NAME.lower().strip().strip('_'):
                    self.state = None
                response = '\n'.join(turn['bot'])
            else:
                response = 'Irrelevant'
        return [(1.0, response)]

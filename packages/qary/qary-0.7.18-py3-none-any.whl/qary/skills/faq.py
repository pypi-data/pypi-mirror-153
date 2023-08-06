""" Pattern and template based chatbot dialog engines """
import logging

# import pandas as pd

from qary.etl import faqs
from qary.config import DOMAINS, FAQ_MIN_SIMILARITY  # , FAQ_MAX_NUM_REPLIES
from qary.skills.base import BotReply
# from qary import spacy_language_model
from qary.etl import knowledge_extraction as extract  # noqa
import numpy as np
import pandas as pd
from qary.chat.dialog_managers import get_nlp

log = logging.getLogger(__name__)


def capitalizations(s):
    return (s, s.lower(), s.upper(), s.title())


class Skill:
    r""" Skill that can reply with answers to frequently asked questions using data/faq/*.yml

    >>> bot = Skill()
    >>> bot.reply('What are the basic variable data types in python?')[0][1]
    '`float`, `int`, `str`, and `bool`'
    >>> bot.reply(None)
    [(0.1, 'I don\'t...
    """

    def __init__(self, domains=DOMAINS, nlp='spacy'):
        """ Load glossary from yaml file indicated by list of domain names """

        self.nlp = get_nlp(nlp)
        self.faq = faqs.load(domains=domains)
        log.debug(f"len(self.faq): {len(self.faq)}")

    def reply(self, statement, context=None):
        """ Suggest responses to a user statement string with [(score, reply_string)..]"""
        statement = statement or ''
        responses = []
        questions = []
        question_vector = self.nlp(statement).vector
        log.debug(f"question_vector is {question_vector}")
        question_vector /= np.linalg.norm(question_vector)
        log.debug(f"faq['question_vectors'].shape is {self.faq['question_vectors'].shape}")
        question_similarities = self.faq['question_vectors'].dot(question_vector.reshape(-1, 1))
        idx = question_similarities.argmax()
        mask = np.array(question_similarities).flatten() >= FAQ_MIN_SIMILARITY
        # TODO: Construct a skill with a new threshold while using the default threshold in the constructor.

        # TODO: progressively expand threshold in case there are many more than FAQ_MAX_NUM_REPLIES similar Q's

        if sum(mask) >= 1:
            questions.extend(dict(confidence=confidence, question=question, answer=answer, skill=self.__module__)
                             for confidence, question, answer in
                             zip(question_similarities[mask],
                                 (str(a) for a in self.faq['questions'][mask]),
                                 (str(a) for a in self.faq['answers'][mask])
                                 ))
            df = pd.DataFrame(questions)

            df = df.sort_values(by=['confidence'], ascending=False, ignore_index=True)

            # Mostly for debugging
            # faq_text = df.question[0]
            # faq_answer = df.answer[0]
            # full_response = f'I found this similar FAQ: "{faq_text}".\n  The answer to that is as follows: {faq_answer}'

            responses.append(BotReply(df.confidence[0], df.answer[0], skill=self.__module__))
        else:
            responses = [(
                0.10,
                f"I don't know. Here's a FAQ similar to yours that you might try: \"{self.faq['questions'][idx]}\". ")]
        return responses

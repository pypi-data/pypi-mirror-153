""" Transformer based chatbot dialog engine for answering questions """

import logging

from qary.skills import qa

log = logging.getLogger(__name__)

STOP_WIKI_PROBABILITY = .4


class Skill(qa.Skill):
    """ Skill that provides answers to questions given context data containing the answer """

    def __init__(self, context=None, **kwargs):
        super().__init__(context=context, **kwargs)

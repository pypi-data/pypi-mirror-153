""" Pattern and template based chatbot dialog engines """
import logging

from qary.chat.v3 import Engine
from qary.skills.base import normalize_replies, ContextBaseSkill


log = logging.getLogger(__name__)

dialog_enging = Engine()


class Skill(ContextBaseSkill):
    r""" Skill that can reply with answers to frequently asked questions using data/faq/*.yml

    >>> bot = Skill()
    >>> bot.reply(None)
    [(1.0, 'I\'m part of the Let\'s Talk NYC team and I\'m here to help ... a few questions? Select "Yes" when ready\n')]
    """

    def __init__(self, *args, **kwargs):
        """ Load the v3.dialog.yaml file to initialize the dialog state machine (dialog engine) """
        self.engine = Engine(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def reply(self, statement, context=None):
        """ Suggest responses to a user statement string with [(score, reply_string)..]"""
        if context is None:
            context = {}
        statement = statement or ''
        # response = self.engine.run(statement, **kwargs)
        response = self.engine.run(**context)
        responses = [(1.0,
                      response.get('bot_text',
                                   'ERROR: not bot_text returned from v3.Engine()')
                      )
                     ]
        normalize_replies(responses)
        return responses

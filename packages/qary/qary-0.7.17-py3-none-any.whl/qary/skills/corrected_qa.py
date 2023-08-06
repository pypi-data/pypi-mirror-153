""" Transformer based chatbot dialog engine for answering questions """
from qary.skills.qa import Skill as QASkill
from qary.etl.spell import make_spelling_corrections

import transformers
# # Allocate a pipeline for question-answering
# >>>
# >>> question_answerer({
# ...     'question': 'What is the name of the repository ?',
# ...     'context': 'Pipeline have been included in the huggingface/transformers repositor


class Skill(QASkill):
    """ Skill that provides answers to questions given context data containing the answer

    FIXME: QA skill broke with upgrade of transformers package (and torch + SpaCy)
    >> skill = Skill()
    >> skill.reply('How many in a bakurs dozin?')[0][1]
    '13'
    >> skill.reply('When was the telefone inventid?')[0][1]
    '1844.'
    """

    def reply(self, statement, context=None, **kwargs):
        """ Use context document + BERT to answer question in statement

        context is a nested dictionary with two ways to specify the documents for a BERT context:
        {docs: ['doc text 1', '...', ...]}
        or, as only syntactic sugar (internally this is converted to the format above)
        {doc: {text: 'document text ...'}}
        """
        statement = make_spelling_corrections(statement)
        return super().reply(statement, context=context, **kwargs)

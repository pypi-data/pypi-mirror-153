""" Transformer based chatbot dialog engine for answering questions """
import logging

import numpy as np
import transformers

from qary.config import CLI_ARGS
from qary.skills.base import BotReply
from qary.skills.base import ContextBaseSkill


log = logging.getLogger(__name__)

STOP_WIKI_PROBABILITY = .4


class Skill(ContextBaseSkill):
    """ Skill that provides answers to questions given context data containing the answer """

    def __init__(self, context=None, cli_args=CLI_ARGS, model=None, *args, **kwargs):
        """ Initialize a Question Answering skill using model supplied (default model=BERT)

        >>> qa = Skill()
        >>> callable(qa.reply)
        True
        >>> qa.model({
        ...     'question': "Who was Adam's son ?",
        ...     'context': "Cain was Abel's brother. They were both Adam's sons."})
        {'score': 0.9..., 'start': 0, 'end': 4, 'answer': 'Cain'}
        """
        context = {'doc': {'text': ''}}
        log.debug(f'Initial qa.Skill.context: {getattr(self, "context", None)}')
        self.model = transformers.pipeline('question-answering') if model is None else model
        # self.wikiscraper = wikititles.WikiScraper()
        super().__init__(context=context, cli_args=cli_args, *args, **kwargs)

    def reply(self, statement, context=None, **kwargs):
        """ Use context document + BERT to answer question in statement

        context is a nested dictionary with two ways to specify the documents for a BERT context:
        {docs: ['doc text 1', '...', ...]}
        or, as only syntactic sugar (internally this is converted to the format above)
        {doc: {text: 'document text ...'}}
        """
        statement = statement or ''
        log.info(f"QABot.reply(statement={statement}, context={context})")
        if isinstance(context, str):
            context = dict(docs=[context], doc=dict(text=context))
        elif isinstance(context, (list, tuple, np.ndarray)):
            context = dict(docs=context, doc=dict(text='\n'.join(context)))
        # this calls self.update_context(context=context) internally:
        elif isinstance(context, dict):
            if not context.get('docs') and context.get('doc'):
                context['docs'] = [context.get('doc').get('text')]

        if (not context or not any(context.get('docs', ['']))):
            gendocs = self.wikiscraper.find_article_texts(
                query=statement,
                max_articles=1, max_depth=1,
                ngrams=3,
                ignore='who what when where why'.split()) or []
            context = dict(docs=gendocs)
        responses = super().reply(
            statement=statement, context=context, **kwargs) or []
        log.info(f"qa_bots.Skill.super() responses (before BERT): {responses}")
        docs = self.context.get('docs') or [self.context['doc']['text']]
        for i, text in enumerate(docs):
            log.info(
                f"text[{i}] from context['doc']['text'] or wikipedia_api: "
                f"{repr(text)[:40]}...{repr(text)[-40:]} ({len(text)} chars)")
            super().update_context(context=dict(doc=dict(text=text)))
            if len(text.strip()) < 2:
                log.info(f'Context document text was too short: "{text}"')
                continue
            qa_inputs = {'context': text, 'question': statement}
            model_prediction_dict = self.model(qa_inputs)
            probability, response_text = model_prediction_dict['score'], model_prediction_dict['answer']

            if len(response_text) > 0:
                responses.append(
                    BotReply(
                        confidence=probability,
                        text=response_text,
                        skill=self.__module__))
                if probability > STOP_WIKI_PROBABILITY:
                    log.info(f"Short circuiting wiki crawl because p > thresh: {probability} > {STOP_WIKI_PROBABILITY}")
                    break
        return responses

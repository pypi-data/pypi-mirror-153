""" Pattern and template based chatbot dialog engines """
import logging

# import pandas as pd

from qary.config import GLOSSARY_DOMAINS
from qary.etl import glossaries
from qary import spacy_language_model
from qary.etl import knowledge_extraction as extract
# from qary.chat.dialog import generate_domain_filepaths

from qary.skills.base import ContextBaseSkill
from qary.skills.base import BotReply

log = logging.getLogger(__name__)
nlp = spacy_language_model.load('en_core_web_md')


def capitalizations(s):
    return (s, s.lower(), s.upper(), s.title())


class Skill(ContextBaseSkill):
    """ Skill that can reply with definitions from glossary yml files in data/faq/glossary-*.yml

    >>> bot = Skill()
    >>> bot.reply('allele')
    [BotReply(confidence=0.05, text="I don't understand. That doesn't sound like...
    >>> bot.reply('What is an Allele?')
    [BotReply(confidence=1.0, text='A variant form of a given gene...
    >>> bot.reply('What is a nucleotide?')
    [BotReply(confidence=0.94, text='The basic building blocks of DNA and RNA...
    """

    def __init__(self, domains=['']):
        """ Load glossary from yaml file indicated by list of domain names """
        global nlp
        super().__init__()
        self.nlp = nlp
        self.glossary = glossaries.load(domains=GLOSSARY_DOMAINS)['cleaned']
        self.vector = dict()
        self.vector['term'] = glossaries.term_vector_dict(self.glossary.keys())
        self.vector['definition'] = glossaries.term_vector_dict(self.glossary.values(), self.glossary.keys())

        self.synonyms = {term: term for term in self.glossary}
        # create reverse index of synonyms to canonical terms
        # for term, d in self.glossary.items():
        #     self.synonyms.update(dict(zip(capitalizations(term), [term] * 4)))
        #     acro = d['acronym']
        #     if acro:
        #         self.synonyms.update(dict(zip(capitalizations(acro), [term] * 4)))

    def reply(self, statement, context=None):
        """ Suggest responses to a user statement string with [(score, reply_string)..]"""
        if statement is None:
            return [BotReply(
                0, "I have the `glossary` skill loaded. So I can answer questions like \"What is an allele?\""
            )]
        responses = []
        extracted_term = extract.whatis(statement) or extract.whatmeans(statement) or ''
        if extracted_term:
            for i, term in enumerate(capitalizations(extracted_term)):
                normalized_term = self.synonyms.get(term, term)
                if normalized_term in self.glossary:
                    responses.append(BotReply(
                        confidence=1 - .02 * i,
                        text=self.glossary[normalized_term]['definition'],
                        skill=self.__module__))
        else:
            responses = [BotReply(
                confidence=0.05,
                text="I don't understand. That doesn't sound like a question I can answer using my glossary.",
                skill=self.__module__)]
        if not len(responses):
            responses.append(
                BotReply(
                    confidence=0.25,
                    text=f"My glossaries and dictionaries don't seem to contain that term ('{extracted_term}').",
                    skill=self.__module__))
        return responses

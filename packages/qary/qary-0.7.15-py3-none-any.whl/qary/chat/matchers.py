""" Intent matching functions that return true or false for the intent matching the statement

(dependency injections for intent recognitizer check_match)
"""
from .classifiers import classify_intent


def exact(statement, intent):
    return statement == intent


def fuzzy(statement, intent):
    """ Use kalika's emotional word/intent recognizer """
    return classify_intent(statement) == intent


def keyword(statement, intent):
    """ Use kalika's emotional word/intent recognizer """
    # TODO: tokenize statement with memoized tokenizer
    return intent in statement


def default(statement, intent):
    return exact(statement, intent)



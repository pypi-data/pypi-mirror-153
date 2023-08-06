""" Pattern and template based chatbot dialog engines """
import logging
import os

print ('PATH = ' + os.environ['PATH'])

import pronouncing
import random
import re 

class Skill:
    r"""Returning a rhyming sentence"""
    def __init__(self, statement, context):
        self.statement = statement
        self.context = None

    def reply(statement):
        r"""Returns a sentence in which the final word rymes with the final word of the input string

        Examples:
            #TODO
        """
     
        # Removing any punctuation from the string using regex, except apostrophes
        statement = re.sub(r"[^\w\d'\s]+", '', statement)
        word_list = statement.split() # list of words
        rhyming_words = pronouncing.rhymes(word_list[-1]) # list of words that rhyme with the last word in 
                                                          # input sentence
        doc = nlp(statement) # tokenizing the statement for pos_ classification

        rhyme_dict = {}
        pos = doc[-1].pos_ # The part of speech of the original last word
        for rhyme in rhyming_words:
            sentence = statement.rsplit(' ', 1)[0] + ' ' + rhyme # putting rhymes in context for accurate 
                                                                 # pos_ classification
            tok = nlp(sentence) # tokenizing the modified statement for pos_ classification
            if tok[-1].pos_ == pos or tok[-1].pos_ == 'PROPN':
                rhyme_dict[rhyme] = tok[-1].pos_
        if len(rhyme_dict) == 0:
            return "Nothing rhymes with " + word_list[-1]
        choices = list(rhyme_dict.keys())
        #print(f"{pos}-Choices -----> ", choices)
        response = ' '.join(word_list[:-1]) + ' ' + str(random.choice(choices))
        return [(1.0, response)]

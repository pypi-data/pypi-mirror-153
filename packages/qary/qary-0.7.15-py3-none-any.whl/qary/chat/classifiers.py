from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np
import yaml

from pathlib import Path
from qary.config import DATA_DIR

from qary.spacy_language_model import load


DEFAULT_EMOTIONS_FILEPATH = Path(DATA_DIR) / 'life_coach' / 'life-language-data.yml'

LANGUAGE_MODELS = dict(
    spacy='en_core_web_md',
    spacy_large='en_core_web_lg'
)


class Intents:
    def __init__(self, filepath=DEFAULT_EMOTIONS_FILEPATH, language_model="spacy"):
        """ Load a pretrained model or training dataset from filepath to fit an intent classifier"""
        with open(filepath) as fstream:
            self.synonyms = yaml.full_load(fstream)
        language_model = LANGUAGE_MODELS.get(language_model.strip().lower())
        self.nlp = load(language_model)
        self.model = self.fit()

    def fit(self, X=None, y=None, random_state=None):
        if not X or not y:
            df = []
            X = []
            for emotion_name, synonyms in self.synonyms.items():
                for w in synonyms:
                    # df.append([emotion_name, w])
                    # print(emotion_name, w)
                    df.append([emotion_name] + list(self.vectorize(w)))
            df = pd.DataFrame(df)
            df = df.set_index(0)
            X = df.values
            y = df.index.values
        model = LogisticRegression(random_state=random_state)
        model.fit(X, y)
        self.model = model
        return model

    def predict(self, phrase):
        return self.model.predict(np.array([self.vectorize(phrase)]))[0]

    def vectorize(self, s):
        return np.array(self.nlp(s).vector)


def classify_intent(statement, intents=None):
    """ Use kalika's emotional word/intent recognizer """
    if not intents:
        classify_intent.intents = classify_intent.intents or Intents()
    else:
        classify_intent.intents = intents
    return classify_intent.intents.predict(statement)


classify_intent.intents = None

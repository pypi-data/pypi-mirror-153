# TODO: add doc strings?
import logging
import importlib
import sys

from qary import constants
from qary.skills.base import BotReply
from qary import spacy_language_model
import qary.scores  # noqa

sys.path.append(constants.BASE_DIR)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def sentiment_analyzer():
    return 0


class QualityScore:
    def __init__(self, confidence_weight=1.0, **kwargs):
        """ replace self-score with mean of weighted external scores and self-score

        >>> QualityScore(semantic=0.85)
        <quality_score.QualityScore...>
        >>> QualityScore(semantic=0.85).weights
        [0.5405..., 0.4594...]
        """
        self.metric_names, self.weights = tuple(zip(*kwargs.items())) if kwargs else ((), ())
        total_weight = sum(self.weights) + confidence_weight
        self.metric_names = ['self_confidence'] + list(self.metric_names)
        self.weights = [confidence_weight / total_weight] + [w / total_weight for w in self.weights]
        self.modules = {name: importlib.import_module(f'qary.scores.{name}_score') for name in self.metric_names[1:]}
        self.nlp = spacy_language_model.nlp
        self.kwargs = {'nlp': self.nlp, 'sentiment_analyzer': sentiment_analyzer}

    def update_replies(self, replies, user_statement=None):
        """ replace self-score with mean of weighted external scores and self-score

        >>> qs = QualityScore(semantic=1)
        >>> qs.update_replies([BotReply(.5, 'good bye')])
        [BotReply(confidence=0.25, text='good bye', skill=None, context=None)]
        >>> qs.update_replies([BotReply(.5, 'good bye'), BotReply(.5, 'awesome')])
        [BotReply(confidence=0.25, text='good bye', skill=None, context=None),
         BotReply(confidence=0.2..., text='awesome', skill=None, context=None)]
        """
        log.debug(replies)

        updated_replies = []
        for reply in replies:
            new_score = self.mean_weighted_score(reply)
            reply = BotReply(*reply)
            i_confidence = reply._fields.index('confidence')
            reply = list(reply)
            reply[i_confidence] = new_score
            updated_replies.append(BotReply(*reply))
        return updated_replies

    def mean_weighted_score(self, reply, user_statement=None):
        """ mean of weighted external scores and reply.confidence

        >>> qs = QualityScore(semantic=1)
        >>> qs.mean_weighted_score((.5, 'hi'), user_statement='hi')
        0.75
        >>> qs.mean_weighted_score((.5, 'goodbye'))
        0.25
        >>> qs.mean_weighted_score((.5, 'good bye'))
        0.25
        >>> qs = QualityScore()
        >>> qs.mean_weighted_score((.75, 'awesome'))
        0.75
        >>> qs = QualityScore(semantic=0)
        >>> qs.mean_weighted_score((.9, 'hi'))
        0.9
        """
        user_statement = user_statement or ''
        scores = [reply[0]]
        for name, weight in zip(self.metric_names[1:], self.weights[1:]):
            fun = getattr(self.modules[name], 'score')
            score = fun(reply[1], stmt=user_statement, **self.kwargs)
            scores.append(score)
        scores = [w * s for w, s in zip(self.weights, scores)]
        return sum(scores)


def score(reply, stmnt=None):
    """ Combine multiple scores into a single quality score """
    raise NotImplementedError()

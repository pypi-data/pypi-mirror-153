import numpy as np
import pandas as pd
# from nlpia.loaders import get_data

# lexicon = pd.Series(SentimentIntensityAnalyzer().lexicon)

# wv = get_data('w2v')


# bad_words = lexicon.index.values[:30:3]


# def closest_to_any(word, targets):
#     """ Find the most similar word among a list of target words/vectors """
#     vectors = pd.DataFrame([wv[word]], index=[word]) if isinstance(word, str) else word
#     targets = pd.DataFrame([targets], index=targets) if not hasattr(targets, 'shape') else targets
#     targets = pd.DataFrame([wv[t] for t in targets], index=targets) if isinstance(targets[0], str) else targets
#     print(targets.shape)
#     print(vectors.shape)
#     return pd.DataFrame(
#         np.matmul(vectors.values, targets.T.values),
#         index=vectors.index, columns=targets.index)


# def is_bad_word_v1(word):
#     """ True/Flase is a negative sentiment word

#     >>> is_bad_word_v1("bad")
#     True
#     >>> is_bad_word_v1("I")
#     True
#     >>> is_bad_word_v1("'m")
#     True
#     >>> is_bad_word_v1("feeling")
#     False
#     >>> is_bad_word_v1(".")
#     False
#     """
#     try:
#         max_badness = max([wv.similarity(word, bw) for bw in bad_words])
#         print(f'max_badness: {max_badness}')
#         if max_badness > .2:
#             return True
#     except:
#         pass
#     return False


# def is_bad_word_v2(word):
#     """ True/Flase is a negative sentiment word

#     >>> is_bad_word_v2("bad")
#     True
#     >>> is_bad_word_v2("I")
#     False
#     >>> is_bad_word_v2("'m")
#     False
#     >>> is_bad_word_v2("feeling")
#     False
#     >>> is_bad_word_v2(".")
#     False
#     """
#     try:
#         if str(word).lower().strip() in bad_words:
#             # print(f'found bad word: {word}')
#             return True
#     except:
#         pass
#     return False


# def add(base_word, modifier, weight=1.):
#     base_word = wv[base_word]
#     modifier = wv[modifier]
#     vector = (1 / 2.) * (base_word + weight * modifier)
#     vector *= (1 / np.linalg.norm(vector))
#     return wv.similar_by_vector(vector)[1][0]

# -*- coding: utf-8 -*-


from .networks import SentimentAnalysis

SA = SentimentAnalysis()


def predict(text):
    """
    1: positif
    0.5: neutral
    0: negatif
    """
    score1, score0 = SA.normalization_score(text)
    if score1 == score0:
        result = 0.5
    elif score1 > score0:
        result = 1
    elif score1 < score0:
        result = 0
    return result




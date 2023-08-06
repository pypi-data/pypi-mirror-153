# -*- coding: utf-8 -*-


from settings import BASE_DIR, relative
from .utils import ToolGeneral

pwd = relative(BASE_DIR, 'ml/nlp/sentiments/by_dict/dict')
tool = ToolGeneral()


class Hyperparams:
    '''Hyper parameters'''
    # Load sentiment dictionary
    deny_word = tool.load_dict(relative(pwd, 'dict', 'not.txt'))
    posdict = tool.load_dict(relative(pwd, 'dict', 'positive.txt'))
    negdict = tool.load_dict(relative(pwd, 'dict', 'negative.txt'))
    pos_neg_dict = posdict | negdict
    # Load adverb dictionary
    mostdict = tool.load_dict(relative(pwd, 'dict', 'most.txt'))
    verydict = tool.load_dict(relative(pwd, 'dict', 'very.txt'))
    moredict = tool.load_dict(relative(pwd, 'dict', 'more.txt'))
    ishdict = tool.load_dict(relative(pwd, 'dict', 'ish.txt'))
    insufficientlydict = tool.load_dict(relative(pwd, 'dict', 'insufficiently.txt'))
    overdict = tool.load_dict(relative(pwd, 'dict', 'over.txt'))
    inversedict = tool.load_dict(relative(pwd, 'dict', 'inverse.txt'))

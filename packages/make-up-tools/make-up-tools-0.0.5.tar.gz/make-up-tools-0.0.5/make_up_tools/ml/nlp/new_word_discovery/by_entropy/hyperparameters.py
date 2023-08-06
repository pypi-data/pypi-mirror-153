# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:31:35 2020

@author: cm
"""

import math

from settings import BASE_DIR, relative

pwd = relative(BASE_DIR, 'ml/nlp/sentiments/by_dict/dict')


class Hyperparamters:
    # Parameters
    file_vocabulary = relative(pwd, 'dict/vocabulary_word.txt')
    top_k = 1000
    chunk_size = 1000000
    min_n = 1  # 1#2
    max_n = 4
    min_freq = 5

    #
    e = math.exp(1)

    # CPU number used
    CPU_COUNT = 1
    #
    vocab_file = relative(pwd, 'dict/vocabulary.txt')

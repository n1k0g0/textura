# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import sent_tokenize
from ..preprocessing import basic
import statistics
nltk.download('punkt')


def avg_sentence_length(text):
    """
    For a given document, return the average sentence length.
    """
    sentence_list = sent_tokenize(text.strip())
    word_list = [basic.remove_punctuation_and_tokenize(words) for words in sentence_list]
    length_list = [len(word) for word in word_list]
    sentence_length_list = [len(basic.remove_punctuation_and_tokenize(sentence)) for sentence in sentence_list]
    return {
        "Средняя длина предложения": float(format(statistics.mean(sentence_length_list), '.2f')),
        "Число предложений": len(sentence_list),
        "Максимальная длина": max(length_list),
        "Минимальная длина": min(length_list),
        "Среднеквадратическое отклонение": float(format(statistics.stdev(length_list), '.2f')),
    }

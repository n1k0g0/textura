from ..preprocessing import complexity
import numpy as np
import pyphen
import nltk


def count_readability(text):
    words = nltk.word_tokenize(text)
    List_of_Words_without_Punctuation = [word for word in words if word.isalnum()]
    List_of_Sentences = complexity.split_into_sentences(text)
    ASL = np.mean(np.array([len(va.split()) for va in List_of_Sentences]))
    dic = pyphen.Pyphen(lang='ru_RU')
    ASW = np.mean(
        np.array([len(dic.inserted(va).split('-')) for va in ' '.join(List_of_Words_without_Punctuation).split()]))

    Reading_Ease_Score = 206.835 - (1.015 * ASL) - (84.6 * ASW)
    Hard_Words_Quantity = len(np.array(
        [va for va in ' '.join(List_of_Words_without_Punctuation).split() if len(dic.inserted(va).split('-')) > 2]))

    Words_Quantity = len(np.array(
        [va for va in ' '.join(List_of_Words_without_Punctuation).split() if len(dic.inserted(va).split('-'))]))

    Gunning_fog = 0.4 * (ASL + ((Hard_Words_Quantity / Words_Quantity) * 100))

    return f'Reading Ease Score: {Reading_Ease_Score}; Gunning Fog: {Gunning_fog}'
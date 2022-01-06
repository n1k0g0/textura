from nltk.tokenize import word_tokenize
import string


def remove_punctuation_and_tokenize(sentence):
    """
    For a given sentence, remove the punctuation and return a tokened list of words.
    """
    return word_tokenize(sentence.translate(str.maketrans({a: None for a in string.punctuation})))
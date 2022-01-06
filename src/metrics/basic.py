from nltk.tokenize import sent_tokenize
from ..preprocessing import basic
import statistics


def avg_sentence_length(text):
    """
    For a given document, return the average sentence length.
    """
    sentence_list = sent_tokenize(text.strip())
    word_list = [basic.remove_punctuation_and_tokenize(words) for words in sentence_list]
    length_list = [len(word) for word in word_list]
    return {
        "Средняя длина предложения": float(format(statistics.mean(length_list), '.2f')),
        "Число предложений": len(sentence_list),
        "Максмальная длина": max(length_list),
        "Минимальная длина": min(length_list),
        "Среднеквадратическое отклонение": float(format(statistics.stdev(length_list), '.2f')),
    }
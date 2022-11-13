from nltk.tokenize import sent_tokenize, word_tokenize
from scipy import stats
import statistics
import pathlib
import string


from .models import CorporaEntityData

class PreprocessedText:
    def __init__(self, filename):
        # self.text = open(f'{pathlib.Path(__file__).parent.parent.resolve()}/media/{text.file.name}', encoding='utf-8', mode="r").read()
        self.text = open(f'{pathlib.Path(__file__).parent.parent.resolve()}/media/{filename}', encoding='utf-8', mode="r").read()
        self.sentence_list = sent_tokenize(self.text.strip()) 
        self.split_sentences_list = [remove_punctuation_and_tokenize(words) for words in self.sentence_list]
        self.sentences_length_list = [len(word) for word in self.split_sentences_list]
        self.word_list = remove_punctuation_and_tokenize(self.text)
        self.words_length_list = [len(word) for word in self.word_list]
        self.asl = float(format(statistics.mean(self.sentences_length_list), '.2f'))
        self.asl_stdev = float(format(statistics.stdev(self.sentences_length_list), '.2f'))
        self.asl_rank = float(format(stats.percentileofscore([entry.avg_sentence_length for entry in CorporaEntityData.objects.all() if entry.avg_sentence_length is not None], self.asl), '.2f'))
        self.msl = float(format(max(self.sentences_length_list), '.2f'))

        self.awl = float(format(statistics.mean(self.words_length_list), '.2f'))
        self.awl_stdev = float(format(statistics.stdev(self.words_length_list), '.2f'))
        self.awl_rank = float(format(stats.percentileofscore([entry.avg_word_length for entry in CorporaEntityData.objects.all() if entry.avg_word_length is not None], self.awl), '.2f'))
        self.mwl = float(format(max(self.words_length_list), '.2f'))


def remove_punctuation_and_tokenize(sentence):
    return word_tokenize(sentence.translate(str.maketrans({a: None for a in string.punctuation})))


# def avg_sentence_length(text):
#     sentence_list = sent_tokenize(text.strip())
#     split_sentences_list = [remove_punctuation_and_tokenize(words) for words in sentence_list]
#     sentences_length_list = [len(word) for word in split_sentences_list]
#     return float(format(statistics.mean(sentences_length_list), '.2f'))
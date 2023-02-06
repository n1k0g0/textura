import conllu
import os
from nltk.tokenize import word_tokenize
import string
import statistics
import time


def remove_punctuation_and_tokenize(sentence):
    return word_tokenize(sentence.translate(str.maketrans({a: None for a in string.punctuation})))

def preprocess_text(path):
    start = time.time()

    data_file = open(path, "r", encoding="utf-8")
    sentences_list = []


    for tokenlist in conllu.parse_incr(data_file):
        sentence = (('').join(list(tokenlist.metadata['text'])))
        sentences_list.append(sentence)

    
    word_list = remove_punctuation_and_tokenize((' ').join(sentences_list))
    sentences_length_list = [len(word) for word in sentences_list]
    words_length_list = [len(word) for word in word_list]

    end = time.time()
    print(end - start)

    asl = float(format(statistics.mean(sentences_length_list), '.2f'))
    asl_stdev = float(format(statistics.stdev(sentences_length_list), '.2f'))
    msl = float(format(max(sentences_length_list), '.2f'))
    awl = float(format(statistics.mean(words_length_list), '.2f'))
    awl_stdev = float(format(statistics.stdev(words_length_list), '.2f'))
    mwl = float(format(max(words_length_list), '.2f'))

    end = time.time()
    print(end - start)
    return (asl, asl_stdev, msl, awl, awl_stdev, mwl)

print(preprocess_text(f"{os.getcwd()}/dev/voskres.conllu"))
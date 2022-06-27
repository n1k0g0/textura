# -*- coding: utf-8 -*-
import nltk
from nltk.tokenize import sent_tokenize
from src.preprocessing import basic
from os import walk
import statistics
nltk.download('punkt')

filenames = next(walk('../../mini_corpus'), (None, None, []))[2]

# print(filenames)


def bag_of_words(dir_name):
    file_names = next(walk(dir_name), (None, None, []))[2]
    bow = []
    for filename in file_names:
        print(filename)
        with open(f'{dir_name}/{filename}', 'r') as f:
            text = f.read()
            sentence_list = sent_tokenize(text.strip())
            word_list = [basic.remove_punctuation_and_tokenize(words) for words in sentence_list]
            bow.extend(word_list)
    print(bow)
    bow_unique = list(set(bow))
    with open('../../bow.txt', 'a') as wf:
        for w in bow_unique:
            wf.write(w)
    return bow_unique


def calculate_tf_idf(text):
    """
    For a given document, return the average sentence length.
    """
    unique_words = bag_of_words('../../corpus')

    num_of_words_by_text = dict.fromkeys(filenames, dict.fromkeys(unique_words))


    return {
        num_of_words_by_text
    }


print(bag_of_words('../../mini_corpus'))

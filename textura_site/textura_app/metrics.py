from nltk.tokenize import sent_tokenize, word_tokenize
from scipy import stats
import pymorphy2
import pyphen
import statistics
import pathlib
import string
import numpy as np
import math
from string import punctuation

from random import sample
from .models import CorporaEntityData, CorpusEntityData
from transformers import pipeline
from nltk import download
from nltk.corpus import stopwords


import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


download('punkt')
download("stopwords")


classifier = pipeline("text-classification",model='blanchefort/rubert-base-cased-sentiment-rusentiment', top_k=3)
morph = pymorphy2.MorphAnalyzer()
dic = pyphen.Pyphen(lang='ru_RU')
russian_stopwords = stopwords.words("russian")

TEXT_TYPES = {'brochures': 'Брошюра',
              'orth': 'Христианство',
              'drama': 'Драма',
              'nauka': 'Наука',
              'oldgazette': 'Старые газеты',
              'politika': 'Политика',
              'voennoe': 'Военное',
              'dnevniki': 'Дневники',
              'doc/': 'Док.',
              'ekonomika': 'Экономика',
              'memoir': 'Мемуары',
              'o_': 'О текстах',
              'statji': 'Публикации',
              'Novelly': 'Новеллы',
              'biogr': 'Биографии',
              'litmanifesty': 'Манифесты',
              'anecdota': 'Анекдоты',
              'archive/gaz': 'Газеты',
              'archive/zhurn': 'Журналы',
              'child': 'Детское',
              'forum': 'Форумы',
              'kommersant':'Газеты',
              'izvest':'Газеты',
              'mass_zhurn':'Журналы',
              'ofic':'Официальное',
              'predisl':'Предисловия',
              'xxi_smi':'СМИ XXI в.',
              'zakony':'Законы',
              'zhur_russru':'Журналы',
              '192_dok': 'Документы',
              '1920story':'Рассказы 1920х',
              'civilwar':'Гражданская война',
              'deti_emigr':'Дети эмигрантов',
              'dok194':'Документы 1940-х',
              'dok1900-1910s':'Документы 1900-1910',
              'dok1941-45':'Документы 1941-45',
              'duma_1907-17':'Дума 1907-1917',
              'pisma':'Письма',
              'xx-1-doc':'Документы XXI в.',
              '/doc_':'Документы',
              'lekarstvo1787':'Медицина',
              'letters':'Письма',
              'skazki_ran_zap':'Сказки',
              'voen_flot':'Воен/флот',
              'xviii_doc':'Документы XVIII в.',
              'dn_kuptsov':'Дневники купцов',
              'from_poetry':'Поэзия',
              'kazaki':'Казаки',
              'dok181':'Документы 1810-х'
              }



class PreprocessedText:
    text = None
    sentence_list = None
    split_sentences_list = None
    sentences_length_list = None
    word_list = None
    list_of_lemmas = None

    words_length_list = None
    lemmas_except_stopwords = None
    asl = None
    asl_stdev = None
    asl_rank = None
    msl = None
    asw = None
    s_count = None

    awl = None
    awl_stdev = None
    awl_rank = None
    mwl = None
    w_count = None

    ttr = None
    lex_den = None

    wq = None
    hwq = None
    chars_q = None
    fres = None
    gunning_fog = None
    ari = None
    smog = None
    l = None
    s = None
    cli = None


    blanchefort_prediction = None 
    blanchefort_positive = None
    blanchefort_negative = None
    blanchefort_neutral = None
    
        


    def __init__(self, filename):
        # self.text = open(f'{pathlib.Path(__file__).parent.parent.resolve()}/media/{text.file.name}', encoding='utf-8', mode="r").read()
        self.text = open(f'{pathlib.Path(__file__).parent.parent.resolve()}/media/{filename}', encoding='utf-8', mode="r").read()
        self.sentence_list = sent_tokenize(self.text.strip()) 
        #print(self.sentence_list[0:2])
        self.split_sentences_list = [remove_punctuation_and_tokenize(words) for words in self.sentence_list]
        #print(self.split_sentences_list[0:2])
        self.sentences_length_list = [len(sent) for sent in self.split_sentences_list]
        self.word_list = remove_punctuation_and_tokenize((' ').join(self.sentence_list))
        #print(self.word_list[0:2])
        self.list_of_lemmas = [morph.parse(word)[0].normal_form for word in self.word_list]
        self.words_length_list = [len(word) for word in self.word_list]
        self.lemmas_except_stopwords = [token for token in self.list_of_lemmas if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
        
    
    def load_basics(self):
        self.asl = statistics.mean(self.sentences_length_list)
        self.asl_stdev = statistics.stdev(self.sentences_length_list)
        self.asl_rank = stats.percentileofscore([entry.avg_sentence_length for entry in CorpusEntityData.objects.all() if entry.avg_sentence_length is not None], self.asl)
        self.msl = max(self.sentences_length_list)
        self.asw = np.mean(np.array([len(dic.inserted(va).split('-')) for va in ' '.join(self.word_list).split()]))
        self.awl = statistics.mean(self.words_length_list)
        self.awl_stdev = statistics.stdev(self.words_length_list)
        self.awl_rank = stats.percentileofscore([entry.avg_word_length for entry in CorpusEntityData.objects.all() if entry.avg_word_length is not None], self.awl)
        self.mwl = max(self.words_length_list)
        self.w_count = len(self.word_list)
        self.s_count = len(self.sentence_list)

    def load_vocab(self):
        self.ttr = len(set(self.list_of_lemmas)) / len(self.list_of_lemmas) if len(set(self.list_of_lemmas)) else 0
        self.lex_den = len(set(self.lemmas_except_stopwords)) / len(self.lemmas_except_stopwords) if len(set(self.lemmas_except_stopwords)) else 0

    def load_complexity(self):
        self.wq = len(np.array([va for va in ' '.join(self.word_list).split() if len(dic.inserted(va).split('-'))]))
        self.hwq = len(np.array([va for va in ' '.join(self.word_list).split() if len(dic.inserted(va).split('-')) > 2]))
        self.chars_q = sum(c.isalpha() or c.isdigit() for c in ('').join(self.sentence_list) )
        self.fres = 206.835 - (1.015 * self.asl) - (84.6 * self.asw)
        self.gunning_fog = 0.4 * (self.asl + ((self.hwq/self.wq)*100) )
        self.ari = 4.71 * (self.chars_q / len(self.word_list)) + 0.5 * (len(self.word_list) / len(self.sentence_list)) - 21.43
        self.smog = 1.043 * math.sqrt(self.hwq * 30 / len(self.sentence_list)) + 3.1291 if len(self.sentence_list) > 0 else 0
        self.l = sum(c.isalpha() for c in ('').join(self.sentence_list) ) / len(self.word_list) * 100
        self.s = len(self.sentence_list) / len(self.word_list) * 100
        self.cli = 0.0588 * self.l - 0.296 * self.s - 15.8
    
    def load_sentiment(self):
        self.blanchefort_prediction = [classifier(sentence) for sentence in sample(self.sentence_list, min(100, len(self.sentence_list)))]
        positive, negative, neutral = [],[],[]
        for pred in self.blanchefort_prediction:
          for cat in pred[0]:
            if cat['label'].lower() == 'positive':
              positive.append(cat['score'])
            if cat['label'].lower() == 'neutral':
              neutral.append(cat['score'])
            if cat['label'].lower() == 'negative':
              negative.append(cat['score'])
        self.blanchefort_positive = statistics.mean(positive)
        self.blanchefort_neutral = statistics.mean(neutral)
        self.blanchefort_negative = statistics.mean(negative)


def remove_punctuation_and_tokenize(sentence):
    return word_tokenize(sentence.translate(str.maketrans({a: None for a in string.punctuation})))


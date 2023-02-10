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
from .models import CorporaEntityData
from transformers import pipeline
from nltk import download
from nltk.corpus import stopwords

download('punkt')
download("stopwords")


classifier2 = pipeline("text-classification",model='blanchefort/rubert-base-cased-sentiment-rusentiment', top_k=3)
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








def calculate_metrics(metrics, data):
    


    words_length_list = [len(word) for word in data['word_list']]
    list_of_lists_of_words_for_each_sentence = []
    list_of_lemmas = []

    for word in data['word_list']:
      list_of_lemmas.append(morph.parse(word)[0].normal_form)

    list_of_lists_of_words_for_each_sentence = [remove_punctuation_and_tokenize(sentence) for sentence in data['sentences_list']]

    sentences_length_list = [len(s) for s in list_of_lists_of_words_for_each_sentence]


    
    if 'blanchefort_positive' in metrics or \
      'blanchefort_neutral' in metrics or \
      'blanchefort_negative' in metrics:
        blanchefort_prediction = [classifier2(sentence) for sentence in sample(data['sentences_list'], min(100, len(data['sentences_list'])))]
        positive, negative, neutral = [],[],[]
        for pred in blanchefort_prediction:
          for cat in pred[0]:
            if cat['label'].lower() == 'positive':
              positive.append(cat['score'])
            if cat['label'].lower() == 'neutral':
              neutral.append(cat['score'])
            if cat['label'].lower() == 'negative':
              negative.append(cat['score'])

    result_dictionary = {}
    for metric in metrics: 
        result_dictionary[metric] = None
    

    # block metadata
    result_dictionary['path'] = data['path']
    result_dictionary['id'] = data['id']
    result_dictionary['title'] = data['title']




    # block corpus typology
    if 'time_period' in metrics:
        result_dictionary['time_period'] = data['path'].split('RNC/')[1].split('/')[0]
    # TODO: add categorization
    if 'category' in metrics:
        result_dictionary['category'] = None
        for key in TEXT_TYPES.keys():
            if key in data['path']:
                result_dictionary['category'] = TEXT_TYPES[key]
    if 'author' in metrics:
        result_dictionary['author'] = None


    # block basic measurements
    if 'asl' in metrics:
        result_dictionary['asl'] = statistics.mean(sentences_length_list)
    if 'asl_std' in metrics:
        result_dictionary['asl_std'] = statistics.stdev(sentences_length_list)
    if 'msl' in metrics:
        result_dictionary['msl'] = max(sentences_length_list)
    if 'awl' in metrics:
        result_dictionary['awl'] = statistics.mean(words_length_list)
    if 'awl_std' in metrics:
        result_dictionary['awl_std'] = statistics.stdev(words_length_list)
    if 'mwl' in metrics:
        result_dictionary['mwl'] = max(words_length_list)
    if 'asw' in metrics:
        result_dictionary['asw'] = np.mean(np.array([len(dic.inserted(va).split('-')) for va in ' '.join(data['word_list']).split()]))

    # block vocabulary
    if 'type-token_ratio' in metrics:
        result_dictionary['type-token_ratio'] = len(set(list_of_lemmas)) / len(list_of_lemmas) if len(set(list_of_lemmas)) else 0
    
    if 'lexical_density1' in metrics:
        lemmas_except_stopwords = [token for token in list_of_lemmas if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation]
        result_dictionary['lexical_density1'] = len(set(lemmas_except_stopwords)) / len(lemmas_except_stopwords) if len(set(lemmas_except_stopwords)) else 0
    
    
    # block complexity 
    # check out https://en.wikipedia.org/wiki/Automated_readability_index
    if 'hard_words_quantity' in metrics:
        result_dictionary['hard_words_quantity'] = len(np.array([va for va in ' '.join(data['word_list']).split() if len(dic.inserted(va).split('-')) > 2]))
    if 'fres' in metrics:
        asl = len(data['word_list']) / len(data['sentences_list']) if len(data['sentences_list']) > 0 else 0
        asw = np.mean(np.array([len(dic.inserted(va).split('-')) for va in ' '.join(data['word_list']).split()]))
        result_dictionary['fres'] = 206.835 - (1.015 * asl) - (84.6 * asw)
    if 'gunning_fog' in metrics:
        asl = len(data['word_list']) / len(data['sentences_list']) if len(data['sentences_list']) > 0 else 0
        words_quantity = len(np.array([va for va in ' '.join(data['word_list']).split() if len(dic.inserted(va).split('-'))]))
        hard_words_quantity = len(np.array([va for va in ' '.join(data['word_list']).split() if len(dic.inserted(va).split('-')) > 2]))
        result_dictionary['gunning_fog'] = 0.4 * (asl + ((hard_words_quantity/words_quantity)*100) )
    if 'ari' in metrics:
        chars = sum(c.isalpha() or c.isdigit() for c in ('').join(data['sentences_list']) )
        result_dictionary['ari'] = 4.71 * (chars / len(data['word_list'])) + 0.5 * (len(data['word_list']) / len(data['sentences_list'])) - 21.43
    if 'smog' in metrics:
        hard_words_quantity = len(np.array([va for va in ' '.join(data['word_list']).split() if len(dic.inserted(va).split('-')) > 2]))
        result_dictionary['smog'] = 1.043 * math.sqrt(hard_words_quantity * 30 / len(data['sentences_list'])) + 3.1291 if len(data['sentences_list']) > 0 else 0
    if 'cli' in metrics:
        l = sum(c.isalpha() for c in ('').join(data['sentences_list']) ) / len(data['word_list']) * 100
        s = len(data['sentences_list']) / len(data['word_list']) * 100
        result_dictionary['cli'] = 0.0588 * l - 0.296 * s - 15.8

    # block sentiment analysis (rather raw)
    # https://huggingface.co/blanchefort/rubert-base-cased-sentiment-rusentiment
    if 'blanchefort_positive' in metrics:
        result_dictionary['blanchefort_positive'] = statistics.mean(positive)
    if 'blanchefort_neutral' in metrics:
        result_dictionary['blanchefort_neutral'] = statistics.mean(neutral)
    if 'blanchefort_negative' in metrics:
        result_dictionary['blanchefort_negative'] = statistics.mean(negative)

      
    return result_dictionary













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


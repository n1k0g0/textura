import glob
from hehexd import creds
import psycopg2
import random

SENTIMENT_TYPES = ['negative', 'neutral', 'positive']

TEXT_TYPES = {'brochures': 'brochures',
              'orth': 'christian',
              'drama': 'plays',
              'nauka': 'science',
              'oldgazette': 'newspapers',
              'politika': 'politics',
              'voennoe': 'military',
              'dnevniki': 'diaries',
              'doc/': 'doc',
              'ekonomika': 'economics',
              'memoir': 'memoir',
              'o_': 'about texts',
              'statji': 'publications',
              'Novelly': 'novels',
              'biogr': 'biographies',
              'litmanifesty': 'manifests'
              }

TEXT_TIME_PERIODS = [
    'xix',
    'xx',
    'xviii'
]

INSERT_QUERY = "insert into textura_test.corpus_test(name, time_period, type, general_sentiment) values "

paths = glob.glob('/Users/nikolay/Downloads/home/sarebrikov/qbic/merged_fixed_num/pre1950' + '/**/*.conllu',
                  recursive=True)

conn = psycopg2.connect(**creds)

values_to_insert = ""
q = "\'"
iteration = 0
try:
    for path in paths:
        iteration += 1
        entries = path.split('/')
        ttype = ''
        for key in TEXT_TYPES.keys():
            if key in path:
                ttype = TEXT_TYPES[key]
        ttime = ''
        for value in TEXT_TIME_PERIODS:
            if value in path:
                ttime = value
        tname = entries[len(entries) - 1].split('.')[0]
        insert_row = f'(\'{tname}\', \'{ttime}\', {q + ttype + q if len(ttype) else "NULL"}, \'{random.choice(SENTIMENT_TYPES)}\'); '
        values_to_insert += f'{"," if paths.index(path) != 0 else ""}(\'{tname}\', \'{ttime}\', {q + ttype + q if len(ttype) else "NULL"}, \'{random.choice(SENTIMENT_TYPES)}\') '
        cur = conn.cursor()
        cur.execute(INSERT_QUERY + insert_row)
        cur.close()
        conn.commit()
        print(insert_row)
    conn.close()
except Exception as e:
    print(e)
    conn.close()





#print(paths)
#print(periods)
#print(authors)
#print(text_types)



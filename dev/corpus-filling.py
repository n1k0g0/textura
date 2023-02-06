import glob
import psycopg2
import random

creds = {
    "host": "localhost",
    "port": "5433",
    "database": "texturadb",
    "user": "postgres",
    "password": ""
}


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

TEXT_TIME_PERIODS = [
    'xix',
    'xx',
    'xviii'
]

INSERT_QUERY = "insert into textura_test.corpus_test(name, time_period, type, general_sentiment) values "

paths = glob.glob('/Users/nikolay/Downloads/home/sarebrikov/qbic/merged_fixed_num/pre1950' + '/**/*.conllu',
                  recursive=True)

conn = psycopg2.connect(**creds)

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
        insert_row = f'(\'{tname}\', \'{ttime}\', {q + ttype + q if len(ttype) else "NULL"}); '
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



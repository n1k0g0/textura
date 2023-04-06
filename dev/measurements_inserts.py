import psycopg2
import random
from hehexd import creds

RESULT_VARIANTS = ['positive', 'negative', 'unexpected', 'suspicious', 'expected', 'neutral']
INSERT_QUERY = "insert into textura_test.measurements_test(text_id, metrics_id, result_score, result_text) values "

conn = psycopg2.connect(**creds)
cur = conn.cursor()
cur.execute("select * from textura_test.corpus_test")
corpus = cur.fetchall()
cur.close()
conn.close()
present_corpus_ids = []
for text in corpus:
    present_corpus_ids.append(text[0])

conn = psycopg2.connect(**creds)
cur = conn.cursor()
cur.execute("select * from textura_test.metrics_test")
metrics = cur.fetchall()
cur.close()
conn.close()

conn = psycopg2.connect(**creds)
cur = conn.cursor()
cur.execute("select * from textura_test.measurements_test")
measurements = cur.fetchall()
cur.close()
conn.close()

print(measurements)


conn = psycopg2.connect(**creds)
q = "\'"

try:
    for corpus_id in range(249, 10001):
        if corpus_id in present_corpus_ids:
            for metrics_id in range(1, len(metrics) + 1):
                insert_row = f'({corpus_id}, {metrics_id}, {("%.2f" % (random.uniform(0, 1) * 100))}, \'{random.choice(RESULT_VARIANTS)}\'); '
                cur = conn.cursor()
                cur.execute(INSERT_QUERY + insert_row)
                cur.close()
                conn.commit()
                print(insert_row)
    conn.close()
except Exception as e:
    print(e)
    conn.close()


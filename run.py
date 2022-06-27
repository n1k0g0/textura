#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import json
from src.validation.input_file_validation import *
from src.manager import Manager
import psycopg2
from hehehd import creds






MEASUREMENTS_MAP = {
    'Средняя длина предложения': 'avg(avg_sentence_length)'
}

if __name__ == "__main__":
    command = ""
    parser = argparse.ArgumentParser(description='Get average sentence length from a file.')
    parser.add_argument('filename', help='filename', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    first_cycle = True
    while command != "exit":
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="texturadb",
            user="postgres",
            password=creds
        )
        filename = ""
        if not len(sys.argv) > 1 or not first_cycle:
            print("\nВведите имя файла или \"exit\" для выхода")
            _input = input()
            while not is_valid_filename(_input):
                if _input == "exit":
                    exit()
                else:
                    print("Некорректное имя. Введите корректное имя файла:")
                    _input = input()
            filename = _input
        else:
            if first_cycle:
                filename = args.filename
            #print(filename)
        manager = Manager(filename)

        print("\nВведите команду: descriptive | spelling | exit")

        VALID_COMMANDS = {"descriptive", "exit", "spelling"}
        VALID_DIMENSIONS = {"time_period", "type"}
        valid_measurements = {}
        results = {}
        command = input()

        while command not in VALID_COMMANDS:
            print("Некорректная команда. Введите корректную команду")
            command = input()
        if command == "exit":
            exit()
        elif command == "descriptive":
            results = manager.analyse()
            print()
            sys.stdout.write(json.dumps(results, ensure_ascii=False))
            valid_measurements = set(results.keys())
            #print(valid_measurements)
            print()
        elif command == "spelling":
            print(manager.analyse_spelling())
        elif command == "preprocess":
            pass

        print("\nВведите название метрики")
        input_measurement_key = input()
        while input_measurement_key not in valid_measurements or input_measurement_key not in set(MEASUREMENTS_MAP.keys()):
            print("Некорректная метрика. Введите корректную метрику")
            input_measurement_key = input()

        print("\nВведите название проекции: time_period | type")
        input_dimension = input()
        while input_dimension not in VALID_DIMENSIONS:
            print("Некорректная проекция. Введите корректную проекцию")
            input_dimension = input()

        print(f"\nКорпус в разрезе \'{input_dimension}\' по метрике \'{input_measurement_key}\':")
        try:
            cur = conn.cursor()
            cur.execute(f'select {input_dimension}, {MEASUREMENTS_MAP[input_measurement_key]} from textura.test group by {input_dimension} order by {MEASUREMENTS_MAP[input_measurement_key]} asc')
            res = cur.fetchall()
            corpus_results = []
            corpus_similarities = []
            for row in res:
                if row[0] != '':
                    corpus_results.append({row[0]: float(row[1])})
                    corpus_similarities.append((row[0], abs(float(row[1]) - (results[input_measurement_key]))))
                    print(f'{row[0]}: {"%.2f" % float(row[1])}')


            sorted_list = sorted(corpus_similarities, key=lambda d: d[1])
            print(f'\nСудя по метрике \'{input_measurement_key}\'\nваш текст больше всего похож на группу {sorted_list[0][0]}')
            print(f'расстояния по метрике: {corpus_similarities}')
            cur.close()
            conn.commit()
        except Exception as e:
            print(e)
            conn.close()
        conn.close()

        first_cycle = False



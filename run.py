#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import json
from src.validation.input_file_validation import *
from src.manager import Manager


if __name__ == "__main__":
    command = ""
    parser = argparse.ArgumentParser(description='Get average sentence length from a file.')
    parser.add_argument('filename', help='filename', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    first_cycle = True
    while command != "exit":
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

        print("\nВведите команду: descriptive | exit")

        VALID_COMMANDS = {"descriptive", "exit"}
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
            print()
        elif command == "preprocess":
            pass
        first_cycle = False



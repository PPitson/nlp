import csv

from config import POLIMORFOLOGIK_DICT_PATH


def dictionary_words():
    with open(POLIMORFOLOGIK_DICT_PATH, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        return set(line[1].lower() for line in reader)

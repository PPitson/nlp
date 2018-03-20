import glob
import itertools
import json
import operator
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from commons import clear_text, tokenize_and_filter
from config import *
from morfologik import dictionary_words
from plot import plot_data
from spell import SpellCorrector

year_pattern = str(YEAR) + '-\d{2}-\d{2}'


def get_filenames_with_judgments_for_year(judgment_filenames):
    with open(FILENAMES_FOR_YEAR, 'w') as file:
        filenames_for_year = filter(contains_judgments_from_year, judgment_filenames)
        json.dump(list(filenames_for_year), file)


def contains_judgments_from_year(filename):
    return any(re.match(year_pattern, item['judgmentDate']) for item in get_judgments(filename))


def get_judgments(filename):
    with open(filename, encoding='utf-8') as file:
        content = json.load(file)
    return (item for item in content['items'] if re.match(year_pattern, item['judgmentDate']))


def generate_words(texts):
    for judgment_text in texts:
        yield from tokenize_and_filter(judgment_text)


def create_file_with_all_judgments(filenames):
    with open(ALL_JUDGMENTS_FILENAME, 'w', encoding='utf-8') as file:
        for judgment_filename in filenames:
            with open(judgment_filename, encoding='utf-8') as f:
                content = json.load(f)
            judgment_texts = '\n'.join(clear_text(item['textContent']) for item in content['items'])
            file.write(judgment_texts + '\n')


def create_counter_from_all_texts():
    def words_generator():
        with open(ALL_JUDGMENTS_FILENAME, encoding='utf-8') as f:
            for line in f:
                yield from tokenize_and_filter(line)

    return Counter(words_generator())


def main():
    all_judgment_filenames = glob.glob(PATH)

    if not os.path.isfile(FILENAMES_FOR_YEAR):
        get_filenames_with_judgments_for_year(all_judgment_filenames)

    with open(FILENAMES_FOR_YEAR) as file:
        filenames_with_judgments_for_year = json.load(file)
        judgments = itertools.chain.from_iterable(map(get_judgments, filenames_with_judgments_for_year))

    judgment_texts = (clear_text(judgment['textContent']) for judgment in judgments)

    if not os.path.isfile(WORD_COUNTS_FILENAME):
        counter = Counter(generate_words(judgment_texts))
        sorted_counter = Counter(dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True)))
        with open(WORD_COUNTS_FILENAME, 'w') as file:
            json.dump(sorted_counter, file)

    with open(WORD_COUNTS_FILENAME) as file:
        counter = json.load(file)

    plot_data(counter)
    dict_words = dictionary_words()
    diff = set(counter) - set(dict_words)

    if not os.path.isfile(HUGE_COUNTER_FILENAME):
        if not os.path.isfile(ALL_JUDGMENTS_FILENAME):
            create_file_with_all_judgments(all_judgment_filenames)
        counts_from_all_texts = create_counter_from_all_texts()
        with open(HUGE_COUNTER_FILENAME, 'w') as file:
            json.dump(counts_from_all_texts, file)

    with open(HUGE_COUNTER_FILENAME) as file:
        counts_from_all_texts = json.load(file)

    spell_corrector = SpellCorrector(counts_from_all_texts)

    with ProcessPoolExecutor(max_workers=6) as pool, open(CORRECTIONS, 'w', encoding='utf-8') as file:
        for word, corrected in zip(diff, pool.map(spell_corrector.correct, diff)):
            print(word, '->', corrected, file=file)


if __name__ == '__main__':
    main()

import glob
import itertools
import json
import operator
import os
import re

from config import *
from histogram import plot_histograms
from regexp import extract_money, references_article_of_regulation, contains_any_word_case

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


def main():
    judgment_filenames = glob.glob(PATH)

    if not os.path.isfile(FILENAMES_FOR_YEAR):
        get_filenames_with_judgments_for_year(judgment_filenames)

    with open(FILENAMES_FOR_YEAR) as file:
        filenames_with_judgments_for_year = json.load(file)
        judgments = list(itertools.chain.from_iterable(map(get_judgments, filenames_with_judgments_for_year)))

    judgment_texts = list(map(operator.itemgetter('textContent'), judgments))
    referenced_regulations = itertools.chain.from_iterable(map(operator.itemgetter('referencedRegulations'), judgments))

    money_values = list(itertools.chain.from_iterable(extract_money(judgment_text) for judgment_text in judgment_texts))
    plot_histograms(money_values)

    reference_count = sum(references_article_of_regulation(reference, REGULATION, ARTICLE)
                          for reference in referenced_regulations)
    print(f'Ilość odwołań do art. {ARTICLE} ustawy "{REGULATION}": {reference_count}')

    texts_with_szkoda_count = sum(contains_any_word_case(judgment_text, CASES) for judgment_text in judgment_texts)
    print(f'Liczba orzeczeń zawierających słowo szkoda w dowolnej formie fleksyjnej: {texts_with_szkoda_count}')


if __name__ == '__main__':
    main()

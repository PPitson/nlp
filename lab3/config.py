import os


def create_dir_if_doesnt_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


YEAR = 2009
PATH = 'F:\\saos\\data\\json\\judgments-*'
RESULTS_DIR = 'results'
HELPERS_DIR = 'helpers'

create_dir_if_doesnt_exist(RESULTS_DIR)
create_dir_if_doesnt_exist(HELPERS_DIR)

FILENAMES_FOR_YEAR = os.path.join(HELPERS_DIR, f'judgments_from_{YEAR}.json')
WORD_COUNTS_FILENAME = os.path.join(HELPERS_DIR, 'counts.json')
PLOT_FILENAME = os.path.join(RESULTS_DIR, 'plot.png')
ALL_JUDGMENTS_FILENAME = os.path.join(HELPERS_DIR, 'all_judgments.txt')
HUGE_COUNTER_FILENAME = os.path.join(HELPERS_DIR, 'huge_counter.json')
POLIMORFOLOGIK_DICT_PATH = 'polimorfologik\\polimorfologik-2.1.txt'
CORRECTIONS = os.path.join(RESULTS_DIR, 'corrections.txt')

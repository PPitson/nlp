import os
from itertools import tee, filterfalse
from textwrap import wrap

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

from config import HISTOGRAMS_DIR, YEAR


def partition(pred, iterable):
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def plot_histograms(money_values):
    plot_data(list(money_values), label='all')
    less_than_million, more_than_million = partition(lambda x: x >= 1e6, money_values)
    plot_data(list(less_than_million), label='less_than_million')
    plot_data(list(more_than_million), label='more_than_million')


def format_value(value, _):
    if value < 1e3:
        divider = 1
    elif value < 1e6:
        divider = 1e3
        suffix = 'tys.'
    elif value < 1e9:
        divider = 1e6
        suffix = 'mln'
    else:
        divider = 1e9
        suffix = 'mld'
    value = int(value // divider)
    return f'{value} {suffix}' if divider != 1 else str(value)


def plot_data(data, label):
    title_part = {
        'all': 'wszystkich wartości pieniężnych',
        'less_than_million': 'wartości pieniężnych poniżej 1 mln złotych',
        'more_than_million': 'wartości pieniężnych powyżej 1 mln złotych'
    }
    number_of_bins = 40
    x_min = min(data)
    x_max = max(data)
    plt.hist(data, bins=np.logspace(np.log10(x_min), np.log10(x_max), number_of_bins), rwidth=0.9)
    ax = plt.gca()
    ax.set_xlim(xmin=x_min, xmax=x_max)
    ax.set_yscale('log', nonposy='clip')
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(FuncFormatter(format_value))
    title = wrap(f'Histogram dla {title_part[label]} pojawiających się w tekstach orzeczeń z roku {YEAR}', width=60)
    plt.title('\n'.join(title))
    plt.xlabel('złotych')
    plt.ylabel('Liczba odniesień w tekstach')
    if not os.path.exists(HISTOGRAMS_DIR):
        os.makedirs(HISTOGRAMS_DIR)
    plt.savefig(os.path.join(HISTOGRAMS_DIR, label + '.png'))
    plt.show()

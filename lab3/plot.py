import matplotlib.pyplot as plt
import numpy as np

from config import PLOT_FILENAME


def plot_data(counter):
    words = list(counter.keys())
    counts = list(counter.values())
    indices = np.arange(len(words)) + 1
    plt.figure(figsize=(18, 18))
    plt.loglog(indices, counts, label='word count')
    plt.plot(indices, [counts[0] / x for x in indices], label='f(x) = max_count / x')
    plt.legend()
    ax = plt.gca()
    ax.set_xlim(xmin=1)
    ax.set_ylim(ymin=1)
    plt.xlabel('Word\'s position')
    plt.ylabel('Number of appearances in judgment texts')
    plt.savefig(PLOT_FILENAME)
    plt.show()

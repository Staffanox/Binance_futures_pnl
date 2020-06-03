import matplotlib.pyplot as plt
import numpy as np


def plot_bar(dates, values):
    y_pos = np.arange(len(dates))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, dates)
    plt.xticks(rotation=90)
    plt.ylabel("Profit")
    plt.grid()
    plt.show()


def decide_plot(plot_type: str, dates, values):
    if plot_type == "bar":
        plot_bar(dates, values)

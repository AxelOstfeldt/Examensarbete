import matplotlib.pyplot as plt
import numpy as np
import math

PlotNr = 1

#PlotNr 1. Bar plot for RiceCoding original input 

if PlotNr == 1:
    fig, ax = plt.subplots()

    title = ['1 k Hz tone', 'Drone sound', 'Static noise', 'Silence (Mic 20)', 'Large magnitude (Mic 217)']
    counts = [0.739, 0.809, 0.808, 0.125, 0.784]
    bar_labels = ['1 k Hz tone', 'Drone sound', 'Static noise', 'Silence (Mic 20)', 'Large magnitude (Mic 217)']
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple']
    for i in range(len(counts)):
        ax.bar(title[i], counts[i], label=bar_labels[i], color=bar_colors[i])

    ax.set_ylabel('Average compression rate')
    ax.legend()
    plt.ylim(0,1)
    plt.show()


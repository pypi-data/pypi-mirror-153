import os
import numpy as np

import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()

# do this before importing pylab or pyplot
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from django.conf import settings

from ..utils import remove_file, get_color


def create_bar_charts(name, titles, series, legend):
    path = os.path.join(settings.MEDIA_ROOT, 'stats', name)
    remove_file(path)

    x = np.arange(len(titles))

    plt.xticks(range(len(titles)), titles)

    colors = [
        get_color("2A437DFF"),
        get_color("9398C2FF"),
        get_color("A9B3EAFF")
    ]
    plt.bar(x + 0.00, series[0], color=colors[0], width=0.25)
    plt.bar(x + 0.25, series[1], color=colors[1], width=0.25)
    plt.bar(x + 0.50, series[2], color=colors[2], width=0.25)

    plt.legend(legend)
    plt.savefig(path, dpi=400)
    plt.clf()


def create_age_plot(items, title):
    path = os.path.join(settings.MEDIA_ROOT, 'stats/ages.png')
    remove_file(path)

    x = []
    y = []
    for item in items:
        x.append(item['age'])
        y.append(item['sum'])

    plt.xlim(20, 100)
    plt.ylim(0, 150)
    plt.title(title)
    plt.scatter(x, y, color=get_color("9398C2FF"))
    plt.ylabel("Nombre d'inscrits")
    plt.xlabel("Age")
    plt.savefig(path, dpi=400)
    plt.clf()

from rq3.region import Region
from rq3.partitioning import random_partition, quadtree_partition
from rq3.metrics import stdev_mean
import numpy as np

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt


def frange(x, y, jump=1.0):
    '''Range for floats.'''
    i = 0.0
    x = float(x)
    x0 = x
    epsilon = jump / 2.0
    yield x
    while x + epsilon < y:
        i += 1.0
        x = x0 + i * jump
        yield x


def heatmap(b, filename):
    plt.clf()
    cax = plt.imshow(b, cmap='binary', interpolation='nearest')
    plt.colorbar(cax, ticks=list(range(1, 21)))
    plt.savefig(filename)
    plt.close()

m = 50
n = 50

SCHEMES = [
    ('random', random_partition),
    ('quad',   quadtree_partition),
]

buff = np.random.randint(1, 21, size=(m, n)).tolist()
heatmap(buff, 'results/real.png')

for name, scheme in SCHEMES:
    for n in frange(0, 7, jump=0.5):
        r = Region.from_data(
            buff,
            metrics=stdev_mean(n),
            pscheme=scheme,
            )
        heatmap(r.fill(), 'results/%s-%s.png' % (name, n))

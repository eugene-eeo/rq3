from rq3 import Region
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
    plt.imshow(b, cmap='binary', interpolation='nearest')
    plt.savefig(filename)
    plt.close()

m = 50
n = 50

buff = np.random.randint(1, 21, size=(m, n)).tolist()
heatmap(buff, 'real.png')

for n in frange(0, 7, jump=0.5):
    r = Region.from_data(buff, target=n)
    heatmap(r.fill(), 'comp-%s.png' % n)

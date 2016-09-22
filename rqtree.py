from collections import namedtuple
import statistics as stats
import math


def yieldrows(r):
    for row in r:
        for item in row:
            yield item


def partition4(data):
    mid = len(data) // 2
    return [
        [r[0:mid] for r in data[0:mid]],
        [r[0:mid] for r in data[mid:]],
        [r[mid:] for r in data[0:mid]],
        [r[mid:] for r in data[mid:]],
    ]


class Box(namedtuple('Box', 'x0,x1,y0,y1')):
    def partition(self):
        x0, x1, y0, y1 = self
        mid = (x1 - x0) // 2
        return [
            Box(x0, x0 + mid, y0, y0 + mid),
            Box(x0, x0 + mid, y1 - mid, y1),
            Box(x1 - mid, x1, y0, y0 + mid),
            Box(x1 - mid, x1, y1 - mid, y1),
        ]


class Region:
    def __init__(self, data, target):
        self.data = data
        self.target = target

        self.mean = stats.mean(yieldrows(data))
        self.stdev = 0 if len(data) == 1 else \
            stats.pstdev(yieldrows(data), mu=self.mean)

    @property
    def acceptable(self):
        return self.stdev <= self.target

    def partition(self):
        if self.acceptable:
            return [self]
        return [Region(k, self.target) for k in partition4(self.data)]

from collections import namedtuple
import statistics as stats


def yieldrows(r):
    for row in r:
        for item in row:
            yield item


def partition4(data):
    size = len(data)
    mid = size // 2
    return [
        [r[0:mid] for r in data[0:mid]],
        [r[0:mid] for r in data[mid:]],
        [r[mid:] for r in data[0:mid]],
        [r[mid:] for r in data[mid:]],
    ]


class Region:
    def __init__(self, data, target):
        self.data = data
        self.size = len(data)
        self.target = target

        self.mean = stats.mean(yieldrows(data))
        self.stdev = stats.pstdev(yieldrows(data), mu=self.mean)

    @property
    def acceptable(self):
        return self.stdev <= self.target

    def partition(self):
        if self.acceptable:
            return [self]
        return [Region(k, self.target) for k in partition4(self.data)]

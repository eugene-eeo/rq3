from collections import namedtuple
import statistics as stats
import math


def yieldrows(r):
    for row in r:
        for item in row:
            yield item


Box = namedtuple('Box', 'x0,x1,y0,y1')


def partition_box(box):
    x0, x1, y0, y1 = box
    mid = (x1 - x0) // 2
    return [
        Box(x0, x0 + mid - 1, y0, y0 + mid - 1),
        Box(x0, x0 + mid - 1, y1 - mid, y1),
        Box(x1 - mid, x1, y0, y0 + mid - 1),
        Box(x1 - mid, x1, y1 - mid, y1),
    ]


def partition4(data):
    mid = len(data) // 2
    return [
        [r[0:mid] for r in data[0:mid]],
        [r[0:mid] for r in data[mid:]],
        [r[mid:] for r in data[0:mid]],
        [r[mid:] for r in data[mid:]],
    ]


class Region:
    def __init__(self, data, target, box):
        self.data = data
        self.target = target
        self.box = box
        self.mean = stats.mean(yieldrows(data))
        self.stdev = 0 if len(data) == 1 else \
            stats.pstdev(yieldrows(data), mu=self.mean)

    @property
    def ok(self):
        return self.stdev <= self.target

    def partition(self):
        if self.ok:
            yield self
            return
        for box, data in zip(partition_box(self.box), partition4(self.data)):
            yield Region(data, self.target, box)

    def __repr__(self):
        return 'Region(%r, µ=%r, σ=%r, ok=%r)' % (
                self.box,
                self.mean,
                self.stdev,
                self.ok,
                )

    @classmethod
    def from_data(cls, data, target):
        box = Box(0, len(data[0]) - 1, 0, len(data) - 1)
        return cls(data, target, box)

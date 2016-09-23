from collections import namedtuple
import statistics as stats
import math


def yieldrows(r):
    for row in r:
        for item in row:
            yield item


class Box(namedtuple('Box', 'x0,x1,y0,y1,data')):
    @staticmethod
    def from_data(data):
        return Box(0, len(data[0]), 0, len(data), data)

    def partition(self):
        x0, x1, y0, y1, data = self
        x_mid = (x1 - x0) // 2
        y_mid = (y1 - y0) // 2

        xm = x0 + x_mid
        ym = y0 + y_mid

        tl = [r[:x_mid] for r in data[:y_mid]]
        tr = [r[x_mid:] for r in data[:y_mid]]
        bl = [r[:x_mid] for r in data[y_mid:]]
        br = [r[x_mid:] for r in data[y_mid:]]

        if tl: yield Box(x0, xm, y0, ym, tl)
        if tr: yield Box(xm, x1, y0, ym, tr)
        if bl: yield Box(x0, xm, ym, y1, bl)
        if br: yield Box(xm, x1, ym, y1, br)


class Region:
    def __init__(self, box, target):
        self.box = box
        self.data = box.data
        self.target = target
        self.mean = stats.mean(yieldrows(box.data))
        self.stdev = 0 if len(box.data) == 1 else \
            stats.pstdev(yieldrows(box.data), mu=self.mean)

    @property
    def ok(self):
        return self.stdev <= self.target

    def partition(self):
        if self.ok:
            yield self
            return
        for box in self.box.partition():
            yield Region(box, self.target)

    def __repr__(self):
        return 'Region(%r)' % (self.box,)

    @classmethod
    def from_data(cls, data, target):
        return cls(Box.from_data(data), target)

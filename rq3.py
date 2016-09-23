from collections import namedtuple, deque
import statistics as stats
import math


class Box(namedtuple('Box', 'x0,x1,y0,y1,data')):
    @staticmethod
    def from_data(data):
        return Box(0, len(data[0]), 0, len(data), data)

    dx = property(lambda s: s.x1 - s.x0)
    dy = property(lambda s: s.y1 - s.y0)

    def seq(self):
        for row in self.data:
            for item in row:
                yield item

    def dimensions(self):
        return self.dx * self.dy

    def partition(self):
        x0, x1, y0, y1, data = self
        x_mid = (x1 - x0) // 2
        y_mid = (y1 - y0) // 2

        xm = x0 + x_mid
        ym = y0 + y_mid

        chunks = [
            Box(x0, xm, y0, ym, [r[:x_mid] for r in data[:y_mid]]),
            Box(xm, x1, y0, ym, [r[x_mid:] for r in data[:y_mid]]),
            Box(x0, xm, ym, y1, [r[:x_mid] for r in data[y_mid:]]),
            Box(xm, x1, ym, y1, [r[x_mid:] for r in data[y_mid:]]),
        ]

        for box in chunks:
            if box.dimensions() > 0:
                yield box


class Region:
    def __init__(self, box, target):
        self.box = box
        self.target = target
        self.mean = stats.mean(box.seq())
        self.stdev = 0 if box.dimensions() == 1 else \
            stats.pstdev(box.seq(), mu=self.mean)

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

    def write_to(self, buff):
        for x in range(self.box.x0, self.box.x1):
            for y in range(self.box.y0, self.box.y1):
                buff[y][x] = self.mean

    def fill(self):
        buff = [([0] * self.box.dx) for _ in range(self.box.dy)]
        proc = deque([self])
        while proc:
            r = proc.popleft()
            b = list(r.partition())
            for item in b:
                if item is r:
                    r.write_to(buff)
                    break
                proc.append(item)
        return buff

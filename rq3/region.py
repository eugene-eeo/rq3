from collections import deque
import statistics as stats
from rq3.box import Box
from rq3.partitioning import quadtree_partition


def rectangular_array(x, y):
    return [([0] * x) for _ in range(y)]


class Region:
    def __init__(self, box, data, target, pscheme):
        self.box = box
        self.data = data
        self.target = target
        self.pscheme = pscheme
        self.mean = stats.mean(box.seq(data))
        self.stdev = 0 if box.dimensions() == 1 else \
            stats.pstdev(box.seq(data), mu=self.mean)

    @classmethod
    def from_data(cls, data, target, pscheme=quadtree_partition):
        return cls(Box.from_data(data), data, target, pscheme)

    @property
    def should_partition(self):
        return self.stdev > self.target

    def partition(self):
        if self.should_partition:
            for box in self.box.partition(self.pscheme):
                yield Region(box, self.data, self.target, self.pscheme)
            return
        yield self

    def write_to(self, buff):
        for y in self.box.y_indexes():
            r = buff[y]
            for x in self.box.x_indexes():
                r[x] = self.mean

    def fill(self):
        buff = rectangular_array(self.box.width, self.box.height)
        proc = deque([self])
        while proc:
            r = proc.popleft()
            for item in r.partition():
                if item is r:
                    item.write_to(buff)
                    break
                proc.append(item)
        return buff

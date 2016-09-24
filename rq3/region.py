from collections import deque
from rq3.box import Box
from rq3.partitioning import quadtree_partition
from rq3.metrics import stdev_mean


def rectangular_array(x, y):
    return [([0] * x) for _ in range(y)]


class Region:
    def __init__(self, box, data, metrics, pscheme):
        self.box = box
        self.data = data
        self.should_partition, self.value = metrics(box, data)
        self.metrics = metrics
        self.pscheme = pscheme

    @classmethod
    def from_data(cls, data, metrics, pscheme=quadtree_partition):
        return cls(Box.from_data(data), data, metrics, pscheme)

    def partition(self):
        if self.should_partition:
            for box in self.box.partition(self.pscheme):
                yield Region(box, self.data, self.metrics, self.pscheme)
            return
        yield self

    def write_to(self, buff):
        for y in self.box.Y:
            r = buff[y]
            for x in self.box.X:
                r[x] = self.value

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

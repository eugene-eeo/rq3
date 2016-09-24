from collections import deque
import statistics as stats
from rq3.box import Box


def rectangular_array(x, y):
    return [([0] * x) for _ in range(y)]


class Region:
    def __init__(self, box, data, target):
        self.box = box
        self.data = data
        self.target = target
        self.mean = stats.mean(box.seq(data))
        self.stdev = 0 if box.dimensions() == 1 else \
            stats.pstdev(box.seq(data), mu=self.mean)

    @classmethod
    def from_data(cls, data, target):
        return cls(Box.from_data(data), data, target)

    @property
    def should_partition(self):
        return self.stdev > self.target

    def partition(self):
        if self.should_partition:
            for box in self.box.partition():
                yield Region(box, self.data, self.target)
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

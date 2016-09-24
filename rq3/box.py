from collections import namedtuple


class Box(namedtuple('Box', 'x0,x1,y0,y1')):
    @classmethod
    def from_data(cls, data):
        size = len(data)
        return cls(0, 0 if size == 0 else len(data[0]), 0, size)

    height = property(lambda s: s.y1 - s.y0)
    width = property(lambda s: s.x1 - s.x0)

    def x_indexes(self):
        return range(self.x0, self.x1)

    def y_indexes(self):
        return range(self.y0, self.y1)

    def seq(self, data):
        for y in self.y_indexes():
            row = data[y]
            for x in self.x_indexes():
                yield row[x]

    def dimensions(self):
        return self.height * self.width

    def partition(self, strategy):
        for box in strategy(self):
            if box.dimensions() > 0:
                yield box

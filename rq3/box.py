from collections import namedtuple


class Box(namedtuple('Box', 'x0,x1,y0,y1')):
    @classmethod
    def from_data(cls, data):
        size = len(data)
        return cls(0, 0 if size == 0 else len(data[0]), 0, size)

    height = property(lambda b: b.y1 - b.y0)
    width = property(lambda b: b.x1 - b.x0)

    X = property(lambda b: range(b.x0, b.x1))
    Y = property(lambda b: range(b.y0, b.y1))

    def seq(self, data):
        for y in self.Y:
            row = data[y]
            for x in self.X:
                yield row[x]

    def dimensions(self):
        return self.height * self.width

    def partition(self, scheme):
        for box in scheme(self):
            if box.dimensions() > 0:
                yield box

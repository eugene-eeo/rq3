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

    def partition(self):
        x0, x1, y0, y1 = self
        x_mid = (x1 - x0) // 2
        y_mid = (y1 - y0) // 2

        xm = x0 + x_mid
        ym = y0 + y_mid

        chunks = [
            Box(x0, xm, y0, ym),
            Box(xm, x1, y0, ym),
            Box(x0, xm, ym, y1),
            Box(xm, x1, ym, y1),
        ]

        for box in chunks:
            if box.dimensions() > 0:
                yield box

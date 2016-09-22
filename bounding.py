from collections import namedtuple


class Region(namedtuple('Region', 'x0,x1,y0,y1')):
    def contains(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    def subdivide(self):
        x0, x1, y0, y1 = self
        xm = (self.x0 + self.x1) / 2
        ym = (self.y0 + self.y1) / 2
        return [
            Region(x0, xm, y0, ym),
            Region(xm, x1, y0, ym),
            Region(x0, xm, ym, y1),
            Region(xm, x1, ym, y1),
        ]

    def resolution(self):
        return abs(self.x0 - self.x1)


class QuadTree:
    NODE_SIZE = 4

    def __init__(self, region=Region(0, 4, 0, 4)):
        self.region = region
        self.points = []
        self.children = None

    def insert(self, x, y):
        if not self.region.contains(x, y):
            return False

        if len(self.points) < self.NODE_SIZE:
            self.points.append((x, y))
            return True

        if self.children is None:
            self.children = [QuadTree(r) for r in self.region.subdivide()]

        for node in self.children:
            if node.insert(x, y):
                return True
        return False

    def __repr__(self):
        return '<QuadTree(%r) %r>' % (self.points, self.region)

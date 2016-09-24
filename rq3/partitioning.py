import random
from rq3.box import Box


def quadtree_partition(box):
    x0, x1, y0, y1 = box
    x_mid = (x1 - x0) // 2
    y_mid = (y1 - y0) // 2

    xm = x0 + x_mid
    ym = y0 + y_mid

    yield Box(x0, xm, y0, ym)
    yield Box(xm, x1, y0, ym)
    yield Box(x0, xm, ym, y1)
    yield Box(xm, x1, ym, y1)


def rrange(start, end):
    while True:
        point = random.randint(start + 1, end)
        yield (start, point)
        start = point
        if start == end:
            break


def random_partition(x0, x1, y0, y1):
    for x0, x1 in rrange(x0, x1):
        for y0, y1 in rrange(y0, y1):
            yield Box(x0, x1, y0, y1)

from itertools import islice
from random import randint
from rq3.region import Region
from rq3.partitioning import random_partition, quadtree_partition


def stream(a, b):
    while True:
        yield randint(a, b)


for scheme in [random_partition, quadtree_partition]:
    for m in islice(stream(1, 10), 10):
        for n in islice(stream(1, 10), 5):
            buff = [[randint(1, 10) for _ in range(n)] for _ in range(m)]
            r = Region.from_data(buff, target=0, pscheme=scheme)
            assert buff == r.fill()

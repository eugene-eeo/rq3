from pprint import pprint
from rqtree import Region
from itertools import islice
import random

print('5x5:')
r = Region.from_data([[0, 1, 2, 3, 4]]*5, target=0)
pprint(r.fill())


def stream(a, b):
    while True:
        yield random.randint(a, b)


for m in islice(stream(1, 10), 10):
    for n in islice(stream(1, 10), 5):
        buff = [[random.randint(1, 10) for _ in range(n)] for _ in range(m)]
        r = Region.from_data(buff, target=0)
        assert buff == r.fill()

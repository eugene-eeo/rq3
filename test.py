from itertools import islice
import random
from rq3.region import Region


def stream(a, b):
    while True:
        yield random.randint(a, b)


for m in islice(stream(1, 10), 10):
    for n in islice(stream(1, 10), 5):
        buff = [[random.randint(1, 10) for _ in range(n)] for _ in range(m)]
        r = Region.from_data(buff, target=0)
        assert buff == r.fill()

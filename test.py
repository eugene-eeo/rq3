from pprint import pprint
from rqtree import Region

print('5x5:')
r = Region.from_data([[0, 1, 2, 3, 4]]*5, target=0)
b = [k for k in r.partition()]
pprint(b)

for region in b:
    for k in region.partition():
        print(k)
        for g in k.partition():
            if g != k:
                print(' ', g)

pprint(r.fill())

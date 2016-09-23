from pprint import pprint
from rqtree import Region

print('5x5:')
r = Region.from_data([[0,1,2,3,4]]*5, target=0)
b = list((k, k.data) for k in r.partition())
pprint(b)

print()
print('4x4:')
r = Region.from_data([[0,1,2,3]]*4, target=0)
b = list((k, k.data) for k in r.partition())
pprint(b)

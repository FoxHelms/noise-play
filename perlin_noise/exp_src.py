import math
from perlin_noise.tools import each_with_each, hasher
from perlin_noise.rand_vec import RandVec

coordinates = (12,13)

if isinstance(coordinates, (int, float)):
            coordinates = [coordinates]


coordinates = list(
    map(lambda coordinate: coordinate * 1, coordinates),
)


coor_bounding_box = [
    (math.floor(coordinate), math.floor(coordinate + 1))
    for coordinate in coordinates
]

def get_from_cache_of_create_new(coors):
    RandVec(
        coors, 1 * hasher(coors),
    )

coors = (1,1)

#h = hasher(zeroes)

tit = get_from_cache_of_create_new((12,13))

# added = sum([
#     get_from_cache_of_create_new(coors) for coors in coor_bounding_box
# ])

l = [10 ** coordinate for coordinate in range(len(coors))]

d = sum([val1 * val2 for val1, val2 in zip(l, coors)])

print(d)
import math
import matplotlib.pyplot as plt
import random
from perlin_noise import PerlinNoise
from perlin_noise.rand_vec import RandVec

noise = PerlinNoise(octaves=10, seed=1)
xpix, ypix = 100, 100
# pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
pic = [[[i/xpix + j/ypix] for j in reversed(range(xpix))] for i in reversed(range(ypix))]



def dot(vec1,vec2):
    if len(vec1) != len(vec2):
        raise ValueError('lengths of two vectors are not equal')
    return sum([val1 * val2 for val1, val2 in zip(vec1, vec2)])

def foiler(arrays,prev=()):
    for el in arrays[0]:
        new = prev + (el,)
        if len(arrays) == 1:
            yield new
        else:
            yield from foiler(arrays[1:], prev=new)

def hasher(coors):
    return max(1,int(abs(dot([10 ** coordinate for coordinate in range(2)],coors,) + 1)))


# def hasher(coors):
#     return max(1,int(abs(dot([10 ** coordinate for coordinate in range(len(coors))],coors,) + 1)))


def sample_vector(dimensions, seed):
    
    st = random.getstate()
    random.seed(seed)

    vec = []
    for _ in range(dimensions):
        vec.append(random.uniform(-1, 1))  # noqa: S311

    random.setstate(st)
    return vec

#breakdown of noise function!!
# noise takes two floats, 0.75 and 0.75 and creates 0.1586900089235641
# nut = noise([0.75,0.75])
deez = [0.75,0.75]

# then it shifts everything to the right: 0.75 -> 7.5
deez_shifted = list(map(lambda d: d * 10, deez))

# Then, for each item it creates two  sub_items (for d in deez-shifted): [item1, item2] -> [(subitem1.1, subitem1.2), (subitem2.1, subitem2.2)]
# The first subitem is just the original number rounded down: 7.5 -> 7. (math.floor(d))
# The second subitem is the rounded numbere plus one: 7 -> 8 (math.floor(d + 1))
# [7.5,7.5] -> [(7,8),(7,8)]
deez_evolved = [(math.floor(d), math.floor(d + 1)) for d in deez_shifted]


# Let's break down the rest of the algo
# give = sum([RandVec(d, 1 * hasher(d)).product(list(map(lambda dist: fade(1 - abs(dist)),self.dists_to(coordinates)))) * dot(self.vec, self.dists_to(coordinates)) for d in deez_foiled])

# First, we create a generator whose output is the "foil" of the input: for d in deez_foiled
# So [(7,8),(7,8)] becomes [(7,7),(7,8)(8,7),(8,8)]
deez_foiled = foiler(deez_evolved)

# coors = d in generator!!!

deez_hashed = [hasher(d) for d in deez_foiled]
# Then we take each coordinate in the foil, the first would be (7,7), and run the hasher algorithm on it. 
#  return max(1,int(abs(dot([10 ** coordinate for coordinate in range(len(coors))],coors,) + 1)))
#      Simplified, the hasher algorithm:
#      adds 1 to the first index of the coordinate (7,7) -> (8,7)
#      does a dot product of the vector (1,10) and the changed coordinate, so: (1,10) * (8,7) -> 78
#      If for some reason this result is zero, then hasher just returns 1. 
# After running this on each item in the generator we get:
# [(7,7),(7,8)(8,7),(8,8)] -> [78,88,79,89]

#Next:
# 1 * hasher(d)
# We multiply each hashed value by the seed, in this case 1:

deez_seeded = [1 * d for d in deez_hashed]

# Next, a random vector object is created with each coordinate and it's seeded hash
# RandVec(d, deez_seeded)
# so, for the coordinate (7,7) and 78
# The coordinates are put into the attribute self.coordinates
# So here, self.coordinates = (7,7)
# And the seeded hash is used in this function
# sample_vector(dimensions=len(self.coordinates), seeded_hash)
# Which uses the random library to return a signed float
# sv = sample_vector(2,78)
# so here, self.vec = [0.6289562908956208, -0.8079541131822325]


# Next, we call the product function of the RandVec class 
# .product(list(map(lambda dist: fade(1 - abs(dist)),self.dists_to(coordinates))))
# From self.dists_to(coordinates)
# tuple(coor1 - coor2 for coor1, coor2 in zip(coordinates, self.coordinates))
# where coordinates = deez_shifted = (7.5,7.5) 
# self.coordinates = (7,7)
# so dists_to returns -> (7.5 - 7, 7.5 - 7) = (0.5, 0.5)
# 
# Then it 'fades' the floats. For different floats (0.49, 0.49) -> [0.5187450006000003, 0.5374600192000001]
# Our faded floats are just: [0.5, 0.5] for some reason??!
# and then product multiplies our faded floats together [0.5, 0.5] -> 0.25
# More interesting product return: [0.5187450006000003, 0.5374600192000001] -> 0.2788046979823802
randVec_first_index_product = 0.25

# Next we multiply this product by the dot product of the self vector and the dists_to vector:
# [0.6289562908956208, -0.8079541131822325] * (0.5, 0.5) -> -0.089498911143306

# Finally,
# We calculate this for every part of deez_seeded and sum them all together, and we return this sum: 0.1586900089235641
deez_sum = noise(deez)


print(deez_sum)




#print(deez_shifted)
#print(deez_evolved)






# plt.imshow(pic) #, cmap='gray')
# plt.show()

# print(pic[99][99])



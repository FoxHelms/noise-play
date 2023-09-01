import matplotlib.pyplot as plt
import math
from toying import hasher,foiler
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=10, seed=1)
# xpix, ypix = 100, 100

xpix, ypix = 5,5

plt.axis([0,xpix,0,ypix])

# pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
# Base Grad
# pic = [[[i/xpix + j/ypix] for j in range(xpix)] for i in range(ypix)]
# Shifted BaseGrad
# pic = [[list(map(lambda d: d * 10, [i/xpix + j/ypix])) for j in range(xpix)] for i in range(ypix)]
first_coords = [[y for y in range(ypix)] for _ in range(50)]
last_coords = [[y for y in reversed(range(ypix))] for _ in range(51, 100)]

# coords = first_coords + last_coords

# plt array = [[all x values at y = 0], [all x values at y = 1], ]

coords = [[1,2,3,4,5] for y in range(ypix)]

plt.imshow(coords, cmap='gray')
plt.show()
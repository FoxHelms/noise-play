import math
import random
import matplotlib.pyplot as plt
'''
Plan: 

Subdivision is not working correctly
Debug!!
'''

xgrid, ygrid = 64,64
plt.axis([0,xgrid,0,ygrid])
grad_lookup = [[(math.sqrt(2)/2),(math.sqrt(2)/2)],[-(math.sqrt(2)/2),(math.sqrt(2)/2)],[(math.sqrt(2)/2),-(math.sqrt(2)/2)],[-(math.sqrt(2)/2),-(math.sqrt(2)/2)]]
corner_grads = [grad_lookup[random.randint(0,3)],grad_lookup[random.randint(0,3)],grad_lookup[random.randint(0,3)],grad_lookup[random.randint(0,3)]]

def point_to_float(point):
    '''Take coordinate and convert to float'''
    return [p/xgrid for p in point]

def create_bounding_box(point):
    '''take float point and create int bounding box'''
    return [(math.floor(point[0]), math.floor(point[1])),(math.floor(point[0]) + 1, math.floor(point[1])),(math.floor(point[0]), math.floor(point[1]) + 1),(math.floor(point[0]) + 1, math.floor(point[1]) + 1)]

def dist_to_boundary(point_comp, bound_comp):
    '''Finds distance and direction between point and boundary for a dimension'''
    return point_comp - bound_comp

def alter_gradient(dimension_diff, grad_comp):
    '''Multiply the difference in coords for a dimension by the same dimension of the grad'''
    return dimension_diff * grad_comp

def smoothstep(t):
    """Smooth curve with a zero derivative at 0 and 1, making it useful for
    interpolating.
    """
    return t * t * (3. - 2. * t)

def fade(n):
    '''returns faded scalar'''
    return ((6 * n**5) - (15 * n**4) + (10 * n**3))

def lerp(t, a, b):
    """Linear interpolation between a and b, given a fraction t."""
    return a + t * (b - a)

def calculate_dot_prods(point, bounding_box,corner_grads):
    '''Wrapper for dot products'''
    dots = []
    for corner, grad in zip(bounding_box, corner_grads):
        dot = 0
        for p, d, g in zip(point, corner, grad):
            dim_diff = dist_to_boundary(p, d)
            dot += alter_gradient(dim_diff, g)    
        dots.append(dot)
    return dots

def smooth_dots(dots, new_point):
    '''Interpolate dot products to get smooth noise number'''
    count = 2
    while len(dots) > 1:
        count -= 1
        s_dim = smoothstep(new_point[count] - math.floor(new_point[count]))
        new_dots = []
        while dots:
            new_dots.append(lerp(s_dim, dots.pop(0), dots.pop(0)))
        dots = new_dots
    return dots[0] * 2 * 2 ** -0.5 # Scaling factor, should bring vals to [0,1]


def create_noise(point, level_detail):
    '''main noise gen function'''
    point = point_to_float(point)
    ret = 0
    for m in range(level_detail):
        multiplier = 1 << m
        new_point = []
        for p in point:
            p *= multiplier
            new_point.append(p)
        bounding_box = create_bounding_box(new_point)
        dots = calculate_dot_prods(new_point, bounding_box, corner_grads)
        ret += smooth_dots(dots, new_point) / multiplier
    # ret /= 2 - 2 ** (1 - level_detail)
    return ret
    
# print(create_noise([32,32], 5))

pic = [[create_noise([i, j], 4) for j in range(xgrid)] for i in range(ygrid)]

plt.imshow(pic, cmap='gray')
plt.show()

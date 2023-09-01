import random
import math

def rand_rad():
    '''gen random radian'''
    rn = random.uniform(0,1)
    return math.acos((2 * rn) - 1)

def rad_to_vec(rd):
    '''returns 2d cart unit vector'''
    urx = math.cos(rd)
    ury = math.sin(rd)
    return [urx,ury]

def calc_cell_point(coord, uvc):
    '''takes coordinate and rand unit vector and returns point on unit circle centered at coordinate'''
    return [coord[0] + uvc[0], coord[1] + uvc[1]]

def create_cell(coord, vec):
    '''takes coordinate and vector and returns cell coordinates'''
    x_cell_fac = y_cell_fac = 1
    if vec[0] < 0:
        x_cell_fac = -1
    if vec[1] < 0:
        y_cell_fac = -1
    p2 = [coord[0] + x_cell_fac, coord[1]]
    p3 = [coord[0], coord[1] + y_cell_fac]
    p4 = [coord[0] + x_cell_fac, coord[1] + y_cell_fac]
    return [coord, p2, p3, p4]

def calc_dir_vec(a, b):
    '''takes two vectors, a,b and calculates unit vector from a->b'''
    return [b[0]-a[0], b[1]-a[1]]    


def unit_vec_to_p(cell_coords, p):
    '''takes cell coords and random point within cell and returns direction unit vectors'''
    vec_to_p = []
    for corner in cell_coords:
        vec_to_p.append(calc_dir_vec(corner, p))
    return vec_to_p

def rand_vecs_at_corners(cell_coords):
    '''generates random 2d vector at each corner of the cell'''
    corner_vecs = []
    for corner in cell_coords:
        corner_vecs.append(rad_to_vec(rand_rad()))
    return corner_vecs

def vec_dot(a,b):
    '''takes vector op a dot b'''
    return sum([ac * bc for ac,bc in zip(a,b)])

def corner_vec_to_scalar(corner_vecs, vec_to_p):
    '''takes all corner vectors and dots them, return corner scalars'''
    return [vec_dot(cv,vtp) for cv, vtp in zip(corner_vecs,vec_to_p)]

def interpolate_corner_scalars(c_sclrs):
    '''bilinear interpolation on corner scalars'''
    return (((c_sclrs[0] + c_sclrs[1]) / 2) + ((c_sclrs[2] + c_sclrs[3]) / 2)) / 2


def my_noise(coords):
    '''takes coordinate pair and retuns scalar noise value'''
    ruv = rad_to_vec(rand_rad())
    p = calc_cell_point(coords, ruv)
    cell_coords = create_cell(coords, ruv)
    vec_to_p = unit_vec_to_p(cell_coords, p)
    corner_vecs = rand_vecs_at_corners(cell_coords)
    c_scalars = corner_vec_to_scalar(corner_vecs, vec_to_p)
    return interpolate_corner_scalars(c_scalars)



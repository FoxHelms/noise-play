import math
import random
import matplotlib.pyplot as plt
'''
Plan: package everything below into a PerSection method
'''
#xlim, ylim = 20, 20
#corners = [[0,0],[0,20],[20,0],[20,20]]



def calc_dir_vec(a, b):
    '''takes two vectors, a,b and calculates unit vector from a->b'''
    if a[0] == b[0] and a[1] == b[1]:
        return [0,0]
    x_comp = b[0]-a[0]
    y_comp = b[1]-a[1]
    mag = math.sqrt(x_comp**2 + y_comp**2)
    return [(x_comp/mag),(y_comp/mag)]    

def vec_dot(a,b):
    '''takes vector op a dot b'''
    return sum([ac * bc for ac,bc in zip(a,b)])

def bi_int(c_scalars, coords, corners):
    '''take coordinate and four corner scalars and return interpolated number'''
    xs = []
    ys = []
    for corner in corners:
        if corner[0] not in xs:
            xs.append(corner[0])
        if corner[1] not in ys:
            ys.append(corner[1])
    xs.sort()
    ys.sort()
    return ((c_scalars[0] * ((xs[1] - coords[0]) * (ys[1] - coords[1]))) + (c_scalars[1] * ((coords[0] - xs[0]) * (ys[1] - coords[1]))) + (c_scalars[2] * ((xs[1] - coords[0]) * (coords[1] - ys[0]))) + (c_scalars[3] * ((coords[0] - xs[0]) * (coords[1] - ys[0]))))/((xs[1] - xs[0]) * (ys[1]-ys[0]))

def fade(n):
    '''returns faded scalar'''
    faded = ((6 * n**5) - (15 * n**4) + (10 * n**3))
    if faded < -1:
        return -1
    if faded > 1:
        return 1
    return faded

def make_noise(p):
    '''take point and return scalar noise value'''
    corner_dirs = []
    corner_scalars = []
    for c in corners:
        corner_dirs.append(calc_dir_vec(c,p))
    for grad, dir in zip(corner_grads,corner_dirs):
        corner_scalars.append(vec_dot(grad,dir))
    return bi_int(corner_scalars,p,corners)
    # return fade(bi_int(corner_scalars,p,corners))


grad_lookup = [[(math.sqrt(2)/2),(math.sqrt(2)/2)],[-(math.sqrt(2)/2),(math.sqrt(2)/2)],[(math.sqrt(2)/2),-(math.sqrt(2)/2)],[-(math.sqrt(2)/2),-(math.sqrt(2)/2)]]
xgrid, ygrid = 500,500
steps = 10
section_length = xgrid // steps
plt.axis([0,xgrid,0,ygrid])
boxes = []

for y_slice in range(0, ygrid + 1, section_length):
    # Creates y boundaries for section
    ymin = y_slice
    ymax = y_slice + section_length
    for x_slice in range(0, xgrid + 1, section_length):
        # Creates x boundaries for section
        y_to_graph = []
        xmin = x_slice
        xmax = x_slice + section_length
        # Defines corners for section
        corners = [[xmin, ymin],[xmax,ymin],[xmin,ymax],[xmax,ymax]] 
        corner_grads = [grad_lookup[random.randint(0,3)],grad_lookup[random.randint(0,3)],grad_lookup[random.randint(0,3)],grad_lookup[random.randint(0,3)]]
        for y in range(ymin, ymax):
            # Loops through every y coord in section
            x_to_graph = []
            for x in range(xmin, xmax):
                # Loops through every x coord in at y-value and generates noise for coord pair
                # Appends noise value to list
                x_to_graph.append(make_noise([x,y]))
            # Appends x list to y list
            y_to_graph.append(x_to_graph)
        boxes.append(y_to_graph)


# print(len(boxes))

y_secs = []


for row_of_boxes in range(0, len(boxes) - section_length, section_length):
    
    for box_row_i in range(0,section_length):
        # One grid row
        x_temp = [] 
        for box_i in range(row_of_boxes,row_of_boxes + steps):
            # Loops through all boxes in an x row
            for n in boxes[box_i][box_row_i]:
                # Loops through each number in a list
                x_temp.append(n)
        y_secs.append(x_temp)





plt.imshow(y_secs, cmap='gray')
plt.show()
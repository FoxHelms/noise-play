import matplotlib.pyplot as plt
from pn_tools import my_noise

xpix, ypix = 100,100

plt.axis([0,xpix,0,ypix])

coords = [[my_noise([x,y]) for y in range(ypix)] for x in range(xpix)]

plt.imshow(coords, cmap='gray')
plt.show()
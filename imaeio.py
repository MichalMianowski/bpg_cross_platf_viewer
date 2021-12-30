import imageio as iio
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('image_test.png')
imgplot = plt.imshow(img)
plt.show()

images = list()
for file in Path("/home/mm/Pictures/").iterdir():
    im = iio.imread(file)
    images.append(im)


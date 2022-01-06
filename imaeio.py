import imageio as iio
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('image_test_2.jpg')
imgplot = plt.imshow(img)
plt.show()
#
# images = list()
# for file in Path("/home/mm/Pictures/").iterdir():
#     im = iio.imread(file)
#     images.append(im)
#
# for image in images:
#     iio.imwrite(Path("/home/mm/Pictures/output"), format="png")

# im = iio.imread("/home/mm/Pictures/ptak.jpeg")
# iio.imwrite(Path("/home/mm/Pictures/ptaszek.png"), im, format="png")
a = iio.formats
b = 1



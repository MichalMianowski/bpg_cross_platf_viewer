import imageio
import imageio as iio
import visvis as vv
from pathlib import Path
import bpg

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# img = mpimg.imread('jetplane.tif')
img = imageio.imread('image_samples/HappyFish.jpg')

# imageio.imsave("output.bpg", img)
imageio.imsave("output.bpg", img, qp=29,
            lossless=0, compress_level=8, preferred_chroma_format=444)
# img = imageio.imread('barbara.bmp')
# imgplot = plt.imshow(img)
a=1
# plt.show()

# vv.imshow(img)

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



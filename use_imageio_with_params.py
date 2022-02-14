import imageio
import bpg

img_path = "baboon.png"

img = imageio.imread(img_path)
# params you can use: qp, lossless, compress_level, preferred_chroma_format, color_space
imageio.imsave("output_file-1.bpg", img)
# saving with params looks like:
imageio.imsave("output_file-2.bpg", img, qp=2, preferred_chroma_format=444)

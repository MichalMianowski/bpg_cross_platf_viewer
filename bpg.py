# -*- coding: utf-8 -*-
# imageio is distributed under the terms of the (new) BSD License.

""" BPG plugin to load and save in bpg format.
    Format created to use HEVC encoding and decoding intra frame to encode and decode images.
    Format created by Bellard Thomas.
    Library with load/save func and imageio plugin created by Michal Mianowski.
"""

import numpy as np

from imageio import formats
from imageio.core import Format

from ctypes import CDLL, Structure, c_int, POINTER, c_char_p, pointer
from sys import platform


class DecodedImage(Structure):
    _fields_ = [
        ("w", c_int),
        ("h", c_int),
        ("pixel_len", c_int),
        ("has_alpha", c_int),
        ("is_grayscale", c_int),
        ("raw_data", POINTER(c_int))
    ]


def load_lib():
    shared_lib_path = "./bpg_load_save_lib.so"
    if platform.startswith('win32'):
        shared_lib_path = "./bpg_load_save_lib.dll"
    try:
        lib = CDLL(shared_lib_path)
        # print("Successfully loaded ", lib)
    except Exception as e:
        print(e)

    # arg:  str(FILEPATH).encode("utf_8")
    lib.load_bpg_image.restype = DecodedImage

    lib.save_bpg_image.argtype = [POINTER(DecodedImage), c_char_p, c_int, c_int, c_int, c_int]
    lib.save_bpg_image_with_defaults.argtype = [POINTER(DecodedImage)]

    return lib


class BpgFormat(Format):

    """BPG format created to use HEVC encoding and decoding intra frame to encode and decode images.
    This documentation is shown when the user does ``help('thisformat')``.

    Parameters for reading
    ----------------------
    filename : string
        path to file with a filename

    Parameters for saving
    ---------------------
    img : ndarray
    outfilename : string
    qp : int
        set quantizer parameter (smaller gives better quality, range: 0-51
        default value 29
    lossless : int
        enable lossless mode, values 0 or 1, default 0
    compress_level : int
        select the compression level (1=fast, 9=slow, default = 8)
    preferred_chroma_format : int
        set preferred chroma format for output file
        possible values: 444, 422 or 420
    """
    
    lib = load_lib()

    def _can_read(self, request):
        if request.mode[1] in (self.modes + "?"):
            if request.extension in self.extensions:
                return True

    def _can_write(self, request):
        if request.mode[1] in (self.modes + "?"):
            if request.extension in self.extensions:
                return True

    class Reader(Format.Reader):
        def _open(self):
            filename = self.request.filename
            self._decoded_image = BpgFormat.lib.load_bpg_image(str(filename).encode("utf_8"))

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass

        def _get_length(self):
            return 1

        def _get_data(self, index):
            pixel_len = self._decoded_image.pixel_len
            line_len = pixel_len * self._decoded_image.w
            im = np.ndarray((self._decoded_image.h, self._decoded_image.w, pixel_len), dtype=c_int)

            for y in range(self._decoded_image.h):
                for x in range(self._decoded_image.w):
                    if self._decoded_image.has_alpha:
                        im[y][x] = [self._decoded_image.raw_data[y*line_len + x*pixel_len], 
                                    self._decoded_image.raw_data[y*line_len + x*pixel_len + 1],
                                    self._decoded_image.raw_data[y*line_len + x*pixel_len + 2],
                                    self._decoded_image.raw_data[y*line_len + x*pixel_len + 3]]
                    else:
                        im[y][x] = [self._decoded_image.raw_data[y*line_len + x*pixel_len],
                                    self._decoded_image.raw_data[y*line_len + x*pixel_len + 1],
                                    self._decoded_image.raw_data[y*line_len + x*pixel_len + 2]]

            return im, {}

        def _get_meta_data(self, index):
            # Get the meta data for the given index. If index is None, it
            # should return the global meta data.
            return {}  # This format does not support meta data


    """
    Parameters for saving
    ---------------------
    img : ndarray
    outfilename : string
    qp : int
        set quantizer parameter (smaller gives better quality, range: 0-51
        default value 29
    lossless : int
        enable lossless mode, values 0 or 1, default 0
    compress_level : int
        select the compression level (1=fast, 9=slow, default = 8)
    preferred_chroma_format : int
        set preferred chroma format for output file
        possible values: 444, 422 or 420
    """
    class Writer(Format.Writer):
        def _open(self, **kwargs):
            self.c_outfilename = str(self.request.filename).encode("utf_8")

            # DEFAULT VALUES
            self.qp = 29
            self.lossless = 0
            self.compress_level = 8
            self.preferred_chroma_format = 444

            if 'qp' in kwargs.keys():
                if (kwargs['qp'] >=0) and (kwargs['qp'] <= 51):
                    self.qp = kwargs['qp']
            if 'lossless' in kwargs.keys():
                if kwargs['lossless'] in {0, 1}:
                    self.lossless = kwargs['lossless']
            if 'compress_level' in kwargs.keys():
                if (kwargs['compress_level'] >=1) and (kwargs['compress_level'] <= 9):
                    self.compress_level = kwargs['compress_level']
            if 'preferred_chroma_format' in kwargs.keys():
                if kwargs['preferred_chroma_format'] in {444, 422, 420}:
                    self.preferred_chroma_format = kwargs['preferred_chroma_format']

        def _close(self):
            # Close the reader.
            # Note that the request object will close self._fp
            pass

        def _append_data(self, im, meta):
            self._decoded_image = DecodedImage()

            h = im.shape[0]
            w = im.shape[1]

            if len(im.shape) == 2:
                pixel_len = 1
                is_grayscale = 1
            else:
                pixel_len = im.shape[2]
                is_grayscale = 0

            if pixel_len == 4:
                has_alpha = 1
            else:
                has_alpha = 0

            line_len = w * pixel_len
            c_decoded_array = np.zeros(h * line_len, dtype=c_int)

            if pixel_len != 1:
                for y in range(h):
                    for x in range(w):
                        for i in range(pixel_len):
                            c_decoded_array[y*line_len + x*pixel_len + i] = im[y][x][i]
            else:
                for y in range(h):
                    for x in range(w):
                        c_decoded_array[y * line_len + x] = im[y][x]

            self._decoded_image.h = h
            self._decoded_image.w = w
            self._decoded_image.pixel_len = pixel_len
            self._decoded_image.has_alpha = has_alpha
            self._decoded_image.is_grayscale = is_grayscale
            self._decoded_image.raw_data = c_decoded_array.ctypes.data_as(POINTER(c_int))

            BpgFormat.lib.save_bpg_image(pointer(self._decoded_image), self.c_outfilename, self.qp,
                                         self.lossless, self.compress_level, self.preferred_chroma_format)
            # BpgFormat.lib.save_bpg_image_with_defaults(pointer(self._decoded_image))

    def set_meta_data(self, meta):
            # Process the given meta data (global for all images)
            # It is not mandatory to support this.
            # raise RuntimeError("The dummy format cannot write meta data.")
            pass


# Register. You register an *instance* of a Format class. Here specify:
format = BpgFormat(
    "bpg",  # short name
    "BPG format - enc/decoding images as intra frame in HEVC",  # one line descr.
    ".bpg",  # list of extensions
    "iI",  # modes, characters in iIvV
)

formats.add_format(format)
print("Added BPG format to imageio")

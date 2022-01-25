from ctypes import CDLL, Structure, c_int, POINTER, c_char_p
from sys import platform

shared_lib_path = "./bpg_load_save_lib.so"
if platform.startswith('win32'):
    shared_lib_path = "./bpg_load_save_lib.dll"

try:
    lib = CDLL(shared_lib_path)
    print("Successfully loaded ", lib)
except Exception as e:
    print(e)


class DecodedImage(Structure):
    _fields_ = [
        ("w", c_int),
        ("h", c_int),
        ("has_alpha", c_int),
        ("is_grayscale", c_int),
        ("image_array", POINTER(POINTER(c_int)))
    ]

# arg:  str(FILEPATH).encode("utf_8")
lib.load_bpg_image.restype = DecodedImage

lib.save_bpg_image.argtype = [POINTER(DecodedImage), c_char_p, c_int, c_int, c_int, c_int]
lib.save_bpg_image_with_defaults = [POINTER(DecodedImage)]

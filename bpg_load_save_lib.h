#ifndef _BPG_LOAD_SAVE_LIB_H
#define _BPG_LOAD_SAVE_LIB_H

#ifdef __cplusplus
extern "C" {
#endif

#include "bpgenc.h"

#define DEFAULT_OUTFILENAME "out.bpg"
#define DEFAULT_QP 29
#define DEFAULT_LOSSLESS 0
#define DEFAULT_COMPRESS_LEVEL 8
#define DEFAULT_PREFFERED_CHROMA_FORMAT 420
#define DEFAULT_BIT_DEPTH 8
#define DEFAULT_COLOR_SPACE 0

DecodedImage load_bpg_image(char *filename);

int save_bpg_image(DecodedImage *decoded_image, char *outfilename, int qp, 
                int lossless, int compress_level, int preffered_chroma_format, int output_color_space);

int save_bpg_image_with_defaults(DecodedImage *decoded_image);

/** defined in bpgenc:  ------------------------------------------------------------------------
*
* typedef struct DecodedImage
* {
*     int w, h, pixel_len, has_alpha, is_grayscale;
*     int * raw_data;
* } DecodedImage;
*
*
*
*arguments of save_bpg_image function
*    qp : set quantizer parameter (smaller gives better quality, range: 0-51
*    lossless : enable lossless mode, values 0 or 1
*    compress_level : select the compression level (1=fast, 9=slow) -- not valid with JCTVC encoder
*    preferred_chroma_format : set preferred chroma format for output file
*        possible values: 444, 422 or 420
*    output_color_space : set output color space (int as arg input)
*        values:
*        0 - YCbCr
*        1 - RGB
*        2 - YCgCo
*        3 - YCbCr_BT709
*        4 - YCbCr_BT2020
*
*/

#ifdef __cplusplus
}
#endif

#endif
# -*- coding: utf-8 -*-
# distutils: language=c++
# cython: language_level=3
# cython: c_string_type=unicode, c_string_encoding=utf8
"""
    Provides access to the bgef_writer interface.
"""

from .bgef_writer cimport *
cimport numpy as np


def generate_bgef(input_file, bgef_file,  n_thread = 8, bin_sizes = None, region = None):
    """
    Function to generate common bin GEF file(.bgef).
    :param input_file:  The input file path of gem file or bin1 bgef.
    :param bgef_file:   Output BGEF filepath.
    :param n_thread:    Number of thread, default 8
    :param bin_sizes:   A list of bin sizes, default: 1,10,20,50,100,200,500
    :param region:      A list of region, (minX, maxX, minY, maxY)
    :return:
    """
    cdef vector[unsigned int] bin_sizes_tmp
    if bin_sizes is None:
        bin_sizes_tmp = {1, 10, 20, 50, 100, 200, 500}
    else:
        #bin_sizes_tmp = bin_sizes
        bin_sizes_tmp.push_back(bin_sizes)

    if region is None:
        generateBgef(input_file, bgef_file, n_thread, bin_sizes_tmp)
    else:
        generateBgef(input_file, bgef_file, n_thread, bin_sizes_tmp, region)

#def SdDataToGef(out_file, bin_size, sz, np.ndarray[unsigned long, ndim=1] cells):
#    StereoDataToGef(out_file, bin_size, sz, &cells[0])

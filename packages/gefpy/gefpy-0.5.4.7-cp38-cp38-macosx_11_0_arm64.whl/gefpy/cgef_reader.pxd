# distutils: language=c++
# cython: language_level=3
import numpy as np
cimport numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool

from .gef cimport *

cdef extern from "cgef_reader.h" nogil:
    cdef cppclass CgefReader:
        CgefReader(const string &filename, bool verbose)
        unsigned short getGeneNum() const;
        unsigned int getCellNum() const;
        unsigned int getExpressionNum() const;

        void getGeneName(char * gene_list)

        int getGeneId(string& gene_name)
        GeneData *getGene()
        GeneData getGene(unsigned short gene_id) const
        CellData *getCell()
        CellData getCell(unsigned int cell_id) const

        void getGeneNameList(vector[string] & gene_list)
        void getGeneNames(char * gene_list)
        void getCellNameList(unsigned long long int * cell_name_list)

        int getSparseMatrixIndices(unsigned int * indices,
                                   unsigned int * indptr,
                                   unsigned int * count,
                                   const char * order)

        int getSparseMatrixIndices2(unsigned int * cell_ind, unsigned int * gene_ind, unsigned int * count)

        void restrictRegion(unsigned int min_x, unsigned int max_x, unsigned int min_y, unsigned int max_y)

        void restrictGene(vector[string] & gene_list, bool exclude)

        bool isRestrictRegion() const

        bool isRestrictGene() const

        void updateGeneInfo()

        void freeRestriction()

        void getCellIdAndCount(unsigned int *cell_id, unsigned short *count) const

        void getGeneIdAndCount(unsigned short *gene_id, unsigned short *count) const

        void closeH5()

        char* getCellBorders_char(bool ball, unsigned int cell_id)
        short* getCellBorders_short(bool ball, unsigned int cell_id)
        
        unsigned int* getGefVer()


'''
Author: zhaozijian
Date: 2022-02-16 14:12:12
LastEditors: zhaozijian
LastEditTime: 2022-04-26 13:36:30
Description: file content
'''
import h5py
import numpy as np

def gef_is_cell_bin(gef_file):
    h5f = h5py.File(gef_file)
    if 'cellBin' in h5f:
        h5f.close()
        return True
    else:
        h5f.close()
        return False

def StereoDataToGef(path, bin, expression, gene, attr):
    h5f = h5py.File(path,"w")
    geneExp = h5f.create_group("geneExp")
    binsz = "bin"+str(bin)
    bing = geneExp.create_group(binsz)

    #genetype = np.dtype({'names':['gene','offset','count'], 'formats':['S32', 'i','i']})
    #exptype = np.dtype({'names':['x','y','count'], 'formats':['i', 'i','i']})

    geneExp[binsz]["expression"] = expression #np.arry([(10,20,2), (20,40,3)], dtype=exptype)
    geneExp[binsz]["gene"] = gene #np.arry([("gene1",0,21), ("gene2",21,3)], dtype=genetype)

    bing["expression"].attrs.create("minX", attr[0])
    bing["expression"].attrs.create("minY", attr[1])
    bing["expression"].attrs.create("maxX", attr[2])
    bing["expression"].attrs.create("maxY", attr[3])
    bing["expression"].attrs.create("minExp", attr[4])
    bing["expression"].attrs.create("resolution", attr[5])

    h5f.attrs.create("version", 2)
    
    h5f.close()
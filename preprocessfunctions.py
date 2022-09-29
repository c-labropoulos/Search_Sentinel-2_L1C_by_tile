import os
import stat
import zipfile
from functions import zipopener, readsentinelProduct, filecreator, removezip, print_menu  # , productfinder
import sys
import subprocess
#sys.path.append('/home/chris/PycharmProjects/pythonProject1/venv/lib/python3.10/site-packages/snappy') # or sys.path.insert(1, '<snappy-dir>')
sys.path.append('C:\\Users\\PC\\anaconda3\\envs\\snapenv\\Lib')
import snappy
from snappy import (ProductIO, ProductUtils, ProgressMonitor)
from snappy import Product
import shutil
from distutils.dir_util import copy_tree
import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import  numpy as np
import tkinter
from  tkinter import *
from snappy import jpy
from snappy import GPF
from snappy import ProductIO
from snappy import HashMap
import xml.etree.ElementTree as ET
from snappy import  WKTReader
import numpy as np
from snappy import Product, ProductIO, ProductUtils, ProductData

#import opencv as cv2
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
HashMap = jpy.get_type('java.util.HashMap')
SubsetOp =jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
WKTReader = jpy.get_type('com.vividsolutions.jts.io.WKTReader')

# Disable JAI native MediaLib extensions
System = jpy.get_type('java.lang.System')
System.setProperty('com.sun.media.jai.disableMediaLib', 'true')
PrintPM = jpy.get_type('com.bc.ceres.core.PrintWriterProgressMonitor')
# or a more concise implementation
ConcisePM = jpy.get_type('com.bc.ceres.core.PrintWriterConciseProgressMonitor')
System = jpy.get_type('java.lang.System')

def readxml():
    file_pathxml, filename = filecreator()
    # Read File
    df = readsentinelProduct(file_pathxml)
    # Get the list of Band Names
    print("Sentinel product was read")
    return file_pathxml,filename,df

def resampleandsubset(df):
    print("Starting preprocessing")
    print('Step 1/2 : Resampling')
    parameters = HashMap()
    parameters.put('targetResolution', 10)
    result = snappy.GPF.createProduct('Resample', parameters, df)
    print("Resample product ready")
    print('Step 2/2 : Subset')
    # wkt = 'POLYGON( (21.249362999999998 39.2489500000000007,21.4993750000000006 39.2489500000000007, 21.4993750000000006  39.4990219999999965, 21.249362999999998 39.4990219999999965,21.249362999999998 39.2489500000000007))'
    op = SubsetOp()
    op.setSourceProduct(result)
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion',
                   'POLYGON( (21.249362999999998 39.2489500000000007,21.4993750000000006 39.2489500000000007, 21.4993750000000006  39.4990219999999965, 21.249362999999998 39.4990219999999965,21.249362999999998 39.2489500000000007))')
    sub_product = GPF.createProduct('Subset', parameters, result)
    print("Subset product ready\n")

    return sub_product
def showsub(sub_product):
    print("Preprocessing finished")
    answer = input("Do yo to see the the preprocessed product Y/N : ")
    while answer.lower().strip() not in ('y', 'n'):
        answer = input("Do yo to see the the preprocessed product Y/N : ")

    if answer.lower().strip() == 'n':
         subprocess.call(['python', 'Sentinelsatscript.py'])
    elif answer.lower().strip() == 'y':
        sub_b6 = sub_product.getBand('B6')
        print("band read")
        width = sub_b6.getRasterWidth()
        height = sub_b6.getRasterHeight()
        print("subset size : ", width, height)
        sub_b6_data = np.zeros(width * height, dtype=np.float32)
        sub_b6.readPixels(0, 0, width, height, sub_b6_data)
        sub_b6_data.shape = height, width

        plt.figure(1)
        fig = plt.imshow(sub_b6_data, cmap=cm.gray)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.show()
def savefile(sub_product,filename):
 pm = PrintPM(System.out)
 ProductIO.writeProduct(sub_product, 'IMG_DATA_preprocessed/'+filename+'.tif', 'GeoTIFF',pm)#-BigTIFF')
 print("Subset product written")
 removezip(filename)
 #safestring='IMG_DATA_preprocessed/'+filename+'.tif'
 #return safestring

def ndviproduct(sub_product):
    product = ProductIO.readProduct(sub_product)
    print("Product read")
    width = product.getSceneRasterWidth()
    height = product.getSceneRasterHeight()
    product_name = product.getName()
    # input product red & nir bands
    red_band = product.getBand('B4')
    nir_band = product.getBand('B8')
    # output product (ndvi) & new band
    output_product = Product('NDVI', 'NDVI', width, height)
    ProductUtils.copyGeoCoding(product, output_product)
    output_band = output_product.addBand('ndvi', ProductData.TYPE_FLOAT32)
    # output writer
    output_product_writer = ProductIO.getProductWriter('GeoTIFF')
    output_product.setProductWriter(output_product_writer)
    output_product.writeHeader(product_name + '.ndvi.tif')

    # compute & save ndvi line by line
    red_row = np.zeros(width, dtype=np.float32)

    nir_row = np.zeros(width, dtype=np.float32)
    for y in range(height):
        red_row = red_band.readPixels(0, y, width, 1, red_row)

        nir_row = nir_band.readPixels(0, y, width, 1, nir_row)

        ndvi = (nir_row - red_row) / (nir_row + red_row)
       # print(ndvi)
        output_band.writePixels(0, y, width, 1, ndvi)

    output_product.closeIO()
    print("NDVI product completed")
    desstinationndvi = '/IMG_DATA_NDVI'
    if os.path.exists(product_name + '.ndvi.tif'):
        shutil.copy2(product_name + '.ndvi.tif', desstinationndvi)
        os.remove(product_name + '.ndvi.tif')
    if os.path.exists(product_name + '.ndvi.data'):
        # os.chmod(product_name + '.ndvi.data',  stat.S_IWRITE)
        copy_tree(product_name + '.ndvi.data', desstinationndvi)
        #  os.remove(product_name + '.ndvi.data')
        shutil.rmtree(product_name + '.ndvi.data')
  #  print(os.listdir('C:/Users/PC/PycharmProjects/comballthesent'))
    print("NDVI product written")



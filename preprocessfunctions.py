import os
import zipfile
from functions import zipopener, readsentinelProduct, filecreator, removezip  # , productfinder
import sys
#sys.path.append('/home/chris/PycharmProjects/pythonProject1/venv/lib/python3.10/site-packages/snappy') # or sys.path.insert(1, '<snappy-dir>')
sys.path.append('C:\\Users\\PC\\anaconda3\\envs\\snapenv\\Lib')
import snappy
from snappy import (ProductIO, ProductUtils, ProgressMonitor)
from snappy import Product

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

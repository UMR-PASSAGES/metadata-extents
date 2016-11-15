#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################
# This script adds rectangular extents to create an
# ASC raster with a value of 0 if 0 extents are present,
# 1 if 1 extent is present, etc.
#
# Metadata extents are read in a CSV file which
# must have minx, maxx, miny and maxy columns.
#
# Resolution (in degrees) can be set in the script.
#####################################################

import numpy as np
import pandas as pd
import decimal
import datetime

############
# variables
############

# resolution (same unit as coordinates used in CSV)
res = 0.01
# path and name of CSV file
csv = '../01_donnees/emprises_nat_valid.csv'
# delimiter of input CSV : comma, semicolon...
mySep = ','
# quotechar of input CSV : ' or "...
myQuotechar = "'"
# names of CSV columns
colminx = 'minx'
colmaxx = 'maxx'
colminy = 'miny'
colmaxy = 'maxy'
# output raster (to be created)
raster = '../03_resultats/tout/emprises_nat_res001.asc'
# log file (to be created)
log = '../03_resultats/tout/emprises_nat_res001.txt'


############
# functions
############

# rounds a coordinate according to resolution (45.52 will be rounded to 45.5 if res = 0.5)
def roundcoord(n):
    nbdec = decimal.Decimal(str(res))
    nbdec = -1 * nbdec.as_tuple().exponent
    t = round(n/res, 0)
    rounded = round(t * res, nbdec)
    return rounded

# transforms a coordinate into a column or row number, based on resolution
def getcol(n):
    col = n/res + 180/res
    return col
def getrow(n):
    row = 90/res - n/res
    return row

# transforms an array into an ASC raster
# https://en.wikipedia.org/wiki/Esri_grid
def arrayToRaster(myRaster, myArray):
    if not myRaster.endswith('.asc'):
        myRaster = myRaster + '.asc'
    input = open(myRaster, 'w')
    # heading
    input.write('ncols ' + str(myArray.shape[1]) + '\n')
    input.write('nrows ' + str(myArray.shape[0]) + '\n')
    input.write('xllcorner -180\n')
    input.write('yllcorner -90\n')
    input.write('cellsize ' + str(res) + '\n')
    input.write('nodata_value -9999\n')
    # values
    for row  in range(myArray.shape[0]):
        for value in myArray[row]:
            input.write(str(value) + ' ')
    input.close()


############
# let's go !
############

# open log file
log = open(log, 'w')
# heading of log file
log.write('execution of metadataExtents.py' + '\n')
begindate = datetime.datetime.now()
log.write('begin : ' + str(begindate) + '\n')
log.write('input CSV file : ' + csv + '\n')
log.write('output raster : ' + raster + '\n')
log.write('resolution : ' + str(res) + '\n')

print ('calculating...')

# get number of rows and columns based on resolution
nbrow = 180/res + 1
nbcol = 360/res + 1

# creates corresponding array of zeros, type integer
a = np.zeros((nbrow,nbcol), dtype='i')

# reads CSV file
df = pd.read_csv(csv, sep=mySep, quotechar=myQuotechar)

# iterates over rows to get current coordinates
for index, row in df.iterrows():
    # in case min and max are inverted
    x = [row[colminx], row[colmaxx]]
    minx = min(x)
    maxx = max(x)
    y = [row[colminy], row[colmaxy]]
    miny = min(y)
    maxy = max(y)

    # rounds coordinates
    minx = roundcoord(minx)
    maxx = roundcoord(maxx)
    miny = roundcoord(miny)
    maxy = roundcoord(maxy)

    # get rows and columns numbers from coordinates
    mincol = getcol(minx)
    maxcol = getcol(maxx)
    minrow = getrow(maxy)
    maxrow = getrow(miny)
    
    # add corresponding values to array (+1)
    a[minrow+1:maxrow+1,mincol:maxcol] = a[minrow+1:maxrow+1,mincol:maxcol] + 1

# transforms array into ASC raster
print ('creating raster file...')
arrayToRaster(raster, a)

# for log file
enddate = datetime.datetime.now()
log.write('end : ' + str(enddate) + '\n')
duration_ms = (enddate - begindate).total_seconds() * 1000
log.write('duration in milliseconds : ' + str(duration_ms))
log.close()


#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

#####################################################
# This script takes 2 ASC files of same sizes extents and resolution
# and substract the 2nd from the 1st
# The result is another ASC file
#
#####################################################

import sys

############
# variables
############

skiplines = 6 # nb of lines in head (ncols, nrows etc.)
file1 = 'fichiers_entree/opendata2017reg_res001.asc'
file2 = 'fichiers_entree/opendata2016reg_res001.asc'
output_raster = 'opendata_reg_2017_moins_2016.asc'

# read one number from file, number are separated by spaces or newline
def read_num(fd):
    strbuf = ""
    while True:
        c = fd.read(1)
        if not c:
            return False
        if c == " " or c == '\n':
            return strbuf
        strbuf = strbuf + c

# redirect print output
sys.stdout = open(output_raster, 'w')

# open the 2 input files
with open(file1, 'r') as f1:
    with open(file2, 'r') as f2:
        # writes heading in output
        for i in range(skiplines):
            f1.readline()
            head = f2.readline()
            print (head.rstrip())
        # extract values from input
        while True:
            num1 = read_num(f1)
            num2 = read_num(f2)
            # calculate new value
            if (num1):
                val = int(num1) - int(num2)
                # write new value in output
                print (str(val) + " ", end = '')
            else:
                break




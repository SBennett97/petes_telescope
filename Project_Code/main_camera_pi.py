# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:54:03 2019

@author: sgb35
"""


from Project_routines import camera_routines_scope as CR
import time 
from time import sleep
import numpy as np
import os

print('Welcome to Jon and Seb\'s stargazing program. \n')



cwd = os.getcwd()
cwd_images = cwd + '\\Images'
cwd_flat_field = cwd + "\\Flat_Field"

for root, dirs, files in os.walk(cwd):
    # new subdir, so let's make a new...
    list_of_files = []
    for name in files:
        if name.endswith((".png")):
            list_of_files.append(name)  # you originally appended the list of all names!
    # once we're here, list_of_files has all the filenames in it,
    # so we can find the largest and print it
    largest = max(list_of_files)
    print ('Most recent image is - ' + largest)


def main():
    CR.Initialise()
    x = 1
    flatfield = raw_input('Are you doing a flat field calibration? - (Y/N)')
    if flatfield != 'N' or 'n':
        CR.flatfield(cwd_flat_field)
        x = 2
    while x < 2:
        loop = raw_input('If you want to quit, press \'q\'. \nIf you want to take an image, press any key - ')
        if loop == 'q':
            x = 2
        else:
            fp = raw_input('Please provide a filepath to save the image to, if you do not have a filepath, please press \'n\' - ')
            
            if fp == 'n':
                print('Using default file path.\n')
                timestr = time.strftime("%Y%m%d-%H%M%S")
                filename = cwd_images + '\\' + timestr + '.png'
                CR.image_with_arguments(filename)

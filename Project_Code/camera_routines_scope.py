# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:52:46 2018
@author: sgb35
"""
from io import BytesIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
from time import sleep
import numpy as np
##from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from skimage.feature import register_translation
from math import sqrt
from time import sleep
from fractions import Fraction
##import matplotlib.pyplot as plt


camera = PiCamera()
camera.start_preview()
sleep(10)
camera.stop_preview()
CAMERA_RESOLUTION = (3280,2464)
CAMERA_FRAMERATE = 30



def image_with_arguments(filepath, array = False, camera=camera):
    '''
    Function to capture custom image to file and variable
    
    Input : filepath - string
            path where image is to be stored
            
            array - Boolean 
            default = True
            
    Returns: if array = True then returns rgb array of image
    '''
    try:
        camera=PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("Camera already running")
    with camera:
        if raw_input('Long exposure image? - (Y/N) ') != 'N' or 'n':
            camera.resolution=CAMERA_RESOLUTION
            camera.framerate=Fraction(1, 6)
            camera.sensor_mode=3
            camera.shutter_speed = 6000000
            camera.iso = 800
            # Give the camera a good long time to set gains and
            # measure AWB (you may wish to use fixed AWB instead)
            sleep(30)
            camera.exposure_mode = 'off'
        else:
            camera.resolution = CAMERA_RESOLUTION
            camera.framerate = raw_input('Framerate - ')
            camera.shutter_speed = raw_input('Shutter speed - ')
            camera.iso = raw_input('ISO - ')
            sleep(15)
        camera.capture(filepath)
        if array:
            output = np.empty((768*1024*3), dtype = np.uint8)
            camera.capture(output,'rgb')
            output = output.reshape((768,1024,3))
            return output        

        

  
def start_display(position_size=(100,100,256,192), camera=camera):
    try:
        camera=PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("Camera already running")
    #Allows the user to define the size of the preview window and its location on the screen 'x,y,w,h'
    camera.start_preview(fullscreen = False, window = position_size)

def stop_display(camera=camera):
    try:
        camera=PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("Camera already running")
    camera.stop_preview()
    

def initialise(camera=camera):
    i = 1
    print("Initialising and warming up")
    try:
        camera=PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("Camera already running")
    
    with camera:
        while i < 205:
            camera.resolution=CAMERA_RESOLUTION
            camera.framerate=CAMERA_FRAMERATE
            camera.shutter_speed = 500000
            camera.iso = 200
            sleep(1)
            print("Taking image {}\n".format(i))
            i += 1
            output = np.empty((3280*2464*3), dtype = np.uint8)
            camera.capture(output,'rgb')
    print('Camera is warmed up')
    
def flat_field(camera=camera, filepath_stem):
    print("Taking flat field images\n")
    try:
        camera=PiCamera()
    except picamera.exc.PiCameraMMALError:
        print("Camera already running")
    for iso in range(100, 800, 100):
        for speed in range(10, 6000000, 599999):
            camera.resolution = CAMERA_RESOLUTION
            camera.iso = iso
            camera.framerate = speed
            sleep(1)
            file_name = "\\" + "ISO_" + str(iso) + "_FR_" + str(speed) + ".png"
            filepath = filepath_stem + file_name
            camera.capture(filepath)
            print("Image - {} done\n".format(file_name))

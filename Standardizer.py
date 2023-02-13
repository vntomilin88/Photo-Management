# -*- coding: utf-8 -*-
"""
Created on 2022.02.12

@author: vntom

This program standardizes all the photos in a given folder by renaming them all in the similar fashion as well as
convert to a JPG format.
"""
import os
import datetime
from PIL import Image

chaosf = '/home/vntom/Purgatory/Chaos/' #Starting folder where all the photos are contained
orderf = '/home/vntom/Purgatory/Order/' #Final folder where all the standardized photos will be placed

for file in os.listdir(f'{chaosf}'):
    RAW = Image.open(f'{chaosf}{file}')
    RAW_exif = RAW.getexif()
    if RAW_exif[272].strip() == 'Canon EOS 40D': #check the camera name
        tdelta = -3600*5 #depending on the camera we have different time deltas
        photosource = '_EC' #in order to avoid any exact matches in name between different cameras we add a tag in the end
    DT = RAW_exif[306] #306 - exif information when the photo was taken, make it into the standardized format
    originaltime = datetime.datetime(int(DT[:4]), int(DT[5:7]), int(DT[8:10]), int(DT[11:13]), int(DT[14:16]), int(DT[17:19]), 00)
    correctedtime = originaltime+datetime.timedelta(seconds=tdelta)
    imgtimename = correctedtime.strftime('%Y%m%d_%H%M%S')
    JPG = RAW.convert('RGB')
    JPG.save(f'{orderf}{imgtimename}{photosource}.jpg', 'JPEG', quality=97, exif=RAW_exif) #  

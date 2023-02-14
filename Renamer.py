# -*- coding: utf-8 -*-
"""
Created on 2022.02.12

@author: vntom

This program takes exif date when the photo was taken (can add or substract time if 
needed)and renames the file in a format: YYYYMMDD_HHMMSS.

Instead of using bulky PIL module, this program uses piexif to get the data and camera
information

exif_dict['0th'][306] - data taken
exif_dict['0th'][272] - Camera model
"""
import os
import piexif
import datetime

chaosf = '/home/vntom/Purgatory/Chaos/' #Starting folder where all the photos are contained
orderf = '/home/vntom/Purgatory/Order/' #Final folder where all the standardized photos will be placed

for file in sorted(os.listdir(f'{chaosf}')):
    extension = os.path.splitext(file)[1] #get the file extension
    img_exif = piexif.load(f'{chaosf}{file}')['0th'] #load image exifc
    # img_exif = piexif.load(f'{chaosf}{file}')['Exif'] #load image exifc
    if img_exif[272].decode() == 'Canon EOS 40D': #check the camera name
        tdelta = -3600*5+60*5+10 #depending on the camera we have different time deltas
        photosource = '_EP' #in order to avoid any exact matches in name between different cameras we add a tag in the end
    DT = img_exif[306] #[0th]306 - exif information when the photo was taken, [Exif]36867 - original time taken
    originaltime = datetime.datetime(int(DT[:4]), int(DT[5:7]), int(DT[8:10]), int(DT[11:13]), int(DT[14:16]), int(DT[17:19]), 00)
    correctedtime = originaltime+datetime.timedelta(seconds=tdelta)
    imgtimename = correctedtime.strftime('%Y%m%d_%H%M%S')
    os.system(f'cp {chaosf}{file} {orderf}{imgtimename}{photosource}{extension}') 
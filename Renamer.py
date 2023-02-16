# -*- coding: utf-8 -*-
"""
Created on 2022.02.12

@author: vntom

This program takes exif date when the photo was taken (can add or substract time if 
needed)and renames the file in a format: YYYYMMDD_HHMMSS.

I created it in order to synchronize naming for multiple photograps from cameras and 
phones, that usualy are set in different times

It takes photos taken on different devices around the same time, calculates the 
difference time wise, the name of the camera, and then relates this information to the
program.

Instead of using bulky PIL module, this program uses piexif to get the data and camera
information

exif_dict['0th'][306] - data taken
exif_dict['0th'][272] - Camera model
exif_dict['Exif'][36867] - original time taken
https://www.exiv2.org/tags.html - for more information on exif tags

Notes:
datetime.datetime.fromtimestamp(os.stat(f'{chaosf}{file}').st_mtime) #get the last modified date
"""

import os
import ffmpeg
import piexif
import datetime


chaosf = '/home/vntom/Purgatory/Chaos/' #Starting folder where all the photos are contained
# chaosf = '/Terra/Oblachko/Pictures/2016/Nevada-California Trip 2016/2016.11.26/' 
orderf = '/home/vntom/Purgatory/Order/' #Final folder where all the standardized photos will be placed
appendixf = '/home/vntom/Purgatory/Appendix/'

camera_set = set()

def datetime_converter(file):
    DT = piexif.load(f'{chaosf}{file}')['0th'][306] #[0th]306 - exif information when the photo was taken, [Exif]36867 - original time taken
    DTF = datetime.datetime(int(DT[:4]), int(DT[5:7]), int(DT[8:10]), int(DT[11:13]), int(DT[14:16]), int(DT[17:19]), 00)
    return(DTF)

def determinator():
    #Determining all the camera models
    for file in sorted(os.listdir(f'{chaosf}')):
        extension = os.path.splitext(file)[1].lower() #get the file extension
        if extension in ['.jpeg', '.jpg', '.cr2']:
            camera_set.add(piexif.load(f'{chaosf}{file}')['0th'][272].decode().rstrip('\x00'))
    
    #determining the time differential, correct_sample is the file from your camera which is the
    #date you center the rest of the photos from, wrong_sample is the media that is taken at
    #approximately the same time, tdelta calculated this way needs further adjustment due to
    #calendar year differences
    
    cor_time = datetime_converter('20150214_120552.jpg') #image with the right time
    wrong_time = datetime_converter('GOPR0059.JPG') #image with distorted time
    tdelta = (cor_time - wrong_time).total_seconds()
    
    print(camera_set)
    print(tdelta)
    print(407*24*3600+3600*14+5*60+14)

# determinator()

#Once you know the camera names create a dictionary containing name of the camera as key
#and list of time differential to be corrected and the suffix you want added to the photos and videos
#from that source in the following  format: {'CameraModel':[CameraName, tdelta, suffix, video_file_header_symbols]}
#time differential (tdelta) should be determined from taking two photos taken around the same
#time and substracting the values of time taken
CameraDict = {'HERO4 Black': ['EgorsGoPro', 407*24*3600+3600*14+5*60+14, '_EG'], \
              'Lumia 1020':  ['EgorsPhone', 0, '_EP']}

#Had to make a second dictionary since video files do not record the camera on which it was recorded
#This dictionary uses the 1st letter of the video file to recognize the camera, since the cameras
#that are weird, do not name videos in a date format.
VideoDict = {'G': ['EgorGoProVideo', 407*24*3600+3600*14+5*60+14, '_EG'], \
             'W': ['EgorPhoneVideo', 0, '_EP']}

def photo_renamer(file, extension):
    img_exif = piexif.load(f'{chaosf}{file}')['0th'] #load image exif
    camera_model = img_exif[272].decode().strip().rstrip('\x00')
    
    if camera_model in CameraDict.keys():
        camera_values = CameraDict[camera_model]
        try:
            DT = img_exif[306]
        except:
            DT = piexif.load(f'{chaosf}{file}')['Exif'][36867]
        originaltime = datetime.datetime(int(DT[:4]), int(DT[5:7]), int(DT[8:10]), int(DT[11:13]), int(DT[14:16]), int(DT[17:19]), 00)
        correctedtime = originaltime+datetime.timedelta(seconds=camera_values[1])
        imgtimename = correctedtime.strftime('%Y%m%d_%H%M%S')
        os.system(f'cp {chaosf}{file} {orderf}{imgtimename}{camera_values[2]}{extension}')
    else:
        os.system(f'cp {chaosf}{file} {orderf}{file}')

def video_renamer(file, extension):
    if file[0] in VideoDict.keys():
        video_values = VideoDict[file[0]]
        VT = ffmpeg.probe(f'{chaosf}{file}')['streams'][0]['tags']['creation_time']
        originaltime = datetime.datetime(int(VT[:4]), int(VT[5:7]), int(VT[8:10]), int(VT[11:13]), int(VT[14:16]), int(VT[17:19]), 00)
        correctedtime = originaltime+datetime.timedelta(seconds=video_values[1])
        vidtimename = correctedtime.strftime('%Y%m%d_%H%M%S')
        os.system(f'cp {chaosf}{file} {orderf}{vidtimename}{video_values[2]}{extension}')
    else:
        os.system(f'cp {chaosf}{file} {orderf}{file}')

def main():
    for file in os.listdir(f'{chaosf}'): #at this stage we complete renaming
        extension = os.path.splitext(file)[1].lower() #get the file extension
        if extension in ['.mp4', '.mov']:
            video_renamer(file, extension)
        elif extension in ['.jpeg', '.jpg', '.cr2', '.tiff']:
            print(file)
            photo_renamer(file, extension)
        else:
            os.system(f'cp {chaosf}{file} {appendixf}{file}')

# main()



# Photo-Management
If you ever travel with other people, you often accumulate photographs from different cameras and phones, when all the files are dumped into one folder it is a mess, since every camera and phone have their own naming conventions.

This program helps deal with that problem. Using it will allow you to rename all the photos from different sources into a format of YYYYMMDD_HHMMSS. It takes the exif information from the photos and ffmpeg info from the videos and uses it for renaming.
Often cameras do not have the correct time settings setup, this program also deal with that. You can calculate the time difference between two photos taken at approximately the same time using the determinator function, then simply provide the time differential to the tdelta variable and the program will add or substract the needed time, to make the flow of photos in the folder chronological no matter the source from whence they came :)
Once you know the

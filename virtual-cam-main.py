#!/usr/bin/env python3
import cv2
import cvzone
import pyfakewebcam
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import glob
import subprocess

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
segmenter = SelfiSegmentation()
fpsReader = cvzone.FPS()
# imageBg = cv2.imread('images/1.jpg')

subprocess.run(["sudo", "-S", "modprobe", "v4l2loopback", "devices=2"])
imageList = []
imageDirList = os.listdir('images')
for img in imageDirList:
    readImg = cv2.imread(f'images/{img}')
    imageList.append(readImg)
imageIndex = 0
cameraPathList = []
for camera in glob.glob('/dev/video?'):
    cameraPathList.append(camera)
print(len(cameraPathList) - 1)
cameraPath = cameraPathList[-(len(cameraPathList) - 1)]
h, w = 480, 640
if cameraPathList is []: print('No camera found!!!')
stream_camera = pyfakewebcam.FakeWebcam(
    '{cameraPath}'.format(cameraPath=cameraPath), w, h
)

while True:
    _, image = cap.read()
    imgOut = segmenter.removeBG(image, imageList[imageIndex], threshold=0.75)

    _, bgChangeImage = fpsReader.update(imgOut, color=(0, 0, 255))
    # imageStack = cvzone.stackImages([image, imgOut], 2, 1)
    # cv2.imshow('image', image)
    # print('index-->', imageIndex)
    key = cv2.waitKey(1)
    if key == ord('a'):
        if imageIndex > 0:
            imageIndex -= 1
    elif key == ord('d'):
        if imageIndex < len(imageList) - 1:
            imageIndex += 1
    elif key == ord('q'):
        break
    stream_camera.schedule_frame(bgChangeImage[..., ::-1])

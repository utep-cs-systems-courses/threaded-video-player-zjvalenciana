#!/usr/bin/env python3

import cv2
import os
import time
import numpy as np
from threading import Thread
from QueueE import QueueE


clipFileName = "clip.mp4"
capacity = 10

readFramesQueue = QueueE(capacity)
grayFramesQueue = QueueE(capacity)

def extractFrames(clipFileName, readFramesQueue):
    vidcap = cv2.VideoCapture(clipFileName)
    count = 0
    # read one frame
    success,image = vidcap.read()
    print(f'Reading frame {count} {success}')
    while success and count < 72:
        # write the current frame out as a jpeg image
        #Transform into a jpg image
        success, jpgImage = cv2.imencode('.jpg', image)
        readFramesQueue.enqueue(jpgImage)
        success,image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1
    readFramesQueue.enqueue(None)


def convertToGrayScale(readFramesQueue, grayFramesQueue):
    # initialize frame count
    count = 0

    # get the next frame file name
    inputFrame = readFramesQueue.dequeue()

    while inputFrame is not None and count < 72:
        print(f'Converting frame {count}')

        inputFrame = np.asarray(bytearray(inputFrame), dtype = np.uint8)
        image = cv2.imdecode(inputFrame, cv2.IMREAD_UNCHANGED)
        
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)
        
        #change it to enqueue into the grayFramesQueue
        grayFramesQueue.enqueue(jpgImage)
        count += 1

        # generate input file name for the next frame
        #TODO change it to dequeue from readFramesQueue

        inputFrame = readFramesQueue.dequeue() ###
    grayFramesQueue.enqueue(None)

def displayFrames(grayFramesQueue):
    # initialize frame count
    count = 0



    # Generate the filename for the first frame
    #TODO change to read/dequeue from the grayFramesBuffer
    
    # load the frame
    frame = grayFramesQueue.dequeue() ###

    while frame is not None:
        print(f'Displaying frame {count}')

        # convert the raw frame to a numpy array
        frame = np.asarray(bytearray(frame), dtype = np.uint8)
        # get a jpg encoded frame
        image = cv2.imdecode(frame, cv2.IMREAD_UNCHANGED)
        
        # Display the frame in a window called "Video"
        cv2.imshow('Video', image)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        # get the next frame filename
        count += 1

        #TODO dequeue from grayFramesBuffer the next frame
        # Read the next frame file
        frame = grayFramesQueue.dequeue()

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()


extractThread = Thread(target = extractFrames, args = (clipFileName, readFramesQueue)).start()
greyFramesThread = Thread(target = convertToGrayScale, args = (readFramesQueue, grayFramesQueue)).start()
displayThread = Thread(target = displayFrames, args = (grayFramesQueue,)).start()
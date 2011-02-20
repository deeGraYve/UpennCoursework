import sys

import sys, getopt
from os.path import dirname, join
from pycv import tprint
from pycv.interfaces.opencv import *
from pycv.cs.cv import *
from time import time
from opencv import highgui

if __name__ == '__main__':

    print "OpenCV Python wrapper test"
   # print "OpenCV version: %s (%d, %d, %d)" % (cv.CV_VERSION,cv.CV_MAJOR_VERSION,cv.CV_MINOR_VERSION,cv.CV_SUBMINOR_VERSION)

    cvNamedWindow ('Camera', CV_WINDOW_AUTOSIZE)

    cvMoveWindow ('Camera', 10, 40)

    try:
        # try to get the device number from the command line
        device = int (sys.argv [1])

        # got it ! so remove it from the arguments
        del sys.argv [1]
    except (IndexError, ValueError):
        # no device number on the command line, assume we want the 1st device
        device = 0

    if len (sys.argv) == 1:
        # no argument on the command line, try to use the camera
        capture = cvCreateCameraCapture (device)

        # set the wanted image size from the camera
        cvSetCaptureProperty (capture, CV_CAP_PROP_FRAME_WIDTH, 320)
        cvSetCaptureProperty (capture, CV_CAP_PROP_FRAME_HEIGHT,240)
    else:
        # we have an argument on the command line,
        # we can assume this is a file name, so open it
        capture = cvCreateFileCapture (sys.argv [1]) 

    # check that capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit (1)

    # capture the 1st frame to get some propertie on it
    frame = cvQueryFrame (capture)

    # get some properties of the frame
    frame_size = cvGetSize (frame)

    # compute which selection of the frame we want to monitor
    od = ObjectDetector('frontal_face', 4, join(datapath,'face-detection-cascade-fastest.txt'))
    #od = ObjectDetector('frontal_face', 0)
    print frame_size
    img2 = cvCreateImage(frame_size, IPL_DEPTH_8U, 3)
    stime = time()
    i = 1
    
    while 1:
        # do forever
        i += 1
        # 1. capture the current image
        frame = cvQueryFrame (capture)
        if frame is None:
            # no image captured... end the processing
            break
        if frame[0].origin == 1: # windows based, need to flip
            cv.cvFlip(frame, img2)
            img3 = img2
        else:
            img3 = frame
        z = od.detect(img3, scale_factor=1.8, min_neighbors=1, group_overlapping=True)
        #z = od.detect(frame, scale_factor=2.2, min_neighbors=1)
        for x in z:
            cvRectangle(img3, CvPoint(x[0], x[1]), CvPoint(x[0]+x[2],x[1]+x[3]), CV_RGB(0,255,0), 2)
        cvShowImage('Camera', img3)

        # mirror the captured image
        #cv.cvFlip (frame, None, 1)

        #highgui.cvShowImage ('Camera', frame)

        # handle events
        k = highgui.cvWaitKey (10)

        if k == '\x1b':
            # user has press the ESC key, so exit
            break
    stime = time()-stime    
    print "Total time = ", stime
    print "Number of frames = ", (i+1)
    print "Fps = ", (i+1)/stime
        
    cvReleaseImage(img2)
    cvReleaseCapture(capture)
    cvDestroyAllWindows()

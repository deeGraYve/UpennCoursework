#!/usr/bin/env python

import sys, getopt
from os.path import dirname, join
from pycv import tprint
from pycv.interfaces.opencv import *
from pycv.cs.cv import *
from time import time

def demo2(delay=1):
    print "======================================================================"
    print "What about detecting from a video?"
    
    print "Here's an example video. Let's play about 500 frames..."
    print "At any time, press ESC to skip the video..."
    filename = join(dirname(__file__), 'webcam.avi')
    
    cap = cvCreateFileCapture(filename)
    if not cap or not cap.contents:
        print "Error, the example video file not found or cannot be opened (may be the problem of codecs)."
        return
        
    cvNamedWindow('video', CV_WINDOW_AUTOSIZE)
    for i in xrange(500):
        img = cvQueryFrame(cap)
        cvShowImage('video', img)
        if cvWaitKey(33) == 27:
            break

    cvDestroyAllWindows()


    print "\n\nLet's detect faces using OpenCV"
    print "At any time, press ESC to skip the video..."
    filename = join(dirname(__file__), 'webcam.avi')
    
    od = ObjectDetector('frontal_face', 0)
    
    # go back to the beginning
    cvSetCaptureProperty(cap, CV_CAP_PROP_POS_AVI_RATIO, 0)
    
    stime = time()
        
    cvNamedWindow('opencv', CV_WINDOW_AUTOSIZE)
    for i in xrange(500):
        img = cvQueryFrame(cap)
        z = od.detect(img, scale_factor=1.2, min_neighbors=1)
        for x in z:
            cvRectangle(img, CvPoint(x[0], x[1]), CvPoint(x[0]+x[2],x[1]+x[3]), CV_RGB(0,255,0), 2)
        cvShowImage('opencv', img)
        if cvWaitKey(delay) == 27:
            break
            
    stime = time()-stime    
    print "Total time = ", stime
    print "Number of frames = ", (i+1)
    print "Fps = ", (i+1)/stime
    
            
    cvDestroyAllWindows()



    print "\n\nLet's detect faces using our method."
    print "Note that ours does not detect faces as varied as theirs."
    print "But our detection is FASTER and MORE ACCURATE...\n"
    print "At any time, press ESC to skip the video..."
    filename = join(dirname(__file__), 'webcam.avi')
    
    od = ObjectDetector('frontal_face', 4, join(datapath,'face-detection-cascade-fastest.txt'))
    #print join(datapath,'face-detection-cascade-fastest.txt')
    
    # go back to the beginning
    cvSetCaptureProperty(cap, CV_CAP_PROP_POS_AVI_RATIO, 0)
    
    img = cvQueryFrame(cap)
    img2 = cvCreateImage(cvGetSize(img), IPL_DEPTH_8U, 3)
    
    stime = time()
        
    cvNamedWindow('ours', CV_WINDOW_AUTOSIZE)
    for i in xrange(1000):
        img = cvQueryFrame(cap)
        if img[0].origin == 1: # windows based, need to flip
            cvFlip(img, img2)
            img3 = img2
        else:
            img3 = img
        z = od.detect(img3, scale_factor=1.2, min_neighbors=1, group_overlapping=True)
        for x in z:
            cvRectangle(img3, CvPoint(x[0], x[1]), CvPoint(x[0]+x[2],x[1]+x[3]), CV_RGB(0,255,0), 2)
        cvShowImage('ours', img3)
        if cvWaitKey(delay) == 27:
            break

    stime = time()-stime    
    print "Total time = ", stime
    print "Number of frames = ", (i+1)
    print "Fps = ", (i+1)/stime
    
    cvReleaseImage(img2)
    cvReleaseCapture(cap)
    cvDestroyAllWindows()

def demo(delay=1):
    cvStartWindowThread()
    #demo1()
    demo2(delay=delay)

    print "\n\nThat's it. More demos are coming soon."
    print "Bye bye for now..."
    
if __name__ == '__main__':
    # check command-line flags
    delay = 1  # delay between frames
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:", ["delay_between_frames="])
        for opt, arg in opts:
            if opt in ("-d", "--delay_between_frames") and int(arg) >= 1:
                delay = int(arg)
    except:
        print 'Invalid delay. Delay of 1 is used instead.'
    demo(delay=delay)

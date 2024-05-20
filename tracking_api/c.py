#!/usr/bin/python

#-*- encoding:utf-8 -*-
import tornado.web
import tornado.ioloop
from tornado.ioloop import IOLoop, PeriodicCallback
import tornado.process
import tornado.template
import tornado.httpserver
import json
import sys
import os,time
import subprocess
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import urllib2
api_port=5001
count=0
count1=0
count2=0
count3=0
count4=0
count5=0
count6=0
count7=0
count8=0
count9=0
import numpy as np

def start_tracking(x,y,w,h):

# construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str,
        help="path to input video file")
    ap.add_argument("-t", "--tracker", type=str, default="csrt",
        help="OpenCV object tracker type")
    args = vars(ap.parse_args())

    # extract the OpenCV version info
    (major, minor) = cv2.__version__.split(".")[:2]

    # if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
    # function to create our object tracker
    if int(major) == 3 and int(minor) < 3:
        tracker = cv2.Tracker_create(args["tracker"].upper())

    # otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
    # approrpiate object tracker constructor:
    else:
        # initialize a dictionary that maps strings to their corresponding
        # OpenCV object tracker implementations
        OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
        }

        # grab the appropriate object tracker using our dictionary of
        # OpenCV object tracker objects
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

    # initialize the bounding box coordinates of the object we are going
    # to track
    initBB = None

    # if a video path was not supplied, grab the reference to the web cam
    if not args.get("video", False):
        print("[INFO] starting video stream...")
        vs = VideoStream(src="rtsp://admin:admin@123@192.168.1.107:554/cam/realmonitor?channel=1?subtype=0").start()
        time.sleep(1.0)

    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])

    # initialize the FPS throughput estimator
    fps = None
    # loop over frames from the video stream
    while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        frame = vs.read()
        frame = frame[1] if args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
            break

        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        # frame = imutils.resize(frame, width=1024,height=800)
        (H, W) = frame.shape[:2]


        # check to see if we are currently tracking an object
        if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)

            # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                    (0, 255, 0), 2)
                cv2.circle(frame,(x+w/2,y+h/2),radius=0,color=(0,255,0),thickness=5)
                #print(x)
                #print(y)
                fps.update()
                fps.stop()
                dz = w+50
                #print("deadzone",dz)
                fw = W
                fh = H
                fwc = fw / 2
                fhc = fh / 2
                global count9
                count9=0
                
                if(x+w/2< fwc-dz  ):
                    global count
                    global count1
                    global count2
                    global count3
                    global count4
                    global count7
                    global count6
                    global count5
                    global count8
                    #print("left")
                    count1=0
                    count2=0
                    count3=0
                    count+=1
                    count4=0
                    count5=0
                    count6=0
                    count7=0
                    count8=0


                    if(count<=1):
                        print("left")
                        
                        url='http://localhost:4001/leftc'+'?p_speed='+str(5)+'&t_speed='+str(5)
                        response = urllib2.urlopen(url)
                elif(x+w/2> fwc+dz  ) :
                    global count
                    global count1
                    global count2
                    global count3
                    global count4
                    global count7
                    global count6
                    global count5
                    global count8
                    #print("right")
                    count=0
                    count1+=1
                    count2=0
                    count3=0
                    count4=0
                    count5=0
                    count6=0
                    count7=0
                    count8=0
                    if(count1<=1):
                        print("right")
                        
                        url='http://localhost:4001/rightc'+'?p_speed='+str(5)+'&t_speed='+str(5)
                        response = urllib2.urlopen(url)
                
                elif fwc-dz<x+w/2<fwc+dz :
                    global count
                    global count1
                    global count2
                    global count3
                    global count4
                    global count7
                    global count6
                    global count5
                    global count8
                    count=0
                    count1=0
                    count2=0
                    count3=0
                    count4+=1
                    count5=0
                    count6=0
                    count7=0
                    count8=0
                    if count4<=1:
                        print("stop")
                        url='http://localhost:4001/stop'
                        response = urllib2.urlopen(url)
                
            if not success:
                count9+=1
                if count9<=1:

                    print("object disappear")
                    url='http://localhost:4001/stop'
                    response = urllib2.urlopen(url)
            # update the FPS counter


            # initialize the set of information we'll be displaying on
            # the frame
            info = [
                ("Tracker", args["tracker"]),
                ("Success", "Yes" if success else "No"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]

            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # show the output frame
        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if(x):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = (x,y,w,h)
            # print(initBB) 
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            tracker.init(frame, initBB)
            fps = FPS().start()

        # if the `q` key was pressed, break from the loop
        elif key == ord("q"):
            break

    # if we are using a webcam, release the pointer
    if not args.get("video", False):
        vs.stop()

    # otherwise, release the file pointer
    else:
        vs.release()

    # close all windows
    cv2.destroyAllWindows()

class tracking(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
class trackingstart(tornado.web.RequestHandler):
    def get(self):

        #global frame
        print("tracking start")
        try:
            x = int(self.get_argument("x_hor")) 
            y = int(self.get_argument("y_hor"))
            w = int(self.get_argument("width"))
            h = int(self.get_argument("height"))
        except:
            print("cordin")

        start_tracking(x,y,w,h)
        # pantilt(b'\xFF\x01\x00\x51\x00\x00\x52')
        self.write({'items': 'tracking start'})

def make_app():
    return tornado.web.Application([("/", tracking),("/track", trackingstart)],template_path=os.path.join(os.path.dirname(__file__), "templates"))

if __name__ == '__main__':
    app = make_app()
    app.listen(api_port)
    print("tracking is listening for commands on port: "+str(api_port))
    IOLoop.instance().start()

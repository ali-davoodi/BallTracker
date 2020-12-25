# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import pandas as pd
import matplotlib.pyplot as plt

import serial

#Global Variables
ser=0
EOP=0XE7
servoY=90
servoX=80
integralX=0
integralY=0

deltaAngleX=90
deltaAngleY=0
calibratedFlag=0
h=60

def updateServos(servo1,servo2):
    if(servo1>180):
        servo1=180
    elif (servo1<0):
        servo1=0

    if(servo2>180):
        servo2=180
    elif (servo2<0):
        servo2=0
        
    ser.write([servo1])
    ser.write([servo2])
    ser.write([EOP])

#Function to Initialize the Serial Port
def init_serial():
    COMNUM = 9          #Enter Your COM Port Number Here.
    global ser          #Must be declared in Each Function
    ser = serial.Serial('COM5')
    ser.baudrate = 115200#38400#9600
    #ser.port = COMNUM - 1   #COM Port Name Start from 0
    
    #ser.port = '/dev/ttyUSB0' #If Using Linux

    #Specify the TimeOut in seconds, so that SerialPort
    #Doesn't hangs
    ser.timeout = 10
    if ser.isOpen()!=1:
        ser.open()          #Opens SerialPort

    # print port open or closed
    if ser.isOpen():
        print('Open: ' + ser.portstr)
#Function Ends Here


init_serial()
updateServos(servoY,servoX)
updateServos(servoY,servoX)
updateServos(servoY,servoX)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(1)
    cam_height=camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cam_width=camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(cam_height)
    print(cam_width)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

#Creating a Pandas DataFrame To Store Data Point
Data_Features = ['x', 'y', 'time']
Data_Points = pd.DataFrame(data = None, columns = Data_Features , dtype = float)


#Reading the time in the begining of the video.
start = time.time()

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    #Reading The Current Time
    current_time = time.time() - start

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=1800)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        

        # only proceed if the radius meets a minimum size
        if (radius < 300) & (radius > 10 ) : 
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            tmp='Xc:'+str(int(x))+'   Yc:'+str(int(y))+'    (pixel)'
            cv2.putText(frame,tmp,(50,50),cv2.FONT_HERSHEY_COMPLEX,
                                    1,(0,255,0),2, cv2.LINE_AA)
            #Save The Data Points
            Data_Points.loc[Data_Points.size/3] = [x , y, current_time]

##            if x>cam_width/2 :
##                servoX+=1
##            elif x<cam_width/2:
##                servoX-=1

##            errorX=cam_width/2-x;
##            servoX=int(-errorX/25+90)

            errorX=(cam_width/2-x);
            integralX+=errorX
            servoX=int(errorX/40+integralX/100+90)
            
##            print('errorY='+str(errorY))
##            print('integralY='+str(integralY))
            print('servoX='+str(servoX))

            errorY=-(cam_height/2-y);
            integralY+=errorY
            servoY=int(errorY/40+integralY/100+90)

            if calibratedFlag==1:
                beta=90-(servoY-deltaAngleY)
                d=h*np.tan(np.deg2rad(beta))
                alpha=-(servoX-deltaAngleX)
                xt=d*np.cos(np.deg2rad(alpha))
                yt=d*np.sin(np.deg2rad(alpha))
##                print('beta= '+str(alpha))
                #print('Xt= '+str(xt)+'Yt= '+str(yt))
                tmp='Xt:'+str(int(xt))+'   Yt:'+str(int(yt))+'    (cm)'
                cv2.putText(frame,tmp,(50,100),cv2.FONT_HERSHEY_COMPLEX,
                                    1,(0,255,0),2, cv2.LINE_AA)
                

            
            
##            print('errorY='+str(errorY))
##            print('integralY='+str(integralY))
            print('servoY='+str(servoY))
            
            updateServos(servoX,servoY)
##            if x-cam_width>10 :
##                servoX-=1
##            elif (x-cam_width<-10):
##                servoX+=1
                
##            if (y-cam_height>10):
##                servoY-=1
##            elif (y-cam_height<-10):
##                servoY+=1

                
        
##  # update the points queue
##  pts.appendleft(center)
##
##  # loop over the set of tracked points
##  for i in range(1, len(pts)):
##      # if either of the tracked points are None, ignore
##      # them
##      if pts[i - 1] is None or pts[i] is None:
##          continue
##
##      # otherwise, compute the thickness of the line and
##      # draw the connecting lines
##      thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
##      cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    elif key==ord("c"):
        deltaAngleX=servoX
        deltaAngleY=servoY
        calibratedFlag=1
        print('Calibrated...')

#'h' is the focal length of the camera
#'X0' is the correction term of shifting of x-axis
#'Y0' is the correction term ofshifting of y-axis
#'time0' is the correction term for correction of starting of time
h = 0.2
X0 = -3
Y0 = 20
time0 = 0
theta0 = 0.3

#Applying the correction terms to obtain actual experimental data
Data_Points['x'] = Data_Points['x']- X0
Data_Points['y'] = Data_Points['y'] - Y0
Data_Points['time'] = Data_Points['time'] - time0

#Calulataion of theta value
Data_Points['theta'] = 2 * np.arctan(Data_Points['y']*0.0000762/h)#the factor correspons to pixel length in real life
Data_Points['theta'] = Data_Points['theta'] - theta0

#Creating the 'Theta' vs 'Time' plot
plt.plot(Data_Points['theta'], Data_Points['time'])
plt.xlabel('Theta')
plt.ylabel('Time')

#Export The Data Points As cvs File and plot
Data_Points.to_csv('Data_Set.csv', sep=",")
plt.savefig('Time_vs_Theta_Graph.svg', transparent= True)

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

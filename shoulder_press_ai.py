#Program is designed to count the amount of reps a shoulder press is done using OpenCV modules
    #need to install modules opencv, cvzone, mediapipe
import cv2
import numpy as np
import math
from cvzone.PoseModule import PoseDetector
import time

#Our VideoCapture to count the amount of reps using computer cam (INITIALIZATION)
#Detections of Human Beings Along with Point Parameters
#Can take in live footage or clip, depends on input
cap = cv2.VideoCapture('C:\\Users\\chris\\OneDrive\\Documents\\Python Learning\\shoulder_press_trainer\\videotest.mp4')
pd = PoseDetector(detectionCon=0.7, trackCon=0.7) #detect and track Confidence of that this is a human

#Class to find the Critical Points of our Shoulder Press and Angles
class angleFinder:
    #Declarations
    def __init__ (self, lmlist, p1, p2, p3, p4, p5, p6, drawPoints): 
        self.lmlist = lmlist
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.p6 = p6
        self.drawPoints = drawPoints
    #Finding Angles
    def angle(self):
        if self.lmlist != 0: #Making sure we are detecting Human body
            point1 = self.lmlist[self.p1]
            point2 = self.lmlist[self.p2]
            point3 = self.lmlist[self.p3]
            point4 = self.lmlist[self.p4]
            point5 = self.lmlist[self.p5]
            point6 = self.lmlist[self.p6]

            #Initializing critial point values, it looks for only 3 values, middle value is the angle point
            x1, y1 = point1[1:-1]
            x2, y2 = point2[1:-1]
            x3, y3 = point3[1:-1]
            x4, y4 = point4[1:-1]
            x5, y5 = point5[1:-1]
            x6, y6 = point6[1:-1]

            #Math Time to calculate angles for rep counter
            leftAngle = math.degrees(math.atan2(y3-y2, x3-x2) - 
                                     math.atan2(y1-y2, x1-x2))
            
            rightAngle = math.degrees(math.atan2(y6-y5, x6-x5) - 
                                     math.atan2(y4-y5, x4-x5))
            
            #Range of Angles
            #When shoulders and elbows are raised at good threshold, numbers become 100
                # - When 100, that's the source of our rep counter
            leftAngle = int(np.interp(leftAngle, [-170, 180], [100, 0]))
            rightAngle = int(np.interp(rightAngle, [-50, 20], [100, 0]))

            #If Detect Points, draw criticals circles
            if self.drawPoints == True:
                cv2.circle(img, (x1, y1), 10, (0, 255, 255), 5)
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), 6) 

                cv2.circle(img, (x2, y2), 10, (0, 255, 255), 5)
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), 6)

                cv2.circle(img, (x3, y3), 10, (0, 255, 255), 5)
                cv2.circle(img, (x3, y3), 15, (0, 255, 0), 6)

                cv2.circle(img, (x4, y4), 10, (0, 255, 255), 5)
                cv2.circle(img, (x4, y4), 15, (0, 255, 0), 6)

                cv2.circle(img, (x5, y5), 10, (0, 255, 255), 5)
                cv2.circle(img, (x5, y5), 15, (0, 255, 0), 6)

                cv2.circle(img, (x6, y6), 10, (0, 255, 255), 5)
                cv2.circle(img, (x6, y6), 15, (0, 255, 0), 6)

                #Connecting points by red lines
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
                cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 4)
                cv2.line(img, (x4, y4), (x5, y5), (0, 0, 255), 4)
                cv2.line(img, (x5, y5), (x6, y6), (0, 0, 255), 4)
                cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 4)

            #Retaining angles to be used for rep counter
            return  ([leftAngle, rightAngle])  

#RUNNING CLASS INTO ACTION

#Rep Counters + Bar Raiser
score = 0
direction = 0

#While loop b/c of frame by frame capture (1 is True) (DOES THE WORK FOR THE VIDEOCAPTURE)
#Includes pose detectors
#MediaPipe Module contains all the points necesary for any certain detection
while 1:
    ret, img = cap.read() #ret is boolean if there is no capture
    img = cv2.resize(img, (640, 480)) #resize
    pd.findPose(img, draw=0)

    #Position numbers from MediaPipe, narrowing it down to points we want
    #IMPORTANT: when u print out lmlist, it gives numbers with boxes of 4 numbers doing angle work
    lmlist, bbox = pd.findPosition(img, draw=0)

    #Angle Work :)
    angles = angleFinder(lmlist, 11, 13, 15, 12, 14, 16, drawPoints=1)
    angleFunctionOutput = angles.angle() #Taking in the goods
    left, right = angleFunctionOutput[0:] #initializing

    #Direction if rep is okay and put in score
    if left >= 90 and right >= 90: #half of rep when fully up
        if direction == 0:
            score += 0.5
            direction = 1
    if left <= 70 and right <= 70: #completed rep when hands and shoulders are down
        if direction == 1:
            score += 0.5
            direction = 0

    rightval = np.interp(right, [0, 100], [400,200])
    leftval = np.interp(left, [0, 100], [400, 200])

    #Text and Box on Video showing the REP COUNTER
    cv2.rectangle(img, (0,0), (120, 120), (255, 0, 0), -1) #-1 is filled rectangle
    cv2.putText(img, str(int(score)), (1, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 6)
        
    #Bar Progress Right Hand
    cv2.putText(img, "R", (24, 194), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 5)
    cv2.rectangle(img, (8, 200), (50, 400), (0, 255, 255), 5)
    cv2.rectangle(img, (8, int(rightval)), (50, 400), (255, 0, 0), -1)

    #Bar Progress Left Hand
    cv2.putText(img, "L", (604, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 5)
    cv2.rectangle(img, (582, 200), (632, 400), (0, 255, 255), 5)
    cv2.rectangle(img, (582, int(leftval)), (632, 400), (255, 0, 0), -1)

    valueLeft = np.interp(left, [0, 100], [0, 100])
    valueRight = np.interp(left, [0, 100], [0, 100])

    if valueLeft >= 70:
        cv2.rectangle(img, (582, int(leftval)), (632, 400), (0, 0, 255), -1)
    if valueRight >= 70:
        cv2.rectangle(img, (8, int(rightval)), (50, 400), (0, 0, 255), -1)

    cv2.imshow('frame', img)
    cv2.waitKey(1) #1 is second by second


    print(time.process_time())
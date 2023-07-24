try:
    import cv2
    import mediapipe as mp
    import math
    import time
 
except ImportError:
    print("Warning: 'cv2' or 'mediapipe' or 'time' module not found. Please check the Python modules installation instructions " +
             "at 'https://www.cyberbotics.com/doc/guide/using-python'.")


#  The video source  (0) and (n) is for, to using the builtin camera of laptop and to using the nth external camera source.

class poseDetector():

    def __init__(self, mode = False, upBody = False, smooth = True, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,1,self.upBody,self.smooth,self.detectionCon,self.trackCon)



    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
                
        return img


    def findPosition(self, img, draw=True):
        LandMarksmList=[]

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c, = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                LandMarksmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255, 0, 0), cv2.FILLED)

        return LandMarksmList




def ang(points):
    elbow = points[1][1], points[1][2]
    shoulder = points[0][1], points[0][2]
    wrist = points[2][1], points[2][2]
    AB = (int(shoulder[0]) - int(elbow[0])), (int(shoulder[1]) - int(elbow[1]))
    AC = (int(wrist[0]) - int(elbow[0])), (int(wrist[1]) - int(elbow[1]))
    ab = ((AB[0] ** 2) + (AB[1] ** 2)) ** 0.5
    ac = ((AC[0] ** 2) + (AC[1] ** 2)) ** 0.5
    theta_elbow = 180 / math.pi * (math.acos((AB[0] * AC[0] + AB[1] * AC[1]) / (ab * ac)))
    return theta_elbow



def rotate(motor,angle):
    motor.setVelocity(angle)
    


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector=poseDetector()
    timestep=64
    speed=1
    
    while cap.read():
        success, img = cap.read()
        img=cv2.flip(img,1)
        img=detector.findPose(img,draw=False)
        lmList=detector.findPosition(img, False)
        AngleRadian=0.0
        if len(lmList) is not 0:
            print(lmList[12], (lmList[14]), (lmList[16]),lmList[11], (lmList[13]), (lmList[15]))

            """For Left Hand"""
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[16][1], lmList[16][2]), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (lmList[12][1],lmList[12][2]),(lmList[14][1],lmList[14][2]),(0,255,0),2)
            cv2.line(img, (lmList[14][1],lmList[14][2]),(lmList[16][1],lmList[16][2]),(0,255,0),2)
            points = [lmList[12], lmList[14], lmList[16]]
            theta_elbow=ang(points)
            cv2.putText(img, (str(int(theta_elbow))+"'"), (lmList[14][1], lmList[14][2]+50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
           
            # AngleRadian=((theta_elbow)*(.01745329252))
           
            
            
            # #angle=(AngleRadian)-(pSensor.getValue())
            # print(theta_elbow)
            # print(AngleRadian)
            # #rotate(m,1)
            # m.setPosition(AngleRadian)
            # m.setVelocity(1)
            



            """For Right Hand"""
            cv2.circle(img, (lmList[11][1], lmList[11][2]), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[13][1], lmList[13][2]), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[15][1], lmList[15][2]), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (lmList[11][1], lmList[11][2]), (lmList[13][1], lmList[13][2]), (0, 255, 0), 2)
            cv2.line(img, (lmList[13][1], lmList[13][2]), (lmList[15][1], lmList[15][2]), (0, 255, 0), 2)
            points=[lmList[11],lmList[13],lmList[15]]
            theta_elbow=ang(points)
            cv2.putText(img, (str(int(theta_elbow))+"'"), (lmList[13][1], lmList[13][2]+50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
            
            AngleRadian=((theta_elbow)*(.01745329252))
           
            
            
            #angle=(AngleRadian)-(pSensor.getValue())
            print(theta_elbow)
            print(AngleRadian)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        
        check = cv2.waitKey(30) & 0xff
        if check == 27:
            break
        
        pass



if __name__=="__main__":
    main()

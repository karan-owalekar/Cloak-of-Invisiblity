import cv2
import numpy as np
import time

#Capturing the video from webcam...
cap = cv2.VideoCapture(0)

# def nothing(x):
#     pass
# cv2.namedWindow("Trackbar")
# cv2.createTrackbar("L - H","Trackbar",0,179,nothing)
# cv2.createTrackbar("L - S","Trackbar",0,255,nothing)
# cv2.createTrackbar("L - V","Trackbar",0,255,nothing)
# cv2.createTrackbar("U - H","Trackbar",179,179,nothing)
# cv2.createTrackbar("U - S","Trackbar",255,255,nothing)
# cv2.createTrackbar("U - V","Trackbar",255,255,nothing)

#The variable specifies weather we captured the background image or not...
backgroungImage = None

#Variable thich triggers when to stat detecting the cloak color...
startInvisiblity = False
scanBg = True

now = time.time()
while True:
    ret, frame = cap.read()
    #Flipping the frame horizontally for better user experience...
    frame = cv2.flip(frame,1)

    if scanBg:
        #Here we start the countdown (it is not necessary) (after 3 sec, we capture and save the background)
        #This image will replace the part sof our cloths making it appear like we get invisible behind cloak...
        if time.time()-now >= 1 and time.time()-now < 2:
            cv2.putText(frame,"3",(220,300),cv2.FONT_HERSHEY_TRIPLEX,10, (0,0,128), 10, cv2.LINE_AA)
        elif time.time()-now >= 2 and time.time()-now < 3:
            cv2.putText(frame,"2",(220,300),cv2.FONT_HERSHEY_TRIPLEX,10, (0,0,128), 10, cv2.LINE_AA)
        elif time.time()-now >= 3 and time.time()-now < 4:
            cv2.putText(frame,"1",(220,300),cv2.FONT_HERSHEY_TRIPLEX,10, (0,0,128), 10, cv2.LINE_AA)
        elif time.time()-now > 4:
            #Saving the frame...
            backgroungImage = frame
            scanBg = False
            startInvisiblity = True

    if startInvisiblity:
        #Here we detect and seperate the cloak color ...
        #once the color is detected... We replace that area with background image...

        cv2.destroyWindow('frame') 
        # l_h = cv2.getTrackbarPos("L - H","Trackbar")
        # l_s = cv2.getTrackbarPos("L - S","Trackbar")
        # l_v = cv2.getTrackbarPos("L - V","Trackbar")
        # u_h = cv2.getTrackbarPos("U - H","Trackbar")
        # u_s = cv2.getTrackbarPos("U - S","Trackbar")
        # u_v = cv2.getTrackbarPos("U - V","Trackbar")
        
        #Setting up the limits for the color...
        lower_blue = np.array([3,200,120])
        upper_blue = np.array([30,255,255])
        # lower_blue = np.array([l_h,l_s,l_v])
        # upper_blue = np.array([u_h,u_s,u_v])

        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask= cv2.inRange(hsv,lower_blue,upper_blue)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.dilate(mask,kernel,iterations=2)
        # contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        # kernel = np.ones((3,3), np.uint8)
        # fgMask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        #cv2.imshow("mask",mask)   
        
        res = cv2.bitwise_and(backgroungImage,backgroungImage,mask = mask) 
        newFrame = cv2.bitwise_and(frame,frame,mask = 255 - mask) 
        #cv2.imshow("result",res)

        invisiblityCloak = cv2.addWeighted(res, 1, newFrame,0.95, 0)
        #invisiblityCloak = cv2.add(res,newFrame)
        cv2.imshow("Invisiblity",invisiblityCloak)

    if not startInvisiblity:
        cv2.imshow("frame",frame)
    
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
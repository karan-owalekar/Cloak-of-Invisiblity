import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbar")
cv2.createTrackbar("L - H","Trackbar",0,179,nothing)
cv2.createTrackbar("L - S","Trackbar",0,255,nothing)
cv2.createTrackbar("L - V","Trackbar",0,255,nothing)
cv2.createTrackbar("U - H","Trackbar",179,179,nothing)
cv2.createTrackbar("U - S","Trackbar",255,255,nothing)
cv2.createTrackbar("U - V","Trackbar",255,255,nothing)

while True:
    
    l_h = cv2.getTrackbarPos("L - H","Trackbar")
    l_s = cv2.getTrackbarPos("L - S","Trackbar")
    l_v = cv2.getTrackbarPos("L - V","Trackbar")
    u_h = cv2.getTrackbarPos("U - H","Trackbar")
    u_s = cv2.getTrackbarPos("U - S","Trackbar")
    u_v = cv2.getTrackbarPos("U - V","Trackbar")
    
    #lower_blue = np.array([95,105,90])
    #upper_blue = np.array([170,215,225])
    lower_blue = np.array([l_h,l_s,l_v])
    upper_blue = np.array([u_h,u_s,u_v])

    _, frame1 = cap.read()
    frame = cv2.flip(frame1, 1)

    hsv1 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    mask= cv2.inRange(hsv1,lower_blue,upper_blue)
    kernel = np.ones((5,5), np.uint8)
    #mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=4)


    cv2.imshow("frame",frame)
    cv2.imshow("result",mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
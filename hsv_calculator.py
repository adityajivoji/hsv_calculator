import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Initializing camera
# Notice: cv.CAP_DSHOW is only used some times
cap = cv.VideoCapture(0 + cv.CAP_DSHOW)
kernel = np.ones((3,3), np.uint8)
# condition to get in the loop
key = 0
font = cv.FONT_HERSHEY_SIMPLEX
show_key = False #This condition when true shows the contours
enter_key = False # This condition when true HSV values are found
# list of all the extreme values of HSV
# this list is appended after every loop with every frame if the enter_key condition is true
maxlistH = []
maxlistS = []
maxlistV = []
minlistH = []
minlistS = []
minlistV = []
# The list that contains the range for hsv thresholding the frame
lower_color = np.array([])
upper_color = np.array([])
# key == 27 is the time when Esc was pressed
while key != 27 :
    _, fram = cap.read()
    frame = cv.flip(fram, 1) # flipping the camera
    x = np.copy(frame)
    roi = frame[275:335,150:255] # grabbing the region inside the representing rectangle
    
    # drawing a rectangle
    cv.rectangle(frame,(146,251),(279,339),(0,255,0),3)
    cv.putText(frame,'place your Object such that the rectanngle is inside the object',(50,400), font, 0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame,'Once done press SpaceBar I will capture your objects HSV and draw the contour',(50,425), font, 0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame,'if satisfied press Esc else press "a" to restart',(50,450), font, 0.5,(255,255,255),2,cv.LINE_AA)
    # showing the obtained contour
    if show_key == True:
        
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  #converting frame from bgr to hsv
        mask = cv.inRange(hsv, lower_color, upper_color)    #hsv thresholding
        #applying closing operation on mask to remove noise from the image
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) 
        #dilation is done to remove some of the dark spot inside the mask
        dilation_after_closing = cv.dilate(closing,kernel,iterations = 3)
        # Prints when some region is detected on mask or modified mask
        if (mask[:] == 255).any():
            print("Maks has a white region")
        if (dilation_after_closing[:] == 255).any():
            print("Dilation after closing has a white region")
        if (dilation_after_closing[:] == 255).any():                  #if there is object in the mask at least 1 white spot will be there only then proceed to find contours
            print("HAS AN ELEMENT")
            contours, _ = cv.findContours(dilation_after_closing, 1, 2) #detecting contours
            areas = [cv.contourArea(c) for c in contours]   #finding areas of all the contourand putting them in a list
            #finding the index of the largest contour in the above list
            cnt=contours[np.argmax(areas)]
            #using the contour with larget area to draw it on the original frame
            cv.drawContours(x, [cnt] , 0, (0,255,0), 3)
        cv.imshow("Contour",x)
        cv.imshow("MASK",dilation_after_closing)
    cv.imshow("LiveROI",roi)
    cv.imshow("frame",frame)
    key = cv.waitKey(1) # asking for input
    # if the input is 'a' then it reset everything
    if key == 97:
        list_H = []
        list_S = []
        list_V = []
        maxlistH = []
        maxlistS = []
        maxlistV = []
        minlistH = []
        minlistS = []
        minlistV = []
        lower_color = np.array([0,0,0],np.uint8)      #creating the array for hsv thresholding
        upper_color = np.array([0,0,0],np.uint8)
        enter_key = False
    # if Spacebar is pressed the enter_key condition is activated
    if key == 32:
        enter_key = True
    if enter_key == True:
        hsv = cv.cvtColor(roi,cv.COLOR_RGB2HSV) # converting to HSV
        # Creating new list to append the hsv values of all the pixels
        list_H = []
        list_S = []
        list_V = []
        # Storing the values of hsv values for all 59 * 104 pixels
        for i in range(59):
            for j in range(104):
                list_H.append(hsv[i][j][0])
                list_S.append(hsv[i][j][1])
                list_V.append(hsv[i][j][2])
        #getting the min and max values from each the values from the obstained list and storing them in new list
        # This list contains all the min and max values found in all the roi's until now
        minlistH.append(min(list_H))
        minlistV.append(min(list_V))
        minlistS.append(min(list_S))
        maxlistH.append(max(list_H))
        maxlistV.append(max(list_V))
        maxlistS.append(max(list_S))
        # these value are the min of the min and max of the max found until now
        lh = min(minlistH)
        ls = min(minlistS)
        lv = min(minlistV)
        uh = max(maxlistH)
        us = max(maxlistS)
        uv = max(maxlistV)
        
        lower_color = np.array([lh, ls, lv],np.uint8)      #creating the array for hsv thresholding
        upper_color = np.array([uh, us, uv],np.uint8)
        print(lower_color,upper_color)
        #plotting the histogram of the hsv values of roi
        # hist = cv.calcHist([hsv],[0],None,[256],[0,256])
        # plt.hist(hsv.ravel(),256,[0,256])
        # plt.show()
        # The enter_key can be set to false to grab pic's whenever one wishes
        # OR if one wants it can be set to true it takes continues pic's
        enter_key = True
        show_key = True

# releasing the capture and destroying all the windows
cap.release()
cv.destroyAllWindows()


    

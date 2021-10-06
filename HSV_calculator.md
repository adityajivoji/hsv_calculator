# HSV calculator

## Method

* grab a part of the stylus get
* get all the hsv values
* find the extremes
* use it as rane for hsv thresholding
* repeat above for better results

==The code collects all the hsv value of every pixel stores them in a list then finds minimum and maximum from that list==

 
Note: In line 7 you may use
```
cap = cv.VideoCapture(0 + cv2.CAP_DSHOW)
```
cv2.CAP_DSHOW use it just incase you have an error

### enter_key

This lets the pic be grabbed and calculate the extremes of hsv values

### show_key

This lets us create mask and draw contours

### printers

In case if the 'mask' or the 'dilation_after_closing' has detected any region the given printers will be printed


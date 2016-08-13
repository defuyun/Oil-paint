import cv2
import numpy as np

img = cv2.imread('charizard_x.jpg',cv2.IMREAD_UNCHANGED)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('image1',gray)
cv2.imshow('image2',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

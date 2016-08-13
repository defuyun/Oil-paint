#!usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('charizard_x.jpg',cv2.IMREAD_GRAYSCALE)

# param: window title, image var
cv2.imshow('image',img)
#cv2.waitKey(0)

#plt.imshow(img,cmap='gray',interpolation='bicubic')
# draw a line the 'c' means color the line
#plt.plot([50,100],[80,100],'c',linewidth=5)
#plt.show()
cv2.imwrite('greyimg.png',img)

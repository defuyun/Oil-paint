#!/usr/bin/python

import cv2
import numpy as np
import sys
import os

mask_size = 5

def get_equal_pixel(img,row,col):
    start_i,start_j = (row - mask_size/2,col - mask_size/2);
    end_i,end_j = (row + mask_size/2,col + mask_size/2)
    wanted = img.item(row,col,0)
    L = []

    for i in range(max(0,start_i),min((img.shape)[0],end_i)):
        for j in range(max(0,start_j),min((img.shape)[1],end_j)):
            if img.item(i,j,0) == wanted:
                L.append((i,j))
    return L

def avIntensity(L,img):
    r,g,b = (0,0,0)
    for row,col in L:
        r += img.item(row,col,2)
        g += img.item(row,col,1)
        b += img.item(row,col,0)

    return (r/len(L),g/len(L),b/len(L))

def most_freq_pixel(img,row,col):
    start_i,start_j = (row - mask_size/2,col - mask_size/2);
    end_i,end_j = (row + mask_size/2,col + mask_size/2)

    count = {}
    for i in range(max(0,start_i),min((img.shape)[0],end_i)):
        for j in range(max(0,start_j),min((img.shape)[1],end_j)):

            pixel = img.item(i,j,0)
            val = count.get(pixel,None)
            if val == None:
                count[pixel] = 1
            else:
                count[pixel] += 1

    maxfreq = (0,0)
    for pixel,val in count.iteritems():
        if val > maxfreq[1]:
            maxfreq = (pixel,val)

    return maxfreq

def process(filename):
    img = cv2.imread(filename)
    name = os.path.splitext(filename)[0]

    height,width,depth = img.shape
    global mask_size

    print "image: " + filename + "(" + str(height) + "x" + str(width) + ")"

    mask_size = max(3,min((width * height)/10000,10))
    # mask_size = 9

    print "mask size set to: " + str(mask_size)

    for i in range(height):
        for j in range(width):
            r = img.item(i,j,2)
            g = img.item(i,j,1)
            b = img.item(i,j,0)

            I = 0.299 * r + 0.587 * g + 0.114 * b
            img.itemset((i,j,2),I)
            img.itemset((i,j,1),I)
            img.itemset((i,j,0),I)

    cv2.imwrite(str(name+'_task1.png'),img)
    print "task1 generated"

    # use a copy because if we overwrite while processing
    # we'd get the wrong result
    copy = img.copy()

    for i in range(height):
        for j in range(width):

            I = most_freq_pixel(copy,i,j)[0]
            img.itemset((i,j,2),I)
            img.itemset((i,j,1),I)
            img.itemset((i,j,0),I)

    cv2.imwrite(str(name+'_task2.png'),img)
    print "task2 generated"

    org = cv2.imread(filename)
    copy = img.copy()

    for i in range(height):
        for j in range(width):
            rgb = avIntensity(get_equal_pixel(copy,i,j),org)
            img.itemset((i,j,2),rgb[0])
            img.itemset((i,j,1),rgb[1])
            img.itemset((i,j,0),rgb[2])

    cv2.imwrite(str(name+'_task3.png'),img)
    print "task3 generated"

    # additional smoothing
    kernel = np.ones((mask_size,mask_size),np.float32)/(mask_size * mask_size)
    img = cv2.filter2D(img,-1,kernel)
    cv2.imwrite(str(name+'_blur.png'),img)
    print "smoothing generated"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        process(sys.argv[1])
    else:
        print "usage: " + sys.argv[0] + " <filename>"

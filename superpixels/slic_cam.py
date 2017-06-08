#!/usr/bin/python

'''
This sample demonstrates SEEDS Superpixels segmentation
Use [space] to toggle output mode

Usage:
  seeds.py [<video source>]

'''

# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
import numpy as np
import cv2
import sys
import time

if __name__ == '__main__':
  print __doc__

  try:
      fn = sys.argv[1]
  except:
      fn = 0

  def nothing(*arg):
      pass

  cv2.namedWindow('slic')
  cv2.createTrackbar('Number of Segments', 'slic', 100, 1000, nothing)
  cv2.createTrackbar('Sigma', 'slic', 5, 12, nothing)

  display_mode = 0

  cap = cv2.VideoCapture(fn)
  while cap.isOpened():
      flag, img = cap.read()

      if not flag:
        cap.release()
        exit()

      #get data from bars
      numSegments = cv2.getTrackbarPos('Number of Segments', 'slic')
      numSigma = cv2.getTrackbarPos('Sigma', 'slic')
      
      #segment
      start_time = time.time()   #  save curr time to report duration
      segments = slic(img.astype(np.float64)/256, n_segments = numSegments, sigma = numSigma)
      duration = time.time() - start_time # calculate time elapsed
      print("slic elapsed: ",duration)

      #mark segments in image
      start_time = time.time()   #  save curr time to report duration
      img = mark_boundaries(img, segments)
      duration = time.time() - start_time # calculate time elapsed
      print("mark boundaries elapsed: ",duration)

      #make a mask
      mask = np.zeros(img.shape)
      mask = mark_boundaries(mask, segments)

      if display_mode == 0:
          cv2.imshow('slic', img)
      else:
          cv2.imshow('slic', mask)

      ch = cv2.waitKey(1)
      if ch == 27:
          break
      elif ch & 0xff == ord(' '):
          display_mode = (display_mode + 1) % 2
  cap.release()
  cv2.destroyAllWindows()

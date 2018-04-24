# -*- coding: utf-8 -*-

import datetime,sys
from threading import Thread

import datetime,sys
import os, time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import subprocess

from WeChatBase import WeChatBase
from AndroidBase import AndroidBase
from DouYinBase import DouYinBase

#Strawberry=cv2.imread("01.png")

img1 = cv2.imread("01.png")
img2 = plt.imread("01.png")

(r, g, b)=cv2.split(img1)
img1 = cv2.merge([b,g,r])

plt.subplot(121)
plt.imshow(img1)

plt.subplot(122)
plt.imshow(img2)

plt.show()

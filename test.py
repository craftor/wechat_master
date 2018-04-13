# -*- coding: utf-8 -*-
import os, time
import cv2
import numpy as np
from matplotlib import pyplot as plt

image = '02.png'
Target = 'template/1080/dianzan_rukou.png'

img_rgb = cv2.imread(image)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(Target, 0)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
loc = np.where( res >= 0.7)
#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
#print(cv2.minMaxLoc(res))
print(loc)
for a in loc:
    #print ('xxx', a)
    if len(a) :
        print ("Yes")
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
        print (max_loc)
    else:
        print ("Empty")
#print(zip(*loc[::-1]))
for pt in zip(*loc[::-1]):
    #print (pt)
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
# plt.imshow(img_rgb)
# plt.xticks([]), plt.yticks([])
# plt.show()
cv2.imwrite(str(image) + '_d.png',img_rgb)

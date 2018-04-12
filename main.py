# -*- coding: utf-8 -*-
import os
import time
import numpy as np
import cv2
import WeChatBase 

VERSION = "0.1"

def showImg(res):
    cv2.namedWindow('Test', cv2.WINDOW_KEEPRATIO)
    cv2.imshow('Test',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    #myWeChat.UnlockScreen(0)
    myWeChat.ReLaunchWechat()
    myWeChat.EnterMoment()

if __name__ == '__main__':
    myWeChat = WeChatBase.WeChatBase()
    #main()
    while(True):
        myWeChat.ClickLike()
        myWeChat.RollingUpScreen(500)
        myWeChat.Sleep(0.5)

# -*- coding: utf-8 -*-
import os, time
import cv2
import numpy as np
from matplotlib import pyplot as plt
import subprocess

# 截图文件名
ScreenShotFileName = "Tmp01.png"
ScreenShotDetected = "Tmp02.png"

class AndroidBase():

    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.dir_root = "."
        self.threshold = 0.7 # 图像比对默认阈值

    # 重新定向命令
    def SendCommand(self, command):
        #os.system(str)
        result = subprocess.call(command, shell=True)
        #result = os.popen(command)
        #result.wait()
        #self.LogPrint(str(result))

    # 截屏
    def PullScreenShot(self):
        cmd = 'adb shell screencap -p /sdcard/' + ScreenShotFileName
        self.SendCommand(cmd)
        cmd = 'adb pull /sdcard/' + ScreenShotFileName + ' .'
        self.SendCommand(cmd)

    # 延时，时间单位为秒
    def Sleep(self, t):
        time.sleep(t)

    # 单击操作
    def OneClick(self, x, y):
        cmd = 'adb shell input tap ' + str(x) + ' ' + str(y)
        self.SendCommand(cmd)

    # 双击操作
    def DoubleClock(self, x, y):
        pass

    # 返回按钮
    def ClickReturn(self):
        cmd = 'adb shell input keyevent 4'
        self.SendCommand(cmd)

     # 滑动操作
    def Rolling(self, x1, y1, x2, y2):
        cmd = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2)
        self.SendCommand(cmd)

    # 上滑屏幕
    def RollingUpScreen(self, step):
        self.Rolling(int(self.width/2), int(self.height/2), int(self.width/2), int(self.height/2) - step)

    # 下滑屏幕
    def RollingDownScreen(self, step):
        self.Rolling(int(self.width/2), int(self.height/2), int(self.width/2), int(self.height/2) + step)

    # 获取屏幕尺寸，非常重要
    def GetScreenSize(self):
        self.PullScreenShot()
        img = cv2.imread(ScreenShotFileName, 3)
        self.height, self.width = img.shape[:2]

    # 点击电源键，点亮屏幕
    def LightScreen(self):
        cmd = 'adb shell input keyevent 26'
        self.SendCommand(cmd)

    # 解锁屏幕
    def UnlockScreen(self, phone):
        self.LightScreen()
        self.Sleep(1)
        # 根据phone类型，选择滑动解锁方式
        if phone == 0: # 上滑
            self.RollingUpScreen(800)

    # 1个条件比对
    def CompareOne(self, cond1):
        # 比对条件
        yes1, max_loc1 = self.myClient.MatchImg(cond1)
        # 检查
        if (yes1):
            return True
        else:
            return False

    # 2个条件比对
    def CompareTwo(self, cond1, cond2):
        # 比对条件
        yes1, max_loc1 = self.myClient.MatchImg(cond1)
        yes2, max_loc2 = self.myClient.MatchImg(cond2)
        # 检查
        if (yes1 and yes2):
            return True
        else:
            return False

    # 3个条件比对
    def CompareThree(self, cond1, cond2, cond3):
        # 比对条件
        yes1, max_loc1 = self.myClient.MatchImg(cond1)
        yes2, max_loc2 = self.myClient.MatchImg(cond2)
        yes3, max_loc3 = self.myClient.MatchImg(cond3)
        # 检查
        if (yes1 and yes2 and yes3):
            return True
        else:
            return False

    # 找匹配图标
    def MatchImg(self, Target):
        # 原始图片
        img_rgb = cv2.imread(ScreenShotFileName)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # 比对模板图片
        temp_url = self.dir_root + "/" + Target
        #print(temp_url)
        template = cv2.imread(temp_url, 0)
        # 获取模板图片尺寸
        w, h = template.shape[::-1]
        # 比对操作
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        # 比对结果坐标
        loc = np.where( res >= self.threshold)
        #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
        #print(cv2.minMaxLoc(res))
        #print(loc)

        # 描绘出外框
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
        # 保存识别目标后的图
        cv2.imwrite(ScreenShotDetected, img_rgb)

        # 检查比对结果
        for pp in loc:
            # 如果不为空，说明有比对成果的内容
            if len(pp) :
                #print ("Yes")
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
                #print (max_loc)
                return True, max_loc
            else:
                #print ("Empty")
                return False, []

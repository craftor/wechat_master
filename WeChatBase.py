# -*- coding: utf-8 -*-
import os, time
import cv2
import numpy as np
from matplotlib import pyplot as plt

VERSION = "0.1"


methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


class WeChatBase():
    
    # 启动初始化
    def __init__(self):
        self.width = 1080  # 默认屏幕宽
        self.height = 1920 # 默认屏幕高
        self.filename = '01.png' # 截图默认文件情况
        self.threshold = 0.7 # 图像比对默认阈值
        self.GetScreenSize() # 初始化先通过截图试获取屏幕分辨率

    # 截屏
    def PullScreenShot(self, filename):
        os.system('adb shell screencap -p /sdcard/' + filename )
        os.system('adb pull /sdcard/' + filename + ' .')
    
    # 延时，时间单位为秒
    def Sleep(self, t):
        time.sleep(t)

    # 单击操作
    def OneClick(self, x, y):
        os.system('adb shell input tap ' + str(x) + ' ' + str(y))

    # 双击操作
    def DoubleClock(self, x, y):
        pass

    # 返回按钮
    def ClickReturn(self):
        os.system('adb shell input keyevent 4')

     # 滑动操作
    def Rolling(self, x1, y1, x2, y2):
        os.system('adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2))

    # 上滑屏幕
    def RollingUpScreen(self, step):
        self.Rolling(int(self.width/2), int(self.height/2), int(self.width/2), int(self.height/2) - step)

    # 下滑屏幕
    def RollingDownScreen(self, step):
        self.Rolling(int(self.width/2), int(self.height/2), int(self.width/2), int(self.height/2) + step)

    # 获取屏幕尺寸，非常重要
    def GetScreenSize(self):
        self.PullScreenShot(self.filename)
        img = cv2.imread(self.filename, 3)
        self.height, self.width = img.shape[:2]

    # 点击电源键，点亮屏幕
    def LightScreen(self):
        os.system('adb shell input keyevent 26')

    # 解锁屏幕
    def UnlockScreen(self, phone):
        self.LightScreen()
        self.Sleep(1)
        # 根据phone类型，选择滑动解锁方式
        if phone == 0:
            self.RollingUpScreen()
    
    # 启动微信
    def LaunchWeChat(self):
        os.system('adb shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI')

    # 点击“发现” -> "朋友圈"
    def EnterMoment(self):
        self.OneClick(int(self.width*5/8), int(self.height*19/20))
        self.Sleep(1)
        self.OneClick(int(self.width*5/8), int(self.height*1/5))

    # 重启微信
    def ReLaunchWechat(self):
        self.LaunchWeChat()
        self.Sleep(1)
        self.ClickReturn()
        self.Sleep(1)
        self.ClickReturn()
        self.Sleep(1)
        self.ClickReturn()
        self.LaunchWeChat()

    # 找到匹配图标
    def MatchImg(self, image, Target):
        img_rgb = cv2.imread(image)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= self.threshold)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
        #print(cv2.minMaxLoc(res))
        #print(loc)
        #print(zip(*loc[::-1]))
        for pt in zip(*loc[::-1]):
            #print (pt)
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)   
        # plt.imshow(img_rgb)
        # plt.xticks([]), plt.yticks([])
        # plt.show()
        cv2.imwrite(str(image) + '_d.png',img_rgb)
        return max_loc

    # For Test
    def Test(self):
        print("Test")

    # 点赞
    def ClickLike(self):

        tmp1 = 'template\dianzan_rukou.png'
        tmp2 = 'template\zan_icon.png'
        tmp3 = 'template\zan_text.png'
        tmp4 = 'template\zan_quxiao_text.png'
        self.PullScreenShot('01.png')

        # 找到待点赞的朋友圈
        max_loc1 = self.MatchImg('01.png', tmp1)
        if (max_loc1[0]>self.width/2 and max_loc1[1] > 200):
            print(u"找到朋友圈消息，坐标：", max_loc1)

            # 点开赞框
            print(u"查看是否赞过")
            self.OneClick(max_loc1[0]+10, max_loc1[1]+10)
            self.Sleep(1.5)
            self.PullScreenShot('02.png')
            max_loc2 = self.MatchImg('02.png', tmp3)
            # 检查是否赞过
            if (max_loc2[0] > self.width/3 and max_loc2[1] > 200):
                print(u"未赞过，正在点赞")
                self.OneClick(max_loc2[0]+10, max_loc2[1]+10)
                print(u"点赞成功")
            else:
                print(u"已经赞过，忽略")
                self.OneClick(max_loc1[0]+10, max_loc1[1]+10)

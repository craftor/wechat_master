# -*- coding: utf-8 -*-
import os, time
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 软件版本
VERSION = "0.1"

# 分辨率
resolution = "1080"  # 1080 or 720
# 图标存放目标
dir_root = "template"
# 图标名
main_tongxunlu = 'main_tongxunlu.png' # 主菜单，通信录
main_faxian    = 'main_faxian.png'    # 主菜单，发现
main_me        = 'main_me.png'        # 主菜单，我
zan_rukou      = 'zan_rukou.png'      # 点赞，入口
zan_icon       = 'zan_icon.png'       # 点赞，图标
zan_text       = 'zan_text.png'       # 点赞，文字
zan_quxiao     = 'zan_quxiao.png'     # 点赞，取消
pyq_fanhui     = 'pyq_fanhui.png'     # 朋友圈，返回键图标
pyq_text       = 'pyq_text.png'       # 朋友圈，文字
pyq_xiangji    = 'pyq_xiangji.png'    # 朋友圈，相机图标
# 截图文件名
file_first = "01.png"  # 第一个

class WeChatBase():

    # 启动初始化
    def __init__(self):
        self.width = 1080  # 默认屏幕宽
        self.height = 1920 # 默认屏幕高
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
        self.PullScreenShot(file_first)
        img = cv2.imread(file_first, 3)
        self.height, self.width = img.shape[:2]

    # 点击电源键，点亮屏幕
    def LightScreen(self):
        os.system('adb shell input keyevent 26')

    # 解锁屏幕
    def UnlockScreen(self, phone):
        self.LightScreen()
        self.Sleep(1)
        # 根据phone类型，选择滑动解锁方式
        if phone == 0: # 上滑
            self.RollingUpScreen(800)

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

    # 找匹配图标
    def MatchImg(self, image, Target):
        # 原始图片
        img_rgb = cv2.imread(image)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # 比对模板图片
        temp_url = dir_root + "/" + resolution + "/" + Target
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
        cv2.imwrite(str(image) + '_d.png',img_rgb)

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

    # For Test
    def Test(self):
        print("Test")

    # 检查是否在主菜单下
    def CheckIsMain(self, FileName):
        # 比对条件
        yes1, max_loc1 = self.MatchImg(FileName, main_tongxunlu)
        yes2, max_loc2 = self.MatchImg(FileName, main_faxian)
        yes3, max_loc3 = self.MatchImg(FileName, main_me)
        # 检查
        if (yes1 and yes2 and yes3):
            return True
        else:
            return False

    # 检查是否在朋友圈状态下
    def CheckInMoment(self, FileName):
        # 比对条件
        yes1, max_loc1 = self.MatchImg(FileName, pyq_fanhui)
        yes2, max_loc2 = self.MatchImg(FileName, pyq_text)
        yes3, max_loc3 = self.MatchImg(FileName, pyq_xiangji)
        # 检查
        if (yes1 and yes2 and yes3):
            return True
        else:
            return False

    # 点赞
    def ClickLike(self):
        # 截图文件名
        FileName1 = 'ClickLike1.png'
        FileName2 = 'ClickLike2.png'

        # 截图
        self.PullScreenShot(FileName1)

        # 检查是否在朋友圈下
        yes = self.CheckInMoment(FileName1)
        if yes:
            pass
        else:
            print(u"不在朋友圈下")
            return 0

        # 查找待点赞的朋友圈
        yes1, max_loc1 = self.MatchImg(FileName1, zan_rukou)

        if yes1:
            print(u"找到朋友圈消息，坐标：", max_loc1)
            # 点开赞框
            print(u"查看是否赞过")
            self.OneClick(max_loc1[0]+10, max_loc1[1]+10)
            self.Sleep(1)
            self.PullScreenShot(FileName2)
            yes2, max_loc2 = self.MatchImg(FileName2, zan_text)
            yes3, max_loc3 = self.MatchImg(FileName2, zan_quxiao)

            # 查看是否赞过
            if yes2 :
                print(u"未赞过，准备点赞")
                self.OneClick(max_loc2[0]+10, max_loc2[1]+10)
                print(u"点赞成功")
            #取消赞操作
            # elif yes3:
            #     print(u"已经赞过，取消")
            #     self.OneClick(max_loc2[0]+10, max_loc2[1]+10)
            # 忽略
            else :
                print(u"已经赞过，忽略")
                self.OneClick(max_loc1[0]+10, max_loc1[1]+10)
        else:
            print(u"未发现最新朋友圈消息")

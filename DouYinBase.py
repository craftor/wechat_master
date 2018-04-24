# -*- coding: utf-8 -*-
import uiautomator2 as u2
import datetime
import os
import time
import numpy as np
import cv2
import subprocess
from threading import Thread
from multiprocessing import Process
from AndroidBase import AndroidBase

# 分辨率
resolution = "1080"  # 1080 or 720
# 图标存放目标
dir_root = "douyin"
# 图标名
follow="follow.png"  # 加好友图标

IP=""

class DouYinU2():
    # 初始化
    def __init__(self):
        self.ip = "192.168.1.118"
        #selr.Android = AndroidBase()
        self.client = u2.connect(self.ip)
        # set delay 1.5s after each UI click and click
        self.client.click_post_delay = 0.2 # default no delay
        # set default element wait timeout (seconds)
        self.client.wait_timeout = 5.0 # default 20.0

    # 打开连接并转到抖音
    def OpenURL(self, url):
        self.client.adb_shell('am start -n com.android.browser/com.android.browser.BrowserActivity')
        self.client.adb_shell('am start -a android.intent.action.VIEW -d ', url)
        self.client(description=u"打开看看").click()
        time.sleep(5)

    # 点赞
    def AwesomeMe(self):
        self.client(resourceId="com.ss.android.ugc.aweme:id/a62").click()

    # 加关注
    def AddFriend(self):
        #self.client(resourceId="com.ss.android.ugc.aweme:id/a60").click()
        self.client.click(0.924, 0.416)

    # 评论
    def Comment(self, text):
        # 点 评论
        self.client.click(0.918, 0.609)
        # 点 聊天框
        self.client.click(0.471, 0.963)
        # 输入内容
        self.client.send_keys(str(text))
        # 发送
        self.client.click(0.926, 0.861)
        # 返回
        self.client.press("back")


    # 通过发坐标方式发消息（更快）
    def SendMsgXY(self, text):
        # 先点头像
        self.client.click(0.915, 0.373)
        # 点 发消息
        self.client.click(0.648, 0.199)
        # 点 聊天框
        self.client.click(0.316, 0.956)
        # 输入内容
        self.client.send_keys(str(text))
        # 发送
        self.client.click(0.926, 0.861)
        # 返回2次
        self.client.click(0.057, 0.073)
        self.client.click(0.057, 0.073)

    # 发消息
    def SendMessage(self, text):
        # 先点头像
        self.client(resourceId="com.ss.android.ugc.aweme:id/a5w").click()
        # 发消息
        self.client(resourceId="com.ss.android.ugc.aweme:id/uz").click()
        # 聊天框
        self.client(resourceId="com.ss.android.ugc.aweme:id/ab9").click()
        # 输入内容
        self.client.send_keys(str(text))
        # 发送
        self.client(resourceId="com.ss.android.ugc.aweme:id/ab_").click()
        # 返回
        self.client(resourceId="com.ss.android.ugc.aweme:id/lt").click()
        # 返回
        self.client(resourceId="com.ss.android.ugc.aweme:id/gz").click()


class DouYinBase():

    # 初始化
    def __init__(self):
        self.myClient = AndroidBase()
        self.myClient.dir_root = dir_root + "/" + resolution # 指定图标存放目录

    # 首页
    def EnterShouye(self):
        self.myClient.LogPrint(u"首页")
        self.myClient.OneClick(int(self.myClient.width*1/5), int(self.myClient.height*19/20))
        #self.myClient.Sleep(1)

    # 进入关注用户
    def EnterGuanzhu(self):
        self.myClient.LogPrint(u"查看关注")
        self.myClient.OneClick(int(self.myClient.width*2/5), int(self.myClient.height*19/20))
        #self.myClient.Sleep(1)

    # 查看消息
    def EnterXiaoxi(self):
        self.myClient.LogPrint(u"查看消息")
        self.myClient.OneClick(int(self.myClient.width*4/5), int(self.myClient.height*19/20))
        #self.myClient.Sleep(1)

    # 点击关注用户的第一个抖音内容
    def ClickFirstGuanZhu(self):
        self.myClient.LogPrint(u"点击关注用户抖音")
        self.myClient.OneClick(int(self.myClient.width/3), int(self.myClient.height/3))
        #self.myClient.Sleep(1)

    # 点赞
    def ClickLike(self):
        self.myClient.LogPrint(u"点赞")
        self.myClient.OneClick(int(self.myClient.width*7/8), int(self.myClient.height/2))

    # 关注
    def ClickFollow(self):
        self.myClient.LogPrint(u"检测是否已关注。。。")
        # 截图
        self.myClient.PullScreenShot()
        # 检查是否有未关注图标
        yes, max_loc = self.myClient.MatchImg(follow)
        if yes:
            self.myClient.LogPrint(u"未关注，点击关注")
            self.myClient.OneClick(max_loc[0], max_loc[1])
        else:
            self.myClient.LogPrint(u"已关注，忽略")
            #self.myClient.OneClick(int(self.myClient.width*7/8), int(self.myClient.height*3/8))

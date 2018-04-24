# -*- coding: utf-8 -*-

import datetime,sys
import time
from threading import Thread

from WeChatBase import WeChatBase
from AndroidBase import AndroidBase
from DouYinBase import DouYinBase, DouYinU2

# 打印日志
def LogPrint(text):
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    mystr = otherStyleTime + "  " + text
    print(mystr)

class Main_Test():
    def __init__(self):
        #self.myAndroid = AndroidBase()
        self.myDouyin = DouYinU2()
        self.myDouyin.ip = "192.168.1.120"

    def Run(self):

        while(True):
            # 暂时视频播放
            LogPrint(u"暂时视频")
            self.myDouyin.client.click(500, 500)
            # 点赞
            LogPrint(u"点赞")
            self.myDouyin.AwesomeMe()
            # 加好友
            LogPrint(u"加好友")
            self.myDouyin.AddFriend()
            # 发消息
            #LogPrint(u"发消息")
            #self.myDouyin.SendMsgXY(u"互粉，谢谢^_^")
            # 暂时视频播放
            #self.myDouyin.client.click(500, 500)
            #LogPrint(u"评论")
            #self.myDouyin.Comment("666")
            # 下一个
            LogPrint(u"下一个")
            self.myDouyin.client.swipe(0.5, 0.8, 0.5, 0.2, 0.1)
            time.sleep(3)

            #self.myAndroid.RollingUpScreen(500)
            #time.sleep(1)

class Main_Douyin():

    def __init__(self):
        self.myAndroid = AndroidBase()
        self.myDouyin = DouYinBase()

    def Run(self):
        #self.myDouyin.EnterGuanzhu()
        #self.myDouyin.ClickFirstGuanZhu()
        while(True):
            self.myAndroid.LogPrint(u"上滑屏幕")
            self.myAndroid.RollingUpScreen(500)
            self.myAndroid.Sleep(0.1)
            self.myDouyin.ClickLike()
            #self.myDouyin.ClickFollow()

class Main_Wechat():

    def __init__(self):
        # 微信
        self.myWeChat = WeChatBase()
        self.myAndroid = AndroidBase()

        # 点赞线程
        self.t_LikeRun = False

        # 线程
        self.t_LikeThread = Thread(target=self.ThreadClickLike, name='LikeThread')

    # 朋友圈线程入口
    def ThreadClickLike(self):
        while(self.t_LikeRun):
            #self.LogPrint(u"点赞开始")
            if self.myWeChat.ClickLike():
                self.myAndroid.LogPrint(u"上滑屏幕")
                self.myAndroid.RollingUpScreen(500)
            #self.Sleep(0.5)
            #self.LogPrint(u"点赞结束")

    def Run(self):
    	if (self.t_LikeRun):
    	    #self.pushButton_AutoStartWeChat.setText(u"停止中。。。")
    	    self.myAndroid.LogPrint(u"==========正在退出点赞线程==========")
    	    self.t_LikeRun = False
    	    self.t_LikeThread.join()
    	    self.myAndroid.LogPrint(u"==========点赞线程已经停止==========")
    	    #self.pushButton_AutoStartWeChat.setText(u"开始")
    	else:
    	    self.myAndroid.LogPrint(u"==========正在启动点赞线程==========")
    	    self.t_LikeRun = True
    	    self.t_LikeThread.start()
    	    self.myAndroid.LogPrint(u"==========点赞线程已经启动==========")
    	    #self.pushButton_AutoStartWeChat.setText(u"停止")

if __name__ == '__main__':
    #test = WeChatUser()
    test = Main_Test()
    test.Run()

# -*- coding: utf-8 -*-

"""
Module implementing Form.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject

from Ui_main import Ui_Dialog

import datetime,sys
from threading import Thread

from WeChatBase import WeChatBase
from AndroidBase import AndroidBase

# 输出重定向
class EmittingStream(QObject):
    textWritten = pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class Main(QWidget, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        # 微信
        self.myWeChat = WeChatBase()
        self.myAndroid = AndroidBase()

        # 点赞线程
        self.t_LikeRun = False

        # 重定向
        sys.stdout = EmittingStream(textWritten=self.LogPrint)
        sys.stderr = EmittingStream(textWritten=self.LogPrint)

        super(Main, self).__init__(parent)
        self.setupUi(self)

    # 打印日志
    def LogPrint(self, text):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        mystr = otherStyleTime + "  " + text
        self.textEdit_Print.append(mystr)

    # 朋友圈线程入口
    def ThreadClickLike(self):
        while(self.t_LikeRun):
            #self.LogPrint(u"点赞开始")
            if self.myWeChat.ClickLike():
                print(u"上滑屏幕")
                self.myAndroid.RollingUpScreen(500)
            #self.Sleep(0.5)
            #self.LogPrint(u"点赞结束")

    @pyqtSlot()
    def on_pushButton_AutoStartWeChat_clicked(self):
        """
        Slot documentation goes here.
        """
        if (self.t_LikeRun):
            self.pushButton_AutoStartWeChat.setText(u"停止中。。。")
            print(u"==========正在退出点赞线程==========")
            self.t_LikeRun = False
            self.t_LikeThread.join()
            print(u"==========点赞线程已经停止==========")
            self.pushButton_AutoStartWeChat.setText(u"开始")
        else:
            print(u"==========正在启动点赞线程==========")
            self.t_LikeRun = True
            self.t_LikeThread = Thread(target=self.ThreadClickLike, name='LikeThread')
            self.t_LikeThread.start()
            print(u"==========点赞线程已经启动==========")
            self.pushButton_AutoStartWeChat.setText(u"停止")

    @pyqtSlot()
    def on_pushButton_RunWeChat_clicked(self):
        """
        Slot documentation goes here.
        """
        pass

    @pyqtSlot()
    def on_pushButton_ClearLog_clicked(self):
        """
        Slot documentation goes here.
        """
        self.textEdit_Print.setText("")

    @pyqtSlot()
    def on_pushButton_AutoAddFriends_clicked(self):
        """
        Slot documentation goes here.
        """
        pass

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    dlg = Main()
    dlg.show()
    sys.exit(app.exec_())

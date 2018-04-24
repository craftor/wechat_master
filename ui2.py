import uiautomator2 as u2
import time

d = u2.connect('192.168.1.117') # alias for u2.connect_wifi('10.0.0.1')
#d = u2.connect_usb("350dec9b")
#print(d.info)
#d.app_start('com.tencent.mm')

url = 'https://www.iesdouyin.com/share/video/6530107251573656839'

print(u"打开视频")
d.adb_shell('am start -n com.android.browser/com.android.browser.BrowserActivity')
d.adb_shell('am start -a android.intent.action.VIEW -d ', url)
print(u"转到抖音")
d(description=u"打开看看").click()
time.sleep(5)
print(u"点赞")
d.click(985, 973)
#d(resourceId="com.ss.android.ugc.aweme:id/a5b").click()
#d(resourceId="com.ss.android.ugc.aweme:id/a62").click()
#time.sleep(3)
#d.click(0.924, 0.503)
print(u"完成")
#d(text="打开看看").click()

d(resourceId="com.ss.android.ugc.aweme:id/a60").click()

#sess = d.session("com.tencent.mm")
#sess = d.session("com.tencent.mm", attach=True)

#sess(text="发现").click()

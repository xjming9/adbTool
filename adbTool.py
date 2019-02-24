# -*-coding:utf-8 -*-
#__author__:xjming
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from adb import *
import sys, os, re, time, threading
from untitled import Ui_Form


class MyForm(QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.status = ''
        self.device = ''  # 当前设备
        self.devices = 0  # 设备数量
        self.package = ''  # 程序包路径
        self.setupUi(self)
        self.loadDev()
        self.treeWidget.clicked.connect(self.chooseDev)

    def loadDev(self):  # 加载设备
        devices = getDevicesInfo()
        if devices == -1:
            self.devices = 0
            self.showresult('未连接设备')
        else:
            self.devices = len(devices)
            self.label.setText('已连接%d台设备' % self.devices)
        try:
            self.device = devices[0]  # 默认第一个设备为当前设备
            for i in range(len(devices)):
                QTreeWidgetItem(self.treeWidget).setText(0, devices[i])
        except:
            pass

    def reload(self):
        if not self.devices == 0:
            for i in range(self.devices):
                self.treeWidget.takeTopLevelItem(i)
        self.loadDev()
        self.showresult('刷新成功！')

    def chooseDev(self):
        item = self.treeWidget.currentItem()
        # print('Key=%s,value=%s' % (item.text(0), item.text(1)))
        self.device = item.text(0)
        name = getDevName(self.device)
        screen = getDecScreen(self.device)
        version = getVersion(self.device)
        msg = '设备名称：%s\n屏幕分辨率：%s\n系统版本：%s' % (name, screen, version)
        self.showresult(msg)

    def reboot(self):
        if self.device == '':
            self.showresult('未连接设备！')
            return
        self.showresult('重启中。。。')
        thread = RunThread(self.device)
        thread.start()
        thread.trigger.connect(self.TimeStop)

    def choose(self):
        self.textBrowser.setText('')
        self.package = QFileDialog.getOpenFileName(self, 'open file', '/')
        if self.package[0]:
            if re.match('.*?apk', self.package[0]):
                self.lineEdit.setText(self.package[0])
            else:
                # self.filename[0] = ''
                self.package = ''
                self.showresult('请选择正确的安装包！')


    def install(self):
        if self.package:
            installapp(self.device, self.package[0])
        else:
            self.showresult('请选择安装包！')

    def TimeStop(self):
        self.showresult('重启完成！')


    def screencap(self):
        self.showresult('正在截图！')
        if self.device == '':
            self.showresult('未连接设备！')
            return
        self.textBrowser.setText('')
        filename = time.strftime("%Y%m%d%H%M%S")
        date = time.strftime("%Y%m%d")
        path = os.path.join(os.path.split(os.path.realpath(__file__))[0], r'screencap\%s' % date)
        if not os.path.exists(path):
            os.makedirs(path)
        screencap(self.device, filename, os.path.join(path, '%s.png' % filename))
        time.sleep(2)
        self.label_2.setScaledContents(True)
        self.label_2.setPixmap(QPixmap(os.path.join(path, '%s.png' % filename)))
        self.showresult('截图成功！\n保存路径：%s' % os.path.join(path, '%s.png' % filename))

    def log(self):
        pass

    def showresult(self, result):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        self.textBrowser.setText(now+'\n'+result)


class RunThread(QThread):
        # python3,pyqt5与之前的版本有些不一样
        #  通过类成员对象定义信号对象
        # _signal = pyqtSignal(str)

    trigger = pyqtSignal()

    def __init__(self, device):
        super(RunThread, self).__init__()
        self.device = device
    def __del__(self):
        self.wait()

    def run(self):
        # 处理你要做的业务逻辑，这里是通过一个回调来处理数据，这里的逻辑处理写自己的方法
        # wechat.start_auto(self.callback)
        # self._signal.emit(msg);  可以在这里写信号焕发
        devReboot(self.device)
        while True:
            devices = getDevicesInfo()
            time.sleep(10)
            if devices != -1:
                self.trigger.emit()
            else:
                time.sleep(3)
        # self._signal.emit(msg)

    def callback(self, msg):
        # 信号焕发，我是通过我封装类的回调来发起的
        # self._signal.emit(msg)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyForm = MyForm()
    MyForm.show()
    sys.exit(app.exec_())


# -*-coding:utf-8 -*-
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
        self.device = ''
        self.filename = ''
        self.setupUi(self)
        self.loadDev()
        self.treeWidget.clicked.connect(self.chooseDev)

    def loadDev(self):  # 加载设备
        devices = getDevicesInfo()
        try:
            self.device = devices[0]
            QTreeWidgetItem(self.treeWidget).setText(0, devices[0])
            QTreeWidgetItem(self.treeWidget).setText(0, devices[1])
            QTreeWidgetItem(self.treeWidget).setText(0, devices[2])
        except:
            pass

    def reload(self):
        self.loadDev()
        self.textBrowser.setText('刷新成功！')

    def chooseDev(self):
        item = self.treeWidget.currentItem()
        # print('Key=%s,value=%s' % (item.text(0), item.text(1)))
        self.device = item.text(0)
        name = getDevName(self.device)
        screen = getDecScreen(self.device)
        version = getVersion(self.device)
        msg = '设备名称：%s\n屏幕分辨率：%s\n系统版本：%s' % (name, screen, version)
        self.textBrowser.setText(msg)

    def reboot(self):
        if self.device == '':
            self.textBrowser.setText('未连接设备！')
            return
        self.textBrowser.setText('重启中。。。')
        self.thread = RunThread(self.device)
        self.thread.start()
        self.thread.trigger.connect(self.TimeStop)

    def choose(self):
        self.textBrowser.setText('')
        self.filename = QFileDialog.getOpenFileName(self, 'open file', '/')
        if self.filename[0]:
            if re.match('.*?apk', self.filename[0]):
                self.lineEdit.setText(self.filename[0])
            else:
                # self.filename[0] = ''
                self.textBrowser.setText('请选择正确的安装包！')


    def install(self):
        if not self.filename:
            installapp(self.filename[0])
        else:
            self.textBrowser.setText('请选择安装包！')

    def TimeStop(self):
        self.textBrowser.setText('重启完成！')


    def screencap(self):
        screencap()
        self.textBrowser.setText('截图成功！')

    def log(self):
        pass

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
            time.sleep(2)
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


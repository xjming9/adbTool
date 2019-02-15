from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.t = 0

        window = QWidget()
        vbox = QVBoxLayout(window)
        # vbox = QVBoxLayout(window)

        self.lcdNumber = QLCDNumber()
        button = QPushButton("测试")
        vbox.addWidget(self.lcdNumber)
        vbox.addWidget(button)

        self.timer = QTimer()

        button.clicked.connect(self.Work)
        self.timer.timeout.connect(self.CountTime)

        self.setLayout(vbox)
        self.show()

    def CountTime(self):
        self.t += 1
        self.lcdNumber.display(self.t)

    def Work(self):
        self.timer.start(1000)
        self.thread = RunThread()
        self.thread.start()
        self.thread.trigger.connect(self.TimeStop)

    def TimeStop(self):
        self.timer.stop()
        print("运行结束用时", self.lcdNumber.value())
        self.t = 0


class RunThread(QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    # _signal = pyqtSignal(str)

    trigger = pyqtSignal()

    def __init__(self, parent=None):
        super(RunThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # 处理你要做的业务逻辑，这里是通过一个回调来处理数据，这里的逻辑处理写自己的方法
        # wechat.start_auto(self.callback)
        # self._signal.emit(msg);  可以在这里写信号焕发
        for i in range(203300030):
            pass
        self.trigger.emit()
        # self._signal.emit(msg)

    def callback(self, msg):
        # 信号焕发，我是通过我封装类的回调来发起的
        # self._signal.emit(msg)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    th = Example()
    sys.exit(app.exec_())
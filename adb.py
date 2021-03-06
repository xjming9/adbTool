#-*-coding:utf-8 -*-
import subprocess, time
def getDevicesInfo():
    out = subprocess.Popen('adb devices',shell=True,stdout=subprocess.PIPE)
    deviceslist = out.stdout.read().splitlines()
    serial_nos = []
    if len(deviceslist) > 2:
        for item in deviceslist:
            if 'List' in item.decode('utf-8'):
                continue
            elif 'no permissions' in item.decode('utf-8'):
                continue
            elif item.decode('utf-8').strip() == '':
                continue
            else:
                serial_nos.append(item.decode('utf-8').split()[0])
                pass
            pass
        return serial_nos
    else:
        return -1


def getDevName(device):
    cmd = "adb -s %s shell getprop ro.product.model" % device
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    name = out.stdout.read().splitlines()
    return name[0].decode('utf-8')

def getDecScreen(device):
    cmd = "adb -s %s shell wm size" % device
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    screen = out.stdout.read().splitlines()
    return screen[0].decode('utf-8').split(':')[1].strip()

def getVersion(device):
    cmd = "adb -s %s shell getprop ro.build.version.release" % device
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    version = out.stdout.read().splitlines()
    return version[0].decode('utf-8')


def getip(device):
    #cmd = "adb -s %s shell ifconfig | grep Mask" % device
    #out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #ip = out.stdout.read().splitlines()
    #return ip[0].decode('utf-8')
    return '该功能调试中。。。'

def devReboot(device):
    cmd = "adb -s %s reboot" % device
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def installapp(device, path):
    cmd = "adb -s %s install %s" % (device, path)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def lightscreen(device):
    cmd = "adb -s %s shell input keyevent 26" % device
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def unlock(device):
    cmd = "adb -s %s shell input keyevent 26" % device
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(1)
    cmd = "adb -s %s shell input swipe 300 1000 300 500" % device
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def log(device, path):
    cmd = "adb -s %s logcat> %s" % (device, path)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def screenrecord(device):
    cmd = "adb -s %s shell screenrecord /sdcard/filename.mp4" % device
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def screencap(device, filename, path):
    cmd = "adb -s %s shell screencap -p /sdcard/%s.png" % (device, filename)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(4)
    cmd = "adb -s %s pull /sdcard/%s.png %s" % (device, filename, path)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def getPid(device,process):
    cmd = "adb -s %s shell ps | grep %s"%(device,process)
    out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    print(infos)
    pidlist = []
    if len(infos) >= 1:
        for i in infos:
            pid = i.split()[1]
            if pid not in pidlist:
                pidlist.append(pid)
        return pidlist
    else:
        return -1

def stopMonkey(devices):
    if (devices):
        pidList = getPid(devices,'monkey')
        if (pidList == -1):
            pass
        else:
            for index in range(len(pidList)):
                try:
                    cmd = 'adb -s %s shell kill %s'%(devices,pidList[index])
                    subprocess.Popen(cmd,shell=True)
                    pass
                except:
                    pass
            pass
        pass
    pass

if __name__=='__main__':
    installapp('95dfacd9', r'D:\python\appium\app\baidu_43013504.apk')

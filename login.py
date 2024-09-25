import sys,cv2
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QApplication as app
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic

class MyMainWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.ui_init()
        self.ui.show()

    def ui_init(self):
        self.ui=uic.loadUi('./login.ui')
        self.ui.resize(800,500)
        self.ui.setWindowIcon(QIcon('./images/logo.ico'))
        self.ui.input_name.setPlaceholderText('请输入用户名')
        self.ui.input_password.setPlaceholderText('请输入密码')
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_quit.clicked.connect(self.exit)

    def login(self):
        name=self.ui.input_name.text()
        password=self.ui.input_password.text()
        # if name=='wenshijian' and password=='3.14wen':
        #     self.ui.display_text.setText('成功登录，欢迎用户'+name+',即将获取视频')
        #     self.ui.display_text.repaint()
        #     self.ShowWindow=FunctionWindow()
        #     self.ShowWindow.ui.show()
        #     self.ui.close()
        # else:
        #     self.ui.display_text.setText('未找到用户')
        #     self.ui.display_text.repaint()
        self.ui.display_text.setText('成功登录，欢迎用户'+name+',即将获取视频')
        self.ui.display_text.repaint()
        self.ShowWindow=FunctionWindow()
       
        self.ui.close()

    def exit(self):
        sys.exit()

class FunctionWindow(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__()
        self.timer_camera=QtCore.QTimer()
        self.timer_camera.timeout.connect(self.display)
        self.ui_init()
        self.ui.show()

    def ui_init(self):
        self.ui=uic.loadUi('./Show.ui')
        self.ui.resize(800,500)
        self.ui.setWindowIcon(QIcon('./images/logo.ico'))
        self.ui.videos.setStyleSheet('border:5px dashed #D7E2F9;')
        self.ui.button_quit.clicked.connect(self.exit)
        self.ui.button_display.clicked.connect(self.start)
        self.ui.button_pause.clicked.connect(self.pause)

    def start(self):
        self.cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        if not self.cap:
            self.ui.setWindowTitle('摄像头打开失败')
            return
        if self.timer_camera.isActive() == False:
            self.timer_camera.start(50)

    def display(self):
        #ret为标志位，获取到图像帧则为True
        ret,frame=self.cap.read()
        if not ret:
            return
        frame=cv2.resize(frame,(400,400))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image=QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],
                                 QtGui.QImage.Format_RGB888)
        image=QtGui.QPixmap.fromImage(image)
        self.ui.videos.setPixmap(image)

    def pause(self):
        #关闭定时器
        self.timer_camera.stop()
        #释放摄像头资源
        self.cap.release()
        self.ui.button_display.setText('Continue')
        
          

    def exit(self):
        sys.exit() 

if __name__=='__main__':
    login_app=app(sys.argv)
    MainWindow=MyMainWindow()
    
    login_app.exec()
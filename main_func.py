import sys
import cv2 as cv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from blink_detection import Ui_MainWindow
from lib.fps import fps
import lib.imgConvert as imCv
import face_recognition
import matplotlib.pyplot as plt

from lib.utils.inference import detect_faces
from lib.utils.inference import load_detection_model
from scipy.signal import savgol_filter
import lib.EAR as EAR
from time import *
import os

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.count = 0

        self.camera = cv.VideoCapture(0)
        self.is_camera_opened = False  # 摄像头有没有打开标记

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)
        self.EAR_object = EAR.EAR_squence(windowLen=7,EAR_threshold = 1.2)  #存储EAR序列
        self.fps_counter = fps()             #显示fps的组件
        detection_model_path = 'trained_models/detection_models/haarcascade_frontalface_default.xml'
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.face_detection = load_detection_model(detection_model_path)   #加载检测器
        self.time_flag=0;

    def open_cama_click(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.open_camera.setText("关闭摄像头")
            self._timer.start()
        else:
            self.open_camera.setText("打开摄像头")
            self._timer.stop()

    def start_dete_click(self):
        '''
        开始检测
        '''
        # 摄像头未打开，不执行任何操作
        if not self.is_camera_opened:
            return
        
        if not self.time_flag:
            self.begin_time=time();
            self.time_flag=1;



    def exit_button_click(self):
        # self.camera.release()
        # sys.exit()
        self.time_flag=0
        self._timer.stop()
        self.camera.release()
        cv.destroyAllWindows()
        self.close()
        #os._exit(5)
        #sys.exit()
        # self.vc.release()
        # self.openCameraBtn.setEnabled(True)
        # self.closeCameraBtn.setEnabled(False)
        # self.QLable_close()
        # self.timer.stop()
        




    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片
        '''
        ret, self.frame = self.camera.read()

        if self.time_flag:
            self.captured = self.frame
    
            bgr_image = cv.flip(self.captured,1,dst=None)
            width = bgr_image.shape[1]     #求取缩放系数
            k = width/320
            
            raw_resolution = bgr_image        #原始分辨率的图片，用于做人脸解析
            bgr_image = cv.resize(bgr_image, (320,180))    #注意这边长宽的缩放系数q要组合成元组
            gray_image = cv.cvtColor(bgr_image, cv.COLOR_BGR2GRAY)   #转换为灰度图做人脸检测
            faces = detect_faces(self.face_detection, gray_image)         #检测人脸
            self.fps_counter.fps_count()   #计算时间Q
            
            Leye_loc = []
            Reye_loc = []
              
            for face_coordinates in faces:
                x,y,w,h = face_coordinates
                x = int(x*k*0.9)                              #坐标变换
                y = int(y*k)
                
                w = int(w*k*1.2)
                h = int(h*k*1.7)
                
                bgr_face = raw_resolution[y:y+h,x:x+w]     #取脸部的区域
            
                ROIformarking = imCv.cvToPIL(bgr_face)  #转换成PIL包的图片格式去做特征点识别
                landmarks=face_recognition.api.face_landmarks(ROIformarking)  #获取所有特征点
                for i in range(len(landmarks)):
                    for key, value in landmarks[i].items():
                        for j in range(len(value)):
                            cv.circle(bgr_face,(value[j][0],value[j][1]),2,(0,0,255),-1)
                            
                    Leye_loc = landmarks[0].get("left_eye",[])    #获取左眼坐标
                    Reye_loc = landmarks[0].get("right_eye",[])   #获取右眼坐标
                #cv2.imshow('raw resolution face',bgr_face)
                #cv2.waitKey(1)
            
            self.EAR_object.updateVaule(Leye_loc,Reye_loc)
            if(self.count != self.EAR_object.blink_count):
                #print("blink detected：")
                #print(self.EAR_object.blink_count)
                self.count = self.EAR_object.blink_count
            self.end_time=time()
            run_time=self.end_time-self.begin_time
            if not self.end_time==self.begin_time:
                freq=self.count/run_time
                self.lineEdit_2.setText(str(round(60*freq)))
                self.lineEdit_3.setText(str(round(run_time)))
                if (freq*60)<8:
                    self.data_out.setStyleSheet("background-color:red")
                    self.data_out.setText("眨眼频率过低，容易引起干涩，注意休息")
                elif (freq*60)<=18:
                    self.data_out.setStyleSheet("background-color:green")
                    self.data_out.setText("正常")
                else :
                    self.data_out.setStyleSheet("background-color:red")
                    self.data_out.setText("眨眼频率过高，注意休息")
                
            self.lineEdit.setText(str(self.count))
            
            
        
        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv.cvtColor(self.frame, cv.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.camera_out.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.camera_out.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
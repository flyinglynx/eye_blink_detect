import cv2
from lib.fps import fps
import lib.imgConvert as imCv
import face_recognition
import matplotlib.pyplot as plt

from lib.utils.inference import detect_faces
from lib.utils.inference import load_detection_model
from scipy.signal import savgol_filter
import lib.EAR as EAR

detection_model_path = 'trained_models/detection_models/haarcascade_frontalface_default.xml'
font = cv2.FONT_HERSHEY_SIMPLEX
face_detection = load_detection_model(detection_model_path)   #加载检测器

cap = cv2.VideoCapture(0) #创建一个 VideoCapture 对象 

fps_counter = fps()             #显示fps的组件
EAR_object = EAR.EAR_squence(windowLen=7,EAR_threshold = 1.2)  #存储EAR序列
count = 0

while(cap.isOpened()):          #循环读取每一帧
    bgr_image = cap.read()[1]
    bgr_image = cv2.flip(bgr_image,1,dst=None)
    width = bgr_image.shape[1]     #求取缩放系数
    k = width/320
    
    raw_resolution = bgr_image        #原始分辨率的图片，用于做人脸解析
    bgr_image = cv2.resize(bgr_image, (320,180))    #注意这边长宽的缩放系数q要组合成元组
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)   #转换为灰度图做人脸检测
    faces = detect_faces(face_detection, gray_image)         #检测人脸
    fps_counter.fps_count()   #计算时间Q
    
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
                    cv2.circle(bgr_face,(value[j][0],value[j][1]),2,(0,0,255),-1)
                    
            Leye_loc = landmarks[0].get("left_eye",[])    #获取左眼坐标
            Reye_loc = landmarks[0].get("right_eye",[])   #获取右眼坐标
        cv2.imshow('raw resolution face',bgr_face)
        cv2.waitKey(1)

    EAR_object.updateVaule(Leye_loc,Reye_loc)
    if(count != EAR_object.blink_count):
        print("blink detected：")
        print(EAR_object.blink_count)
        count = EAR_object.blink_count
    fps_counter.fps_print(160,30,bgr_image)
    cv2.imshow('detection result', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ax = range(1,EAR_object.frames+1)
ay = [a[0]+a[1] for a in zip(EAR_object.squenceL,EAR_object.squenceR)]
y1 = savgol_filter(ay, 15, 3)
y2 = EAR.proportionFilter(ay,threshold=0.1)
y3 = savgol_filter(y2, 7, 2)


img=plt.subplot(3,1,1)
img.set_title('EAR value')      #添加子标题
img.set_ylabel('realtime', fontsize=10)
img.plot(range(1,len(EAR_object.filtered)+1),EAR_object.filtered,'g-')
 
img3=plt.subplot(3,1,2)
img3.set_xlabel('frames',fontsize=10)   #添加轴标签
img3.set_ylabel('whole', fontsize=10)
img3.plot(ax,y3,'g-')

img2=plt.subplot(3,1,3)
#img2.set_xlabel('frames',fontsize=10)   #添加轴标签
img2.set_ylabel('raw', fontsize=10)
img2.plot(ax,ay,'g-')                 

cap.release() #释放摄像头
cv2.destroyAllWindows()#删除建立的全部窗口

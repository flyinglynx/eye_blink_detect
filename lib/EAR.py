import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

class EAR_squence():
    def __init__(self,name='tester',windowLen = 9,EAR_threshold = 1.15):
        self.name = name    #为后续可能加入的人脸识别功能准备
        self.frames=0       #目前已经跑的帧数
        self.squenceL = []  #EAR算法结果的序列(左眼)
        self.squenceR = []  #EAR算法结果的序列(右眼)
        self.sum = []       #左右眼的结果之和
        self.filtered = []  #实时滤波得到的结果序列
        self.EAR_threshold = EAR_threshold
        self.windowLen = windowLen #实时滤波的窗口长度
        self.blink_count = 0     #眨眼次数统计
        self.lastBlinkFrame = -100   #上次眨眼的帧位置，避免在较平滑的区域重复统计


    #给出左右眼特征点坐标，更新对象的实例域
    def updateVaule(self,Leye,Reye):
        LEAR = 0
        REAR = 0
        if(len(Leye)):
            LEAR = get_EAR_value(Leye)
        else:
            try:
                LEAR = self.squenceL[-1]
            except:
                LEAR = 0
                
        if(len(Reye)):
            REAR = get_EAR_value(Reye)
        else:
            try:
                REAR = self.squenceR[-1]
            except:
                REAR = 0
        self.frames += 1
        self.squenceL.append(LEAR)  #左眼EAR序列追加
        self.squenceR.append(REAR)  #右眼EAR值序列追加
        self.sum.append(LEAR+REAR)  #求和
        self.realtimeFilter()       #实时对一段窗口进行滤波
        self.blinkJudge()           #判断是否眨眼

        return LEAR,REAR
    #对持续获得的序列进行滤波
    def realtimeFilter(self):
        if(self.frames%self.windowLen==0): #需要做一批滤波
            temp = proportionFilter(self.sum[self.frames-self.windowLen:self.frames],0.1)
            temp = savgol_filter(temp, self.windowLen, 5) #该窗口内滤波结果并入滤波后序列
            self.filtered.extend(list(temp))
        else:
            return

    #检测该区间内是否有一次眨眼
    def blinkJudge(self):
        if(self.frames%self.windowLen==0): #以窗口长度为单位批量处理
            temp = self.filtered[self.frames-self.windowLen:self.frames] #从滤波结果中取出一段
            for value in temp:
                if (value < self.EAR_threshold) and (self.frames-self.lastBlinkFrame>10):
                    self.blink_count += 1
                    self.lastBlinkFrame = self.frames
                else:
                    continue
        else:
            return

                  
#计算A,B两点之间的距离
def distance(A,B): 
    return ((A[0]-B[0])**2+(A[1]-B[1])**2)**0.5

#给出眼部5点坐标后，得到EAR算法的值
def get_EAR_value(landmarks):
    a = 2*(distance(landmarks[1],landmarks[5])+distance(landmarks[2],landmarks[4])) #分子
    b = distance(landmarks[0],landmarks[3])
    return a/b

#对给出的整个序列滤去噪声
def proportionFilter(squence,threshold=0.3):
    result = []
    result.append(squence[0])
    for i in range(1,len(squence)):
        if(squence[i-1]==0):   #若前一元素为0
            result.append(0)
            continue

        if abs((squence[i]-squence[i-1]))/squence[i-1] < threshold: #变化不大，直接采用前一次的值
            result.append(result[i-1])
        
        else:
            result.append(squence[i])
    
    return result

#两级串联的滤波器
def cascadeFilter(squence,windowsize,order,threshold = 0.3):
    y1 = savgol_filter(squence, windowsize, order)
    y1 = proportionFilter(y1,threshold=0.1)
    return y1
import time
import cv2

class fps():
    def __init__(self):
        self.cur_time = 0.0
        self.int_time = 0.0

        self.count = 0
        self.staticCount = 0
    def fps_count(self):
        self.cur_time = time.clock()
        if self.cur_time - self.int_time > 1:
            self.int_time = self.cur_time
            self.staticCount = self.count
            self.count = 0
            return self.staticCount
        
        else :
            self.count += 1
            return -1

    def fps_print(self,x,y,img):
        
         cv2.putText(img, str(self.staticCount),(x,y),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0, 255, 0), 1, cv2.LINE_AA)
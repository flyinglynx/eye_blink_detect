from PIL import Image
import cv2
import numpy as np
'''
将openCV图像转换为PIL包对应的图像
'''
def cvToPIL(ori_img,mode='RGB'): 
    img = ori_img.copy()
    image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)) 
    if(mode):
        image = image.convert(mode)
    return np.array(image)


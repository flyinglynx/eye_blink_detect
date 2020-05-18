# eye_blink_detect
   Detect eye blink using face detection and face-alignment.

# face detection module
harr cascaded face detector from OpenCV

# face alignment module 
Face alignment module is taken from https://github.com/ageitgey/face_recognition

# Requirements
opencv-python
pytorch
tensorflow   
keras   
sci-py   
face_recognition (can be a bit hard to install,instructions can be found here https://github.com/ageitgey/face_recognition)
# How it works?
   First we compress the frame into a low resolution one, on which we run the face  
detection algorithm. According to the result, we locate the ROI which contain the  
faces in the high resolution image.  
   Running algorithm on the high resolution image can acquire relatively accurate   
coordinates of landmarks. By analyze the change of these coordinates, we can tell   
when a blink occurs.  

# demo
run main_func.py (no arguments)  
 

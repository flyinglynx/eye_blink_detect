# eye_blink_detect
p-> Detect eye blink using face detection and face-alignment.

# face detection module
The face detection module is taken from https://github.com/oarriaga/face_classification

# face alignment module 
Face alignment module is taken from https://github.com/ageitgey/face_recognition

# Requirements
opencv-python   
tensorflow   
keras   
sci-py   
face_recognition (a bit hard to install,instructions here https://github.com/ageitgey/face_recognition)
# How it works?
First we compress the frame into a low resolution one, on which we run the face  
detection algorithm. According to the result, we locate the ROI which contain the  
faces in the high resolution image.  
Running algorithm on the high resolution image can acquire relatively accurate   
coordinates of landmarks. By analyze the change of these coordinates, we can tell   
when a blink occurs.  

# demo
run webcam_demo.py (no arguments)  
the threshold for different people can be quite different, you can change the threshold  
by modify the EAR_threshold in line19(webcam_demo.py)  

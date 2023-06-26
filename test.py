import sys
import cv2

cap = cv2.VideoCapture(0) # 0: 메인 카메라

if not cap.isOpened():
    print("camera open failed")
    sys.exit()
    
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)    
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)    
fps = cap.get(cv2.CAP_PROP_FPS) # frame per second
delay = round(1000/30)

print(width, height, fps, delay)

while True:    
    ret, frame = cap.read() # frame : 이미지 한장 (shape : height x width x channel)        
    
    if not ret:
        print("frame read error")
        break
    cv2.imshow('camera', frame) # 재생    
       
    key = cv2.waitKey(delay) # delay(ms) 기다리기(sleep 효과)
    if key == 27: # 27 : Esc key,  종료조건    
        break

if cap.isOpened(): # True
    print('cap release!!')
    cap.release()
    
cv2.destroyAllWindows()
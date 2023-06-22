import cv2

video = cv2.VideoCapture('http://192.168.0.100:4747/mjpegfeed')
frame_size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(video.CAP_PROP_FRAME_HEIGHT)))

while True:
    ret, frame = video.read()
    if not ret:
        break
        
    cv2.imshow('frame', frame)
    
    # Press 'Esc' to stop
    key = cv2.waitKey(25)
    if key == 27:				
        break
        
if video.isOpened():
    video.release()
    
cv2.destroyAllWindows()
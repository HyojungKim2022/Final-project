import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse

from .make_prediction import make_predict, get_bndbox, calculate_price


global result

def show_strat_page(request):
    return render(request, 'BLC/start.html')

def webcam_stream():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        result = make_predict(frame)
        res_frame = get_bndbox(frame, result)

        # 3. 두 번째 단계의 결과로 나온 비디오를 video_start.html에 반환
        _, img_encoded = cv2.imencode('.jpg', res_frame)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n\r\n')
    
    cap.release()

def video_start(request):
    return StreamingHttpResponse(webcam_stream(), content_type='multipart/x-mixed-replace; boundary=frame', context=context)

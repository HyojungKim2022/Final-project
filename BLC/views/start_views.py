import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse

from .make_prediction import make_predict, get_bndbox, calculate_price

def show_start_page(request):
    return render(request, 'BLC/start.html')

def webcam_stream():
    cap = cv2.VideoCapture(0)
    prev_frame = None  # 이전 프레임을 저장하는 변수 초기화
    prev_price = None  # 이전 가격을 저장하는 변수 초기화
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        result = make_predict(frame)
        res_frame = get_bndbox(frame, result)
        price = calculate_price(result)
        
        # 현재 프레임과 가격이 이전과 다를 경우에만 HTML에 가격 전달
        if prev_frame is not None and prev_price is not None:
            if not (frame == prev_frame).all() or price != prev_price:
                _, img_encoded = cv2.imencode('.jpg', res_frame)
                img_bytes = img_encoded.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n\r\n', price)
        else:
            _, img_encoded = cv2.imencode('.jpg', res_frame)
            img_bytes = img_encoded.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n\r\n', price)
            
        prev_frame = frame
        prev_price = price
    
    cap.release()

def video_start(request):
    return StreamingHttpResponse(webcam_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def start_page(request):
    context = {
        'res_value': request.GET.get('price')
    }
    return render(request, 'BLC/start.html', context=context)
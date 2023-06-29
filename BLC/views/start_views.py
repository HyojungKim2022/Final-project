import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

import json
from mmdet.apis import init_detector
from .make_prediction import make_predict, get_bndbox, calculate_price


cfg = 'models/hj/epoh14/config_14.py'
ckpt = 'models/hj/epoh14/epoch_14 (2).pth'
score_thr = 0.2
model = init_detector(cfg, ckpt, device='cuda:0')

price_dict = json.load(open('price_4.json', encoding='UTF8'))
total_amount = 0
each_amount = {}

def show_start_page(request):
    return render(request, 'BLC/start.html')

def webcam_stream(request):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break

        result = make_predict(model, frame, score_thr)
        res_frame = get_bndbox(frame, result)
        global total_amount, each_amount
        total_amount, each_amount = calculate_price(result, price_dict)

        _, img_encoded = cv2.imencode('.jpg', res_frame)
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n\r\n')

    cap.release()

def get_amount(request):
    global total_amount, each_amount
    data = {
        'total_amount': total_amount,
        'each_amount': each_amount
    }
    return JsonResponse(data)

def video_start(request):
    return StreamingHttpResponse(webcam_stream(request), content_type='multipart/x-mixed-replace; boundary=frame')

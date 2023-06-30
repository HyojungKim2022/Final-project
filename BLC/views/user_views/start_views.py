import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

import json
from .make_prediction import make_predict, get_bndbox, calculate_price
from ..model_init import init_model

score_thr = 0.6

model = init_model()

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

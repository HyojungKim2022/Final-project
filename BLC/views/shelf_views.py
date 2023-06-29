import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse
import time

import json
from mmdet.apis import init_detector
from .make_grid_prediction import draw_grid_line, make_grid_predict, make_grid_frame

cfg = 'models/hj/epoh14/config_14.py'
ckpt = 'models/hj/epoh14/epoch_14 (2).pth'
score_thr = 0.6
model = init_detector(cfg, ckpt, device='cuda:0')

grid_x = 2
grid_y = 1

def show_shelf_page(request):
    return render(request, 'BLC/shelf.html')

def grid_webcam_stream(request):
    cap = cv2.VideoCapture(0)
    delay_time = 2.0  # 2초 지연
    frame_rate = 10  # 10fps 프레임 속도
    frame_delay = 1 / frame_rate  # 프레임 간 지연 시간 계산
    frame_counter = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        current_time = time.time()

        if current_time - start_time >= delay_time:
            start_time = current_time

            if frame_counter % frame_rate == 0:
                grid_frames = make_grid_frame(frame, grid_x, grid_y)
                results = []

                for grid_frame in grid_frames:
                    res = make_grid_predict(model, grid_frame, score_thr)
                    results.append(res)

                # 한 프레임당 하나의 이미지가 들어왔다 가정
                res_frame = draw_grid_line(frame, grid_x, grid_y)

                _, img_encoded = cv2.imencode('.jpg', res_frame)

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n\r\n')

                del results

            frame_counter += 1

        time.sleep(frame_delay)

    cap.release()

def grid_video_start(request):
    return StreamingHttpResponse(grid_webcam_stream(request), content_type='multipart/x-mixed-replace; boundary=frame')

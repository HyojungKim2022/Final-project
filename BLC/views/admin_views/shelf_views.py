import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

from .make_grid_prediction import make_grid_predict
from ..model_init import init_model

score_thr = 0.9
model = init_model()

grid_x = 3
grid_y = 2

global shelf_no
shelf_no='B'

def init_shelf_no(request):
    if request.method == "GET":
        input_shelf_no = request.GET.get('shelf_no')
        global shelf_no
        shelf_no = input_shelf_no
    
    return JsonResponse({'status':'success'})

def show_shelf_page(request):
    return render(request, 'admin/shelf.html')

path = 'C:/Users/thffh/Documents/project/final/test/IMG_1873.mov'
def grid_webcam_stream(request):
    'cap = cv2.VideoCapture(0)'
    cap = cv2.VideoCapture(path, apiPreference=None)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
    
        result = make_grid_predict(model, frame, score_thr)
        frame = compare_with(frame, 3, 2, result)

        _, img_encoded = cv2.imencode('.jpg', frame)
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n\r\n')
        

    cap.release()

def grid_video_start(request):
    return StreamingHttpResponse(grid_webcam_stream(request), content_type='multipart/x-mixed-replace; boundary=frame')


from BLC.models import Stock, Items

# x그리드 y그리드
def compare_with(frame, grid_x, grid_y, results):
    shelf_dicts = {}
    sample_h, sample_w, _ = frame.shape
    grid_line_y = sample_h // grid_y
    grid_line_x = sample_w // grid_x

    for result in results:
        item = list(result.items())[0]
        id = item[0]
        # name = item[0]

        # items = Items.objects.get(item_name=name)
        items = Items.objects.get(item_id=id)

        x, y, x_max, y_max = list(map(int, item[1]))

        for idx, grid_x_cord in enumerate(range(0, sample_w+1, grid_line_x)):
            if x_max <= grid_x_cord:
                # idx -> 같은 층일 때 상품 정렬 순서
                item_order = idx       
                break
                
        for idx, grid_y_cord in enumerate(range(0, sample_h+1, grid_line_y)):
            if y_max <= grid_y_cord:        
                if idx not in shelf_dicts.keys():
                    # idx -> 층 나누기
                    shelf_floor = idx
                break

        # 예측값 floor->위에서부터 1, item_order->왼쪽부터 1
        shelf_item = Stock.objects.filter(shelf_no=shelf_no, shelf_floor=shelf_floor, item_order=item_order).values('item').first()
        if shelf_item:
            if shelf_item['item'] == items.item_id:
                color = [0,255,0]
            else:
                color = [0,0,255]
        
            frame = cv2.rectangle(frame, (x, y), (x_max, y_max), color, 5)
        
    return frame

from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from BLC.models import Sales, DetailSale, Items, Store, Stock

import cv2
import datetime
from .make_prediction2 import make_predict, draw_bndbox, calculate_price
from ..model_init import init_model


score_thr_low = 0.65
score_thr_high = 0.90
model = init_model()

total_amount = 0
each_amount = {}

def show_start_page(request):
    return render(request, 'BLC/start.html')


global boolean_pause
boolean_pause = False

@csrf_exempt
def pause_video(request):
    global boolean_pause
    data = request.GET.get('data')
    if data == '0':
        boolean_pause = True
    else:
        boolean_pause = False
    return JsonResponse({'status':'success'})

# 테스트용 비디오
path = 'C:/Users/thffh/Downloads/videos/400/video_08.mov'

def webcam_stream(request):
    global boolean_pause
    global prev_ret, prev_frame
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(path, apiPreference=None)

    while True:
        # True : 결제하기 눌렀을때
        if boolean_pause:
            ret, frame = prev_ret, prev_frame
        # 기본 or 취소하기
        else:
            ret, frame = cap.read()
            prev_ret, prev_frame = ret, frame

        if not ret:
            break
        
        frame = cv2.resize(frame, (1333, 800))
        # 모델 예측
        result = make_predict(model, frame, score_thr_low, score_thr_high)
        
        # 인식 테스트를 위한 bnd 박스 그리기
        frame = draw_bndbox(frame, result, score_thr_high)

        # 가격 db로부터 가져오기
        global total_amount, each_amount
        total_amount, each_amount = calculate_price(result, score_thr_high)

        _, img_encoded = cv2.imencode('.jpg', frame)
        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img_encoded.tobytes() + b'\r\n\r\n')

    cap.release()


# calculate_price로부터 계산된 값을 json형식으로 return
def get_amount(request):
    global total_amount, each_amount
    data = {
        'total_amount': total_amount,
        'each_amount': each_amount
    }
    return JsonResponse(data)

# 비디오 출력
def video_start(request):
    return StreamingHttpResponse(webcam_stream(request), content_type='multipart/x-mixed-replace; boundary=frame')



# 결제 버튼 클릭시 결제 정보 sales 및 detail_sale db에 저장
# 결제 완료 출력 시 stock db 변경
@csrf_exempt
def process_payment(request):
    # Sales 데이터베이스에 결제 정보 저장
    # store_id = request.POST.get('store')
    store_id = 1
    store = Store.objects.get(pk=store_id)
    sale_date = datetime.date.today()  # 오늘 날짜
    total_price = total_amount
    sale = Sales.objects.create(store=store, sale_date=sale_date, total_price=total_price)
     
    # DetailSale 데이터베이스에 상품 정보 저장
    for item_name, (price, quantity) in each_amount.items():
        item = Items.objects.get(item_name=item_name)
        unit_price = price
        DetailSale.objects.create(sale=sale, item=item, quantity=quantity, unit_price=unit_price)

    # 재고 데이터베이스 업데이트
    for item_name, (price, quantity) in each_amount.items():
        item = Items.objects.get(item_name=item_name)
        stock = Stock.objects.get(item=item)
        stock.quantity -= quantity  # 기존 재고에서 사용한 수량 차감
        stock.save()

    return JsonResponse({'message': '결제가 완료되었습니다.'})
import cv2
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

from .make_prediction import make_predict, get_bndbox, calculate_price
from ..model_init import init_model


score_thr = 0.9
model = init_model()

total_amount = 0
each_amount = {}

def show_start_page(request):
    return render(request, 'BLC/start.html')

path = 'C:/Users/thffh/Documents/project/final/test/IMG_1873.mov'
def webcam_stream(request):
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(path, apiPreference=None)

    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
    
        result = make_predict(model, frame, score_thr)
        
        # 인식 테스트를 위한 bnd 박스 그리기
        # total_amount, each_amount = calculate_price(result, price_dict)
        global total_amount, each_amount
        total_amount, each_amount = calculate_price(result)

        _, img_encoded = cv2.imencode('.jpg', frame)
        
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



# 결제 버튼 클릭시 결제 정보 sales 및 detail_sale db에 저장
# 결제 완료 출력 시 stock db 변경
from BLC.models import Sales, DetailSale, Items, Store, Stock
import datetime
from django.views.decorators.csrf import csrf_exempt

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
        unit_price = price * quantity
        DetailSale.objects.create(sale=sale, item=item, quantity=quantity, unit_price=unit_price)


    # for item_id, (price, quantity) in each_amount.items():
    #     item = Items.objects.get(item_id=item_id)
    #     unit_price = price * quantity
    #     DetailSale.objects.create(sale=sale, item=item, quantity=quantity, unit_price=unit_price)


    # 재고 데이터베이스 업데이트
    for item_name, (price, quantity) in each_amount.items():
        item = Items.objects.get(item_name=item_name)
        stock = Stock.objects.get(item=item)
        stock.quantity -= quantity  # 기존 재고에서 사용한 수량 차감
        stock.save()

    return JsonResponse({'message': '결제가 완료되었습니다.'})
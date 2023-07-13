import cv2
from mmdet.apis import inference_detector
from BLC.models import Items


# 모델 실행 함수
# high_thr와 low_thr을 입력받아 탐지된 객체 분류
def make_predict(model, frame, score_thr_low, score_thr_high):
    results = inference_detector(model, frame)
    
    res = {'high':[], 'low':[]}
    
    for idx, boxes in enumerate(results):
        if boxes.any():
            class_name = model.CLASSES[idx]
            for box in boxes:
                box_ = list(map(int, box[:4]))
                box_.append(box[-1])
                obj_info = {class_name: box_}

                if box[-1] >= score_thr_high:
                    res['high'].append(obj_info)
                elif box[-1] > score_thr_low:
                    res['low'].append(obj_info)

    
    if res['low']:
        remove_list=[]
        for i, low_res in enumerate(res['low']):
            key, value = list(low_res.items())[0]
            x_min, y_min, x_max, y_max, score = list(map(int,value))
            
            if res['high']:
                for high_res in res['high']:
                    key, value = list(high_res.items())[0]
                    x_min_h, y_min_h, x_max_h, y_max_h, score_h = list(map(int,value))

                    overlap_x = min(abs(x_max-x_min_h), abs(x_max_h-x_min))
                    overlap_y = min(abs(y_max-y_min_h), abs(y_max_h-y_min))
                    
                    h_width = (x_max_h - x_min_h)
                    h_height = (y_max_h - y_min_h)

                    if overlap_x * overlap_y > h_width * h_height * 0.5:
                        remove_list.append(i) 

        if remove_list:       
            for i in range(len(res['low']) - 1, -1, -1):
                if i not in remove_list:
                    continue
                res['low'].pop(i)
    
    res = res['high']+res['low']
    return res


# frame과 결과딕셔너리 리스트({name:[bndbox, score]}), high_thr을 입력받아 보다 낮은 객체는 빨간색, 아니면 초록색으로 표시 
def draw_bndbox(frame, res_dicts, score_thr_high):
    for res_dict in res_dicts:
        key, value = list(res_dict.items())[0]
        if value[-1] < score_thr_high:
            color = [0,0,255]
        else:
            color = [0,255,0]
        cv2.rectangle(frame, (value[0], value[1]), (value[2],value[3]), color, thickness=1)
    return frame


# 결과딕셔너리 리스트({name:[bndbox, score]}), high_thr을 입력받아 보다 낮은 객체는 무시, 아니면 db로부터 색인하여 결과값 출력
def calculate_price(result_dict, score_thr_high):
    total_amount = 0
    each_amount = {}

    for result in result_dict:
        score = list(result.values())[0][-1]

        if score < score_thr_high:
            continue
        else:
            try:
                item_id = list(result.keys())[0]
                item = Items.objects.get(item_id=item_id)
                item_name = item.item_name
                price = item.price
                total_amount += price
                
                if item_name not in each_amount:
                    each_amount[item_name] = [price, 1]
                else:
                    each_amount[item_name][0] += price
                    each_amount[item_name][1] += 1

            except Items.DoesNotExist:
                continue

    return total_amount, each_amount

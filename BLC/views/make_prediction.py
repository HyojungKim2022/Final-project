from mmdet.apis import inference_detector
import cv2

color_map = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255],]

def make_predict(model, frame, score_thr):
    result = inference_detector(model, frame)
    
    res_dict = [
        {model.CLASSES[idx]: box[:4]}
        for idx, boxes in enumerate(result)
        if boxes.any()
        for box in boxes
        if box[-1] > score_thr
    ]
    return res_dict

# def get_bndbox(frame, res_dict):   
#     frame_copy = frame.copy()
#     for res in res_dict:
#         name, bndbox = list(res.items())[0]
#         bndbox = list(map(int, bndbox))
#         frame_copy = cv2.rectangle(frame_copy, ((bndbox[0]), bndbox[1]), (bndbox[2], bndbox[3]), [0, 255, 0], 5)
#     return frame_copy

def get_bndbox(frame, res_dict):   
    frame_copy = frame.copy()
    for i, res in enumerate(res_dict):
        _, bndbox = list(res.items())[0]
        bndbox = list(map(int, bndbox))
        frame_copy = cv2.rectangle(frame_copy, ((bndbox[0]), bndbox[1]), (bndbox[2], bndbox[3]), color_map[i%6], 5)
    return frame_copy


def calculate_price(res_dict, price_dict):
    total_amount = 0
    each_amount = {}
    for item in res_dict:
        name, _ = list(item.items())[0]
        price = price_dict.get(name, 0)
        total_amount += price
        
        if name not in each_amount:
            each_amount[name] = [each_amount.get(name, 0) + price, 1]
        else:
            each_amount[name][1] += 1       
            each_amount[name][0] += price        
    return total_amount, each_amount
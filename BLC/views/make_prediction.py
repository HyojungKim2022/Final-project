from mmdet.apis import init_detector, inference_detector
import cv2
import json

cfg = 'models/config.py'
ckpt = 'models/epoch_15.pth'
score_thr = 0.2

price_dict = json.load(open('price_3.json', encoding='UTF8'))

def make_predict(frame):
    model = init_detector(cfg, ckpt, device='cuda:0')
    result = inference_detector(model, frame)
    
    res_dict = [
        {model.CLASSES[idx]: box[:4]}
        for idx, boxes in enumerate(result)
        if boxes.any()
        for box in boxes
        if box[-1] > score_thr
    ]
    return res_dict

def get_bndbox(frame, res_dict):   
    frame_copy = frame.copy()
    for res in res_dict:
        name, bndbox = list(res.items())[0]
        bndbox = list(map(int, bndbox))
        frame_copy = cv2.rectangle(frame_copy, ((bndbox[0]), bndbox[1]), (bndbox[2], bndbox[3]), [0, 255, 0], 5)
    return frame_copy


def calculate_price(res_dict):
    total_amount = 0
    each_amount = {}
    for item in res_dict:
        name, _ = list(item.items())[0]
        price = price_dict.get(name, 0)
        total_amount += price
        each_amount[name] = each_amount.get(name, 0) + price

    return total_amount, each_amount

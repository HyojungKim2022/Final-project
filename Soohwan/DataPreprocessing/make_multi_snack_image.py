"""
make a new image with two snacks
"""

import glob
import xml.etree.ElementTree as ET
import json
import cv2
import numpy as np
import random
from create_coco_format import *


def image_process(idx, xml_list, size, ratio):
    # 이미지 축소 비율을 담은 사전
    division = {1: 1, 2: 1.2, 3: 1.3, 4: 1.4, 5: 1.5, 6: 1.6, 7: 1.7, 8: 1.8, 9: 1.9}

    # 첫번째 이미지 처리
    tree = ET.parse(xml_list[idx])
    root = tree.getroot()
    annotation = root.find('annotation')
    name = annotation.find('.//name').text

    # xml 파일에서 원본 이미지에서 정보 추출
    img_name = annotation.find("filename").text
    img_height = int(annotation.find("size").find("height").text)
    img_width = int(annotation.find("size").find("width").text)

    obj = annotation.find('object')  # findall이 아닌 이유는 각 사진의 객체가 하나인 것만 이용함
    coords = obj.find('bndbox')
    x_min = int(coords.find('xmin').text)
    y_min = int(coords.find('ymin').text)
    x_max = int(coords.find('xmax').text)
    y_max = int(coords.find('ymax').text)
    width = abs(x_max - x_min)
    height = abs(y_max - y_min)

    # resize 이미지에 맞는 bbox 좌표 계산
    resize_x_min = x_min * size // img_width
    resize_y_min = y_min * size // img_height
    resize_width = width * size // img_width
    resize_height = height * size // img_height

    # img_paths[idx]와 xml_paths[idx]의 정렬 순서가 다름 -> sort()도 되지 않음
    img = cv2.imread("_image_for_make/" + img_name)
    img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
    bbox = img[resize_y_min: resize_y_min + resize_height, resize_x_min: resize_x_min + resize_width, ]
    bbox = cv2.resize(bbox, (int(resize_width // division[ratio]), int(resize_height // division[ratio])),
                      interpolation=cv2.INTER_AREA)
    area = bbox.shape[0] * bbox.shape[1]
    return bbox, name, area


def onChange(pos):
    pass


cv2.namedWindow("setting")
cv2.createTrackbar("ratio_1", "setting", 1, 9, onChange)
cv2.createTrackbar("ratio_2", "setting", 1, 9, onChange)
cv2.createTrackbar("point_x1", "setting", 0, 800, onChange)
cv2.createTrackbar("point_y1", "setting", 0, 800, onChange)
cv2.createTrackbar("point_x2", "setting", 0, 800, onChange)
cv2.createTrackbar("point_y2", "setting", 0, 800, onChange)

cv2.setTrackbarMin("ratio_1", "setting", 1)
cv2.setTrackbarMin("ratio_2", "setting", 1)

img_size = int(input("이미지의 사이즈를 입력하세요: "))
first_file_name = input("별칭을 입력하세요: ")

img_paths = glob.glob("_image_for_make/*")
xml_paths = glob.glob("_xml_for_make/*")

img_id = 0
obj_id = 0

total_image = []
total_annotation = []
backend_dict = {'65621': '마켓오리얼브라우니말차12개입',
                '50098': '롯데)제크찐치즈칩54G',
                '30152': '토하토)크레용신찬20G',
                '45219': '오리온)예감32G',
                '30064': '크라운)꽃게랑불짬뽕맛70G',
                '30166': '롯데)치토스후라이드_양념치킨맛80G',
                '50117': '크라운)콘칩(군옥수수)70G',
                '50062': '농심자갈치90G',
                '30120': '롯데)꼬깔콘매콤달콤72G',
                '20211': '크라운)카라멜메이플콘74G',
                '10178': '농심칩포테토오리지날125G',
                '45221': '오리온)예감볶은양파맛32G',
                '10092': '농심오징어집83G',
                '30061': '농심포스틱84G',
                '10091': '꼬깔콘고소한맛72G',
                '30119': '오뚜기뿌셔뿌셔불고기90G',
                '25679': '오리온후레쉬베리딸기336G',
                '30086': '해태)딸기웨하스Original50G',
                '50063': '도리토스갈비천왕치킨맛172G',
                '15033': '롯데ABC초코쿠키152G',
                '45222': '오리온)고소미35G',
                '65629': '마켓오리얼브라우니12개입',
                '65858': '오리온)크런치케이준눈을감자',
                '30066': '농심꿀꽈배기90G',
                '50061': '오리온스윙칩볶음고추장60G',
                '20164': '해태)허니버터칩38G',
                '10094': '크라운)콘초66G',
                '90078': '농심조청유과96G',
                '30140': '농심인디안밥83G',
                '15046': '동서리츠샌드위치크래커치즈96G',
                '45227': '롯데제과)꼬깔콘고소한맛42G',
                '30060': '농심벌집핏자90G',
                '15175': '미가방유한회사)오레오씬즈바닐라무스84G',
                '10093': '농심매운새우깡90G',
                '65723': '롯데칙촉오리지날',
                '90072': '오리온오징어땅콩98G',
                '10210': '오리온)포카칩오리지널66G',
                '30292': '프링글스양파맛53G',
                '10209': '해태)맛동산90G',
                '45220': '오리온)예감치즈그라탕맛32G',
                '35044': '해태후렌치파이딸기256G',
                '30099': '롯데)빠다코코낫100G',
                '30096': '롯데)웨하스딸기맛50G',
                '65727': '롯데몽쉘카카오생크림케이크12봉',
                '65719': '크라운제과쿠크다스화이트에디션',
                '65890': '투데이)크리스프초코',
                '90073': '농심)고구마깡83G',
                '10095': '농심바나나킥75G',
                '20167': '해태)오사쯔60G',
                '30291': '프링글스오리지날53G'}
model_dict = dict(zip(backend_dict.values(), backend_dict.keys()))

if len(img_paths) != len(xml_paths):
    print("이미지와 xml갯수가 다르니 확인해주세요")
else:
    # 이미지와 xml파일이 매칭되는지 확인하는 부분
    tmp_img_paths = []
    tmp_xml_paths = []
    for idx in range(len(img_paths)):
        tmp_img_paths.append(img_paths[idx].replace(".jpg", " ").split("\\")[-1])
        tmp_xml_paths.append(xml_paths[idx].replace("_meta.xml", " ").split("\\")[-1])
    tmp_img_paths.sort()
    tmp_xml_paths.sort()
    if tuple(tmp_img_paths) != tuple(tmp_xml_paths):
        print("이미지와 xml파일이 매칭되지 않습니다")

    load_state = True
    cnt = 1
    while True:
        # 이미지 합성을 위한 도화지 준비
        paper = np.full((img_size, img_size, 3), (207, 212, 211), dtype=np.uint8)

        if load_state:
            # 이미지 불러올 index 설정
            idx_1, idx_2 = random.randint(0, len(img_paths) - 1), random.randint(0, len(img_paths) - 1)
            load_state = False

        # bbox 축소 비율 측정
        ratio_1 = cv2.getTrackbarPos("ratio_1", "setting")
        ratio_2 = cv2.getTrackbarPos("ratio_2", "setting")

        # 시작점 측정
        point_x1 = cv2.getTrackbarPos("point_x1", "setting")
        point_y1 = cv2.getTrackbarPos("point_y1", "setting")
        point_x2 = cv2.getTrackbarPos("point_x2", "setting")
        point_y2 = cv2.getTrackbarPos("point_y2", "setting")

        # 이미지 별 축소된 bbox 추출
        bbox_1, name_1, area_1 = image_process(idx_1, xml_paths, img_size, ratio_1)
        bbox_2, name_2, area_2 = image_process(idx_2, xml_paths, img_size, ratio_2)

        if (point_x1 + bbox_1.shape[1] < img_size and point_y1 + bbox_1.shape[0] < img_size) \
            and (point_x2 + bbox_2.shape[1] < img_size and point_y2 + bbox_2.shape[0] < img_size):
            paper[point_y1: point_y1 + bbox_1.shape[0], point_x1: point_x1 + bbox_1.shape[1], ] = bbox_1
            paper[point_y2: point_y2 + bbox_2.shape[0], point_x2: point_x2 + bbox_2.shape[1], ] = bbox_2
        else:
            print("구간을 벗어 나니 다시 조정 하세요!")

        cv2.imshow('paper', paper)

        key = cv2.waitKey(1)
        if key == ord('n'):
            load_state = True
            cv2.setTrackbarPos("point_x1", "setting", 0)
            cv2.setTrackbarPos("point_y1", "setting", 0)
            cv2.setTrackbarPos("point_x2", "setting", 0)
            cv2.setTrackbarPos("point_y2", "setting", 0)
        elif key == ord('s'):
            save_img_name = f"{first_file_name}_{img_id}.png"
            cv2.imwrite("_image_save/" + save_img_name, paper)
            coco_image = create_image(save_img_name, img_size, img_size, img_id)
            coco_annotation_1 = create_annotation(img_id, obj_id, model_dict[name_1], area_1,
                                                  [point_x1, point_y1, bbox_1.shape[1], bbox_1.shape[0]])
            obj_id += 1
            coco_annotation_2 = create_annotation(img_id, obj_id, model_dict[name_2], area_2,
                                                  [point_x2, point_y2, bbox_2.shape[1], bbox_2.shape[0]])
            obj_id += 1

            total_image.append(coco_image)
            total_annotation.append(coco_annotation_1)
            total_annotation.append(coco_annotation_2)

            img_id += 1
            print(f"New {cnt}th Image Create")
            cnt += 1
        elif key == 27:  # esc 입력
            print("이미지 작업 종료")
            break

cv2.destroyAllWindows()

INFO = create_INFO()
LICENSES = create_LICENSE()
CATEGORIES = create_category_number(model_dict)

coco_output = {
    "info": INFO,
    "licenses": LICENSES,
    "categories": CATEGORIES,
    "images": total_image,
    "annotations": total_annotation,
    "type": "instances"
}

with open("annotation.json", "w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(coco_output, ensure_ascii=False))

print("save a annotation.json file")

"""
make json file of COCO data format
 - category name is number(str)
"""

import glob
import xml.etree.ElementTree as ET
import json
from create_coco_format import *

img_size = int(input("변경할 이미지의 사이즈를 입력하세요: "))
mode = str(input("어떤 용도 입니까?(train용인 경우 train, valid용인 경우 valid 입력)"))

data_path = "original_sample/" + mode + "/라벨링데이터/*"
folder_paths = glob.glob(data_path)

# 전체 파일로 테스트
img_id = 0
obj_id = 0
total_image = []
total_annotation = []
cnt = 0
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

for folder_path in folder_paths:
    cnt += 1
    xml_paths = glob.glob(folder_path + "/*meta.xml")

    img_folder_path = folder_path.replace("라벨링데이터", "images/").split('\\')[0]
    folder_cnt = 0

    for xml_path in xml_paths:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 각 이미지 정보
        annotation = root.find('annotation')
        name = annotation.find('.//name').text

        img_name = annotation.find("filename").text
        img_height = int(annotation.find("size").find("height").text)
        img_width = int(annotation.find("size").find("width").text)
        coco_image = create_image(img_name, img_size, img_size, img_id)

        # 각 객체 정보
        objects = annotation.findall('object')
        for obj in objects:
            coords = obj.find('bndbox')
            x_min = int(coords.find('xmin').text)
            y_min = int(coords.find('ymin').text)
            x_max = int(coords.find('xmax').text)
            y_max = int(coords.find('ymax').text)

            resize_x_min = x_min * img_size // img_width
            resize_y_min = y_min * img_size // img_width
            resize_x_max = x_max * img_size // img_width
            resize_y_max = y_max * img_size // img_width

            obj_width = resize_x_max - resize_x_min
            obj_height = resize_y_max - resize_y_min
            obj_area = obj_width * obj_height
            obj_bbox = [resize_x_min, resize_y_min, obj_width, obj_height]
            coco_annotation = create_annotation(img_id, obj_id, model_dict[name], obj_area, obj_bbox)
            total_annotation.append(coco_annotation)
            obj_id += 1

        folder_cnt += 1
        img_id += 1
        total_image.append(coco_image)
    print(f"{cnt}번째 폴더인 {folder_path} 폴더 작업 완료했습니다.")

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

with open(f"{mode}.json", "w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(coco_output, ensure_ascii=False))
print(f"save a {mode}.json file")
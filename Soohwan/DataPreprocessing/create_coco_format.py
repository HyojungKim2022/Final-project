"""
make a coco format data for object detection
"""
import datetime


def create_INFO(year=2023):
    INFO = {
        "description": "My Dataset",
        "url": "",
        "version": "",
        "year": year,
        "contributor": "",
        "date_created": datetime.datetime.utcnow().isoformat(' ')
    }
    return INFO


def create_LICENSE():
    LICENSE = [
        {
            "id": 0,
            "name": "",
            "url": ""
        }
    ]
    return LICENSE


def create_category_number(categorys):
    category_list = []
    for key, value in categorys.items():
        category = {
            "supercategory": key,
            "name": value,
            "id": value
        }
        category_list.append(category)
    return category_list


def create_category_name(categorys):
    category_list = []
    for key, value in categorys.items():
        category = {
            "supercategory": key,
            "name": key,
            "id": value
        }
        category_list.append(category)
    return category_list


def create_image(file_name, height, width, image_id):
    image = {
        "file_name": file_name,
        "height": height,
        "width": width,
        "id": image_id,
        "license": 0,
        "url": "null",
        "date_captured": "null"
    }
    return image


def create_annotation(image_id, object_id, category_id, area, bbox):
    annotations = {
        "id": object_id,
        "image_id": image_id,
        "category_id": category_id,
        "segmentation": [],  # RLE or [polygon]
        "area": area,  # float
        "bbox": bbox,  # [x, y, width, height]
        "iscrowd": 0,
        "ignore": 0
    }
    return annotations
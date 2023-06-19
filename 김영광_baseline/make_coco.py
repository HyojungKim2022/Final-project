import json
import xml.etree.ElementTree as ET
import glob


root_dir = 'D:/coding/dataset/sample/'
annot_dir = '라벨링데이터/'
img_dir = 'images/'

def cat_mapping(root_dir, annot_dir):
    clses = glob.glob(root_dir + annot_dir + '/*')
    clses = [cls[cls.rfind('_')+1:] for cls in clses]
    return {cls : i for i, cls in enumerate(clses)}

c = cat_mapping(root_dir, annot_dir)
for key, value in c.items():
    print(key, value)

def convert_xml_to_coco(root_dir, annot_dir, output_file):
    coco_data = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    category_mapping = cat_mapping(root_dir, annot_dir)

    # Load XML files from the given folder
    xml_files = glob.glob(root_dir + annot_dir + '*/*_meta.xml')
    image_id = 1
    annotation_id = 1

    categories = []
    for cat, id in category_mapping.items():
        category = {
            "id" : id,
            "name" : cat,
            # 이유 -> 
            "supercategory" : '과자'
        }        
        coco_data['categories'].append(category)
    
    for xml_file in xml_files:
        # Parse the XML content
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Extract image information
        image_filename = root.find("annotation/filename").text
        image_width = int(root.find("annotation/size/width").text)
        image_height = int(root.find("annotation/size/height").text)

        # Create the image entry in COCO data
        image_entry = {
            "id": image_id,
            "file_name": image_filename,
            "width": image_width,
            "height": image_height
        }
        coco_data["images"].append(image_entry)

        # Extract object annotations
        objects = root.findall("annotation/object")
        for obj in objects:
            # Extract class name
            class_name = obj.find("name").text

            # Add the category to COCO categories if it doesn't exist
            if class_name not in category_mapping:
                category_mapping[class_name] = len(category_mapping) + 1
                category_entry = {
                    "id": category_mapping[class_name],
                    "name": class_name,
                    "supercategory": "Unspecified"
                }
                coco_data["categories"].append(category_entry)

            category_id = category_mapping[class_name]

            # Extract bounding box coordinates
            xmin = int(obj.find("bndbox/xmin").text)
            ymin = int(obj.find("bndbox/ymin").text)
            xmax = int(obj.find("bndbox/xmax").text)
            ymax = int(obj.find("bndbox/ymax").text)

            # Create the annotation entry in COCO data
            annotation_entry = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],
                "area": (xmax - xmin) * (ymax - ymin),
                "iscrowd": 0
            }
            coco_data["annotations"].append(annotation_entry)

            annotation_id += 1

        image_id += 1

    # Save the COCO data as JSON file
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(coco_data, f, ensure_ascii=False)

# Specify the folder containing the XML files and the output file path
output_file = root_dir + "coco_dataset.json"

# Convert the XML files to COCO dataset format
convert_xml_to_coco(root_dir, annot_dir, output_file)

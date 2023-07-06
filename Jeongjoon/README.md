# Final-project
## Purpose
- The purpose of this final project is to develop a payment system that doesn't require barcodes at checkout, using a vision model.
- The system developed for this project is named "Barcodeless Calculator" (BCL)

## Model
- EfficientDet from MMdetection 3.0 (https://github.com/open-mmlab/mmdetection/tree/3.x/projects/EfficientDet)

## Datasets 
- AIhub: '상품 이미지' (https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=64)

## Other works
1) XML2JSON conversion
- the XML2JSON tool was used (https://github.com/yukkyo/voc2coco) to convert the dataset annotations from XML to JSON format.

2) Addressing Korean decoding errors
- The MMDetection 3.0 library, which is used in this project, relies on OpenCV for image processing. However, OpenCV has limitations when it comes to displaying Korean text. To overcome this issue, the Python Imaging Library (PIL) will be used to handle Korean text rendering and display in the context of MMDetection 3.0


3) Exploration of other models
- RTMDet_s model from MMdetection 3.0 (https://github.com/open-mmlab/mmdetection/tree/3.x/configs/rtmdet) and evaluate its performance for the payment system

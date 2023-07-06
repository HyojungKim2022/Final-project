# Final-project
## Introduction
### Purpose
- The purpose of this final project is to develop a payment system that doesn't require barcodes at checkout, using a vision model.
- The system developed for this project is named "Barcodeless Calculator" (BLC)

### Model
- EfficientDet from MMdetection 3.0 (https://github.com/open-mmlab/mmdetection/tree/3.x/projects/EfficientDet)
- Instructions: https://mmengine.readthedocs.io/en/latest/
### Datasets 
1) One product per image
   - AIhub: '상품 이미지' 
    (https://www.aihub.or.kr/aihubdata/data/view.docurrMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=64)
2) Two kinds of products per image (by Soohwan)
3) Four kinds of products per image (by Mainho)

## Main works
- Learning has been accumulated through the use of three datasets, resulting in the generation of PTH files.
- The batch size is limited due to a CUDA memory issue. 
![image](https://github.com/HyojungKim2022/Final-project/assets/128121364/a7266f4b-875e-4c6a-b8d4-4461b697702f)


## Other works
1) XML2JSON conversion
- the XML2JSON tool was used (https://github.com/yukkyo/voc2coco) to convert the dataset annotations from XML to JSON format.


2) Resizing for img files
- To improve learning efficiency, the images with dimensions of 3000 x 3000 were downscaled to 1000 x 1000.
- The coordinates of the bounding boxes were adjusted accordingly to accommodate the resizing.

3) Addressing Korean decoding errors
- The MMDetection 3.0 library, which is used in this project, relies on OpenCV for image processing. However, OpenCV has limitations when it comes to displaying Korean text. To overcome this issue, the Python Imaging Library (PIL) will be used to handle Korean text rendering and display in the context of MMDetection 3.0
![image](https://github.com/HyojungKim2022/Final-project/assets/128121364/f445d26e-1043-4edf-89ac-a29e2009b105)




4) Exploration of other models
- RTMDet_s model from MMdetection 3.0 (https://github.com/open-mmlab/mmdetection/tree/3.x/configs/rtmdet) and evaluate its performance for the BLC system

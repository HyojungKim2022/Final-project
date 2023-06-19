import os
import glob
import shutil

root_dir = 'D:/coding/dataset/sample/'
img_dir = '원천데이터/'
to_dir = 'images/'


def imageMerge(root_dir, img_dir, to_dir='images'):
    try:
        if not os.path.exists(root_dir + to_dir):
            os.makedirs(root_dir+to_dir)
    except:
        print("Error")

    img_paths = glob.glob(root_dir + img_dir + '*/*.jpg')

    for idx, img_path in enumerate(img_paths):
        img_name = img_path[img_path.rfind('\\')+1:]
        shutil.move(img_path, root_dir + to_dir + img_name)
        if idx%100==0:
            print(idx//100)
    
    shutil.rmtree(root_dir+img_dir)
    print('end merging')

imageMerge(root_dir, img_dir, to_dir)
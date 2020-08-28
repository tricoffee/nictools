import json
import os
from nicutils import list_basefiles,save_as_json
import numpy as np
import cv2
label2catid = {"cat":1,"dog":2}
# 文件路径示例
# parent_dir
#   |
#   |______  label_dir
#   |          |__    1.json
#   |          |__    2.json
#   |          |__    3.json
#   |
#   |_______ image_dir
#              |__    1.bmp
#              |__    2.bmp
#              |__    3.bmp
label_dir = "/dataset/labels"
image_dir = "/dataset/Image"
coco_dir = "/dataset/coco_data"
base_labelfnms = list_basefiles(label_dir)
base_imgfnms = list_basefiles(image_dir)

info = {'description': 'cat_dog',
'version': '1.0', 'year': 2020, 'contributor': 'tricoffee', 'date_created': '2020/07/15'}


coco_json_fnm = "coco_data.json"
coco_json_fnm = os.path.join(coco_dir,coco_json_fnm)
with open(coco_json_fnm,"w") as f2:
    pass

assert len(base_imgfnms) == len(base_labelfnms)

images = []
annotations = []
bbox_id = 0
for i,base_labelfnm in enumerate(base_labelfnms):
    file_name = base_labelfnm.strip(".")[0]+".bmp"
    json_fnm = os.path.join(label_dir,base_labelfnm)
    with open(json_fnm,"r") as load_f:
         load_dict = json.load(load_f)
    shapes = load_dict["shapes"]
    height = load_dict["imageHeight"]
    width = load_dict["imageWidth"]
    image_id = i+1
    image = dict(file_name=file_name,height=height,width=width,id=image_id)
    images.append(image)

    for shape in shapes:
        bbox_id += 1
        label = shape["label"]
        points = shape["points"]
        group_id = shape["group_id"]
        category_id = label2catid[label]
        polygon = np.array(points, dtype=np.int32)
        area = cv2.contourArea(polygon)
        bx, by, bw, bh = cv2.boundingRect(polygon)
        # coco format bbox
        # For object detection annotations, the format is "bbox" : [x,y,width,height]
        # Where:
        # x, y: the upper-left coordinates of the bounding box
        # width, height: the dimensions of your bounding box
        # Refer to https://github.com/cocodataset/cocoapi/issues/102
        bbox = [bx,by,bw,bh]
        # iscrowd 等于0，一个bbox只包含一类物体
        annotation=dict(image_id=image_id,category_id=category_id,segmentation=points,id=bbox_id,
                        area=area,bbox=bbox,iscrowd=0)
        annotations.append(annotation)
categories = [{"supercategory":"animal","name":"cat","id":1},
             {"supercategory": "animal","name":"dog","id":2}]

coco_dict = dict(info=info,images=images,annotations=annotations,categories=categories)

save_as_json(coco_dict,coco_json_fnm)

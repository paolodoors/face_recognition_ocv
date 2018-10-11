import numpy as np
import tensorflow as tf
import cv2 as cv
import os

from object_detection.utils import label_map_util
from object_detection.utils import dataset_util

CWD_PATH = os.getcwd()
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
PATH_TO_FROZEN_GRAPH = os.path.join(CWD_PATH,  MODEL_NAME, 'frozen_inference_graph.pb')
print(PATH_TO_FROZEN_GRAPH)




# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME,'ssd_mobilenet_v1_coco_2017_11_17.pbtxt')
print(PATH_TO_LABELS)

encodetype = b'rgb'
filename = PATH_TO_LABELS
filename_utf8 = filename.encode('utf8')

# Loading label map
# label_map = label_map_util.load_labelmap(dataset_util.bytes_feature(filename_utf8))

category_index = label_map_util.create_category_index_from_labelmap(dataset_util.bytes_feature(filename_utf8), use_display_name=True)
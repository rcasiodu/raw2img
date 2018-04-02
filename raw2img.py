import cv2
import numpy as np
import matplotlib.pyplot as plt

raw_type = 8
raw_file = '01.raw'
img_width = 1632
img_height = 1224
img_file = raw_file.split('.')[0]+'.jpg'

with open(raw_file, 'rb') as f:
    img_raw = f.read()

img = []
for i in range(img_height):
    line_value = []
    for j in range(img_width):
        line_value.append(img_raw[i*img_width+j])
    img.append(line_value)

if raw_type==8:
    img = np.array(img)
    cv2.imwrite(img_file, img)

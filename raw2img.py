import cv2
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

raw_type = 12
raw_file = '02.raw'
#img_width = 1632
#img_height = 1224
#IMX290 1848*1097
img_width = 1948
img_height = 1097

img_file = raw_file.split('.')[0]+'.jpg'

with open(raw_file, 'rb') as f:
    img_raw = f.read()

img = []
if raw_type==8:
	img = np.array(list(img_raw)).reshape(img_height, -1)
elif raw_type==12:
	# cols of raw image in bytes
	max_col = int(len(img_raw)/img_height)
	# real cols in bytes
	col_bytes = int(img_width*3/2)
	img = np.array(list(img_raw)).reshape(img_height, -1)
	# get rid of dummy cols
	if max_col>col_bytes:
		dummy_col = list(range(col_bytes, max_col))
		img = np.delete(img, dummy_col, axis=1)
	low8_col = list(range(2, col_bytes, 3))
	# get rid of low 4 bit
	# raw12 format: P1[11:4]P2[11:4]P2[3:0]P1[3:0]
	img = np.delete(img, low8_col, axis=1)

cv2.imwrite(img_file, img)

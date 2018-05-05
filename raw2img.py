import cv2
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

def raw2img(img_raw, raw_type, img_width, img_height):
	if raw_type == 8:
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
	return img

def multiraw2value(img_raw, raw_type, fps, img_width, img_height):
	multiraw = np.array(list(img_raw)).reshape(fps, img_height, -1)
	multiimg = np.zeros((fps, img_height, img_width), dtype = 'float32')
	if raw_type==12:
		odd = (multiraw[:, :, 0::3] & int(0xff)) + (multiraw[:, :, 2::3] & int(0x0f))
		even = (multiraw[:, :, 1::3] & int(0xff)) + (multiraw[:, :, 2::3] & int(0xf0))
		multiimg[:, :, 0::2] = odd
		multiimg[:, :, 1::2] = even
	elif raw_type==8:
		multiimg = multiraw
	return multiimg

def hist_plot(raw_img):
	#multiimg = multiraw2value(img_raw, 12, 1, 1920, 1080)
	pixel_value = np.max(raw_img).item()
	hist = cv2.calcHist([raw_img], [0], None, [int(pixel_value)+1], [0, pixel_value])
	plt.plot(range(int(pixel_value)+1), hist)
	#plt.bar(left = range(int(pixel_value)+1), height = hist[:, 0])
	plt.show()	

raw_type = 12
raw_file = 'ISPOFF-BLC40.raw'

#IMX290 1848*1097
img_width = 1920
img_height = 1080

img_file = raw_file.split('.')[0]+'.jpg'

with open(raw_file, 'rb') as f:
    img_raw = f.read()

#img = raw2img(img_raw, raw_type, img_width, img_height)

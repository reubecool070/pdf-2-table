import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import pytesseract
import pandas as pd
import json
from sys import exit
from PIL import Image, ImageFilter, ImageEnhance

# get relative path
new_path = os.path.dirname(__file__)


# convert image to grayscale
def convert_to_grayscale(img, thresvalue):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh, img_bin = cv2.threshold(img, thresvalue, 255, cv2.THRESH_BINARY)
    img_bin2 = 255-img_bin
    thresh1, img_bin_otsu = cv2.threshold(
        img_bin2, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite('images/img_bin_otsu'+str(thresvalue)+'.jpg', img_bin_otsu)
    return img_bin_otsu

# enhance image
def enhance_image(sharp=3, contrast=2, brightness=2):
    #open image to enhance
    img = Image.open("images/empty-4.jpg")
    #Sharpen image
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharp)
    #Constrast Image
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    #Brightness Image
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)
    #save image
    img.save("images/result.png")

# detect table vertically
def detect_vertical(img):
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, np.array(img).shape[1]//100))
    eroded_image = cv2.erode(img_grayscale, vertical_kernel, iterations=1)
    dilated_image = cv2.dilate(eroded_image, vertical_kernel, iterations=5)
  
    # opening = cv2.morphologyEx(dilated_image, cv2.MORPH_OPEN, kernel1)
    return dilated_image

# detect table horizontally
def detect_horizontal(img):
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (np.array(img).shape[1]//100, 1))
    eroded_image = cv2.erode(img_grayscale, horizontal_kernel, iterations=1)
    dilated_image = cv2.dilate(eroded_image, horizontal_kernel, iterations=7)
    # opening = cv2.morphologyEx(dilated_image, cv2.MORPH_OPEN, kernel1, iterations=2)
    return dilated_image

# remove noise 
def remove_noise(img):
    denoise_1 = cv2.fastNlMeansDenoisingColored(img,None,3,3,7,21) 
    denoise_2 = cv2.fastNlMeansDenoisingColored(img,None,5,5,7,21) 
    denoise_3 = cv2.fastNlMeansDenoisingColored(img,None,15,15,7,21)
    cv2.imwrite('images/denoise_1.png', denoise_1) 
    cv2.imwrite('images/denoise_2.png', denoise_2) 
    cv2.imwrite('images/denoise_3.png', denoise_3)
    return denoise_3

# merge two horizontal and vertical images
def mergetables(vertical_image, horizontal_image, img_grayscale, kernel):
    vertical_horizontal_lines = cv2.addWeighted(
        vertical_image, 0.5, horizontal_image, 0.5, 0.0)
    vertical_horizontal_lines = cv2.erode(
        ~vertical_horizontal_lines, kernel, iterations=3)

    thresh, vertical_horizontal_lines = cv2.threshold(
        vertical_horizontal_lines, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    bitxor = cv2.bitwise_xor(img_grayscale, vertical_horizontal_lines)
    bitnot = cv2.bitwise_not(bitxor)
    return bitnot, vertical_horizontal_lines

# remove short horizontal lines
def remove_short_horizontal_lines(img, kernel,thresh):
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255,255,255), 2)

enhance_image()
img2 = cv2.imread("images/result.png")
img_grayscale = convert_to_grayscale(img2, 30)


plotting = plt.imshow(img_grayscale, cmap='gray')
kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
print(kernel1)

plt.figure(figsize=(100, 100))
vertical_image = detect_vertical(img_grayscale)
plotting = plt.imshow(vertical_image, cmap='gray')

plt.figure(figsize=(100, 100))
horizontal_image = detect_horizontal(img_grayscale)
plotting = plt.imshow(horizontal_image, cmap='gray')

bitnot, vertical_horizontal_lines = mergetables(vertical_image, horizontal_image, img_grayscale, kernel1)

plt.figure(figsize=(100, 100))
plotting = plt.imshow(bitnot, cmap='gray')

# getting contours
contours, hierarchy = cv2.findContours(
    vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
boundingBoxes = [cv2.boundingRect(contour) for contour in contours]
(contours, boundingBoxes) = zip(
    *sorted(zip(contours, boundingBoxes), key=lambda x: x[1][1]))

plt.figure(figsize=(100, 100))
boxes = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if (w < 1000 and h < 500):
        image = cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        boxes.append([x, y, w, h])

plotting = plt.imshow(image, cmap='gray')
plt.title("Identified contours")

plt.show()

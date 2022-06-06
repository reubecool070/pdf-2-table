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
    # cv2.imwrite('images/img_bin_otsu'+str(thresvalue)+'.jpg', img_bin_otsu)
    return img_bin_otsu

# enhance image
def enhance_image(sharp=3, contrast=2, brightness=3):
    #open image to enhance
    img = Image.open("images/empty-1.jpg")
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
    # img.save("images/result.png")

enhance_image()

img2 = cv2.imread("images/result.png")
img_grayscale = convert_to_grayscale(img2, 100)

plotting = plt.imshow(img_grayscale, cmap='gray')
kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
plt.show()

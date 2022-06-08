import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('images/empty-1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Detect horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

# Detect vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,50))
vertical_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)

# Combine masks and remove lines
table_mask = cv2.bitwise_or(horizontal_mask, vertical_mask)
image[np.where(table_mask==255)] = [255,255,255]

plt.imshow(thresh)
plt.figure(figsize=(100, 100))
plt.imshow(horizontal_mask)

plt.figure(figsize=(100, 100))
plt.imshow(vertical_mask)

plt.figure(figsize=(100, 100))
plt.imshow(table_mask)

plt.figure(figsize=(100, 100))
plt.imshow(image)

plt.show()
# cv2.imshow('thresh', thresh)
# cv2.imshow('horizontal_mask', horizontal_mask)
# cv2.imshow('vertical_mask', vertical_mask)
# cv2.imshow('table_mask', table_mask)
# cv2.imshow('image', image)
# cv2.waitKey()
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import pytesseract
import pandas as pd
import json
from sys import exit
from PIL import Image, ImageFilter, ImageEnhance
import tensorflow as tf
import pathlib

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# get relative path
new_path = os.path.dirname(__file__)
image_path = new_path + "/images/empty-6.jpg"

# create a dataset
batch_size = 32
img_height = 50
img_width = 150
# getting model
dataset_path = os.path.join(new_path, "APM_LABELS")
data_dir = pathlib.Path(dataset_path)
class_names = ["NA", "NO", "YES"]
model = tf.keras.models.load_model('apm_model.h5')


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][1]))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


original_img = cv2.imread(image_path)

# Functon for extracting the box


def box_extraction(img_for_box_extraction_path, cropped_dir_path):

    print("Reading image..")
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 30, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image

    print("Storing binary image to images/Image_bin.jpg..")
    cv2.imwrite("images/empty-result.jpg", img_bin)

    print("Applying Morphological Operations..")
    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//40

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=1)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=5)
    cv2.imwrite("images/verticle_lines.jpg", verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=2)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=2)
    cv2.imwrite("images/horizontal_lines.jpg", horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(
        verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(
        img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    print("Binary image which only contains boxes: images/img_final_bin.jpg")
    cv2.imwrite("images/img_final_bin.jpg", img_final_bin)
    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(
        img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    # (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

    print("Output stored in Output directiory!")

    idx = 0
    for c in contours[::-1]:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)

        # If the box height is greater then 15, widht is >70, then only save it as a box in "cropped/" folder.
        # if (w > 50 and h > 10) and w > 3*h:
        if (w > 50 and h > 10):
            idx += 1
            new_img = original_img[y:y+h, x:x+w]
            # resize image
            new_img = cv2.resize(new_img, (150, 40))
            cv2.imwrite(cropped_dir_path+str(idx) + '.png', new_img)
            # load image to model
            new_img = new_img.reshape(1, 40, 150, 3)
            # tensor_img = tf.keras.utils.load_img(
            #     new_img, target_size=(img_height, img_width)
            # )
            # img_array = tf.keras.utils.img_to_array(tensor_img)
            # img_array = tf.expand_dims(img_array, 0) # Create a batch
            predictions = model.predict(new_img)
            print(predictions)
            score = tf.nn.softmax(predictions[0])
            print(idx, class_names[np.argmax(score)],100 * np.max(score))

    # For Debugging
    # Enable this line to see all contours.
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    # cv2.imwrite("./images/img_contour.jpg", img)


# Input image path and out folder
box_extraction(image_path, "./cropped-0/")

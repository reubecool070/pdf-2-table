import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import json
import sys
import tensorflow as tf
import pathlib
import string

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


# image_url = 'https://www.apmterminals.com/los-angeles/-/media/americas/LA/daily-information/empty-receivables-6-13.jpg'
image_url = sys.argv[1]
new_path = os.path.dirname(__file__)
temp_path = '/tmp'

# returns 0 if success


def wget(url, download_path):
    return os.system('wget -O {} {}'.format(download_path, url))


# wget(image_url, temp_path + '/empty-1.jpg')

# get relative path
image_path = temp_path + "/empty-1.jpg"
original_img = cv2.imread(image_path)


DEFAULT_ALPHABET = string.digits + string.ascii_lowercase
blank_index = len(DEFAULT_ALPHABET)
# create a dataset
batch_size = 32
img_height = 50
img_width = 150
# getting model
dataset_path = os.path.join(new_path, "APM_LABELS")
data_dir = pathlib.Path(dataset_path)
class_names = ["NA", "NO", "OTHER", "YES"]
text_detection = []

model = tf.keras.models.load_model(new_path+'/trainmodel/apm_model_new10.h5')

def run_model():
    path = f'/trainmodel/ocr_dr.tflite'
    interpreter = tf.lite.Interpreter(model_path=new_path+path)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return input_details, output_details, interpreter

input_details, output_details, interpreter = run_model()

def run_tflite_model(image_path, quantization):
    input_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    input_data = cv2.resize(input_data, (200, 31))
    input_data = input_data[np.newaxis]
    input_data = np.expand_dims(input_data, 3)
    input_data = input_data.astype('float32')/255
    # path = f'/trainmodel/ocr_dr.tflite'
    # interpreter = tf.lite.Interpreter(model_path=new_path+path)
    # interpreter.allocate_tensors()

    # # Get input and output tensors.
    # input_details = interpreter.get_input_details()
    # output_details = interpreter.get_output_details()

    # input_shape = input_details[0]['shape']
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    return output


# Functon for extracting the box


def box_extraction(img_for_box_extraction_path, cropped_dir_path):
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    # enhance image with opencv
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    (thresh, img_bin) = cv2.threshold(img, 100, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    # cv2.imwrite(new_path+'/images/img_bin.jpg', img_bin)

    # Defining a kernel length    exit()
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
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # cv2.imwrite(new_path+"/images/verticle_lines.jpg", verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=1)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=2)
    # cv2.imwrite(new_path+"/images/horizontal_lines.jpg", horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(
        verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(
        img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(
        img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imwrite(new_path+"/images/img_final_bin.jpg", img_final_bin)
    # Sort all the contours by top to bottom.
    # (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    # For Debugging
    # Enable this line to see all contours.
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    # cv2.imwrite(new_path+"/images/img_contour.jpg", img)
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
            new_img = new_img.reshape(1, 40, 150, 3)
            # custom model
            # load image to model
            predictions = model.predict(new_img)
            # tf.nn.relu(predictions[0])
            score = tf.nn.softmax(predictions[0])
            value = {
                'text':  class_names[np.argmax(score)],
                "confidence": 100 * np.max(score),
                'index': idx
            }
            # lite model from tensorflow
            if (value['text'] == "OTHER"):
                tflite_output = run_tflite_model(
                    cropped_dir_path+str(idx) + '.png', 'dr')
                value['text'] = "".join(
                    DEFAULT_ALPHABET[index] for index in tflite_output[0] if index not in [blank_index, -1])
                if 'ni' in value['text']:
                    value['text'] = "NA"
            text_detection.append(value)


# Input image path and out folder
box_extraction(image_path, temp_path + "/")
json_string = json.dumps(text_detection)
print(str(json_string))

# save list in json file
# with open(new_path + "/text_detection.json", 'r+') as outfile:
# outfile.write(json.dumps(text_detection, indent=4))
# json.dump(text_detection, outfile, indent=4)
# #close file
# outfile.close()

# import tensorflow as tf
# import os
# from tensorflow.keras import layers
# from tensorflow.keras import regularizers


# # !pip install git+https://github.com/tensorflow/docs

# import tensorflow_docs as tfdocs
# import tensorflow_docs.modeling
# import tensorflow_docs.plots


# from matplotlib import pyplot as plt

# import numpy as np

# import pathlib
# import shutil
# import tempfile

# FEATURES = 28
# print(tf.__version__)

# # getting relative path
# relative_path = os.path.dirname(__file__)
# dataset_path = os.path.join(relative_path, "APM_LABELS")

# # get the labels
# data_dir = pathlib.Path(dataset_path)
# image_count = len(list(data_dir.glob('*/*.png')))
# print(image_count)

# N_VALIDATION = 300
# N_TRAIN = 600
# BUFFER_SIZE = 600
# BATCH_SIZE = 30
# STEPS_PER_EPOCH = N_TRAIN//BATCH_SIZE  # 20

# validate_ds = dataset_path.take(N_VALIDATION).cache()
# train_ds = dataset_path.skip(N_VALIDATION).take(N_TRAIN).cache()

# validate_ds = validate_ds.batch(BATCH_SIZE)
# train_ds = train_ds.shuffle(BUFFER_SIZE).repeat().batch(BATCH_SIZE)

# # inverseTimedecay to decrease the learning rate over time
# lr_schedule = tf.keras.optimizers.schedules.InverseTimeDecay(
#     0.001,
#     decay_steps=STEPS_PER_EPOCH*1000,
#     decay_rate=1,
#     staircase=False
# )


# def get_optimizer():
#     return tf.keras.optimizers.Adam(lr_schedule)

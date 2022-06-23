import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import pathlib

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# getting relative path
relative_path = os.path.dirname(__file__)
dataset_path = os.path.join(relative_path, "APM_LABELS")

# get the labels
data_dir = pathlib.Path(dataset_path)
image_count = len(list(data_dir.glob('*/*.png')))
print(image_count)

no = list(data_dir.glob('NO/*'))
print("opening")

# im = PIL.Image.open(str(no[0]))
# print("open")
# im.show()

# create a dataset
batch_size = 16
img_height = 40
img_width = 150

# train dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# validation dataset
val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

#standardize the data
normalization_layer = layers.Rescaling(1./255)
# using that layer to convert to 0 ,1
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

# create the model
num_classes = len(class_names)

#data augmentation
data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    # layers.RandomRotation(0.1),
    # layers.RandomZoom(0.1),
  ]
)

model = Sequential([
  # layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  # layers.Conv2D(16, 3, padding='same', activation='relu'),
  # layers.MaxPooling2D(),
  # layers.Conv2D(32, 3, padding='same', activation='relu'),
  # layers.MaxPooling2D(),
  # layers.Conv2D(64, 3, padding='same', activation='relu'),
  # layers.MaxPooling2D(),
  # layers.Flatten(),
  # layers.Dense(128, activation='relu'),
  # layers.Dense(num_classes)
  # data_augmentation,
  # tf.keras.layers.Rescaling(1./255,input_shape=(img_height, img_width,3)),
  tf.keras.layers.Flatten(input_shape=(img_height, img_width,3)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

# compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#Modal summary
model.summary()

# train the model
epochs=15
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

# visualize training results:
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

#save tensorflow model history
model.save(relative_path+'/trainmodel/apm_model_final' + str(epochs) + '.h5')


plt.show()
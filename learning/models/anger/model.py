from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

train_dir = os.path.join(os.getcwd(), "../../data/anger/train")
validation_dir = os.path.join(os.getcwd(), "../../data/anger/validation")

train_anger_dir = os.path.join(train_dir, 'anger')
train_other_dir = os.path.join(train_dir, 'other')
validation_anger_dir = os.path.join(validation_dir, 'anger')
validation_other_dir = os.path.join(validation_dir, 'other')

num_anger_tr = len(os.listdir(train_anger_dir))
num_other_tr = len(os.listdir(train_other_dir))

num_anger_val = len(os.listdir(validation_anger_dir))
num_other_val = len(os.listdir(validation_other_dir))

total_train = num_anger_tr + num_other_tr
total_val = num_anger_val + num_other_val

print('total training anger images:', num_anger_tr)
print('total training other images:', num_other_tr)

print('total validation anger images:', num_anger_val)
print('total validation other images:', num_other_val)
print("--")
print("Total training images:", total_train)
print("Total validation images:", total_val)

batch_size = 128
epochs = 1
IMG_HEIGHT = 350
IMG_WIDTH = 350


train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size, directory=train_dir, shuffle=True, target_size=(IMG_HEIGHT, IMG_WIDTH), class_mode='binary')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size, directory=validation_dir, target_size=(IMG_HEIGHT, IMG_WIDTH), class_mode='binary')

model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Dropout(0.2),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

story = model.fit_generator(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)

model.summary()
model.save('anger_model.h5')


import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Activation, Dropout
from PIL import Image, ImageOps

class Robot:

    def __init__(self):
        self.mnist = tf.keras.datasets.mnist
        (self.x_train, self.y_train), (self.x_test, self.y_test) = self.mnist.load_data()
        self.x_train, self.x_test = self.x_train / 255.0, self.x_test / 255.0
        self.model = Sequential()
        self.model.add(Flatten(input_shape=(28, 28)))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(10,activation='softmax'))
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(self.x_train, self.y_train, epochs=5, validation_data=(self.x_test, self.y_test), verbose=0)

    def process_data(self):
        self.im = Image.open(r"screenshot.jpg")
        self.im = self.im.resize((28, 28))
        self.im = ImageOps.grayscale(self.im)
        self.im = ImageOps.invert(self.im)
        self.im = np.array(self.im)
        self.im = self.im.reshape(1, 28, 28)
        self.norm_im = self.im / np.max(self.im).astype(float)

    def predict(self):
        self.setPrediction = self.model.predict(self.norm_im)
        self.getPrediction = np.array(self.setPrediction[0])
        self.predictedNum = str(np.argmax(self.getPrediction))

    def reveal(self):
        return self.predictedNum
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :     
@Author:   zhangchang
@Date  :   2021/12/1 20:31
'''

import ndraw
import tensorflow as tf

# model = tf.keras.Sequential()
# model.add(tf.keras.layers.Conv2D(100,5))
# model.add(tf.keras.layers.Conv2D(10,3))
# model.add(tf.keras.layers.MaxPool2D())
# model.add(tf.keras.layers.Flatten())
# model.add(tf.keras.layers.Dense(200))
# model.add(tf.keras.layers.BatchNormalization())
# model.add(tf.keras.layers.Dense(20))
# model.add(tf.keras.layers.Dense(100))
# model.add(tf.keras.layers.Dense(200))
# model.add(tf.keras.layers.Dropout(0.2))
# model.add(tf.keras.layers.Dense(200))
# model.add(tf.keras.layers.Dense(200))
# model.add(tf.keras.layers.Dense(200))
# model.add(tf.keras.layers.Dense(200))
# model.add(tf.keras.layers.Dense(2,activation='softmax'))
# model.build(input_shape=(None,28,28,3))
x1 = tf.keras.layers.Input(shape=(None,100))
x = tf.keras.layers.Dense(100)(x1)
x = tf.keras.layers.Dense(40)(x)
x2 = tf.keras.layers.Input(shape=(None,100))
x3 = tf.keras.layers.Input(shape=(None,100))
x = tf.keras.layers.concatenate([x,x2,x3])
x = tf.keras.layers.Dense(300)(x)
x = tf.keras.layers.Dense(100)(x)
out = tf.keras.layers.Dense(2,activation="softmax")(x)
model = tf.keras.Model(inputs=[x1,x2,x3],outputs = out)
# from tensorflow import keras
# from tensorflow.keras import layers
# import tensorflow as tf
# model=tf.keras.Sequential([
#     tf.keras.layers.Dense(512,activation='relu',input_shape=(None,11)),
#     tf.keras.layers.Dense(256,activation='relu'),
#     tf.keras.layers.Dense(2,activation='softmax')
# ])
# ndraw.render(model)
ndraw.server(model,flow='horizontal')
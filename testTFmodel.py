#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :     
@Author:   Chang Zhang
@Date  :   2021/12/1 20:31
'''

import tensorflow as tf


def model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(100, 5))
    model.add(tf.keras.layers.Conv2D(10, 3))
    model.add(tf.keras.layers.MaxPool2D())
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(200))
    model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dense(20))
    model.add(tf.keras.layers.Dense(2))
    # model.add(tf.keras.layers.Softmax())
    model.build(input_shape=(None, 28, 28, 3))
    return model


def model2():
    x1 = tf.keras.layers.Input(shape=(None, 100))
    x = tf.keras.layers.Dense(100)(x1)
    # x = tf.keras.layers.Dense(40)(x)
    x2 = tf.keras.layers.Input(shape=(None, 100))
    x3 = tf.keras.layers.Input(shape=(None, 100))
    x = tf.keras.layers.concatenate([x, x2, x3])
    # x = tf.keras.layers.Dense(300)(x)
    # x = tf.keras.layers.Dense(100)(x)
    out = tf.keras.layers.Dense(2, activation="softmax")(x)
    out2 = tf.keras.layers.Dense(2, activation="softmax")(x)
    model = tf.keras.Model(inputs=[x1, x2, x3], outputs=[out,out2])
    return model

def model3():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    model.build(input_shape=(None, 100))
    return model

import ndraw
#该方式会在本地生成一个model.html的文件  直接浏览器打开即可
# ndraw.render(model2(),theme=ndraw.BLACK_WHITE)

# 该方式会启动一个web服务  本地9999端口访问
ndraw.server(model2(),theme=ndraw.DEFAULT,flow=ndraw.HORIZONTAL)

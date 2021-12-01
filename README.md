# ndraw
ndraw是一个简单的神经网络可视化工具

## 安装

### 1、pip安装
```
pip install ndraw
```

### 2、源码安装

下载源码，打开命令行

```
python setup.py bdist_egg

python setup.py install
```


## 使用

> 可以参考test.py

### 1、pb模型可视化
```
--pbpath
  |--variables
  |--saved_model.pb

```

```python
import ndraw
ndraw.server("pbpath")
# 打开浏览器访问9999端口即可
```

### 2、h5模型可视化

```python
import ndraw
ndraw.server("model.h5")
# 打开浏览器访问9999端口即可
```

### 3、模型对象可视化

```python
import ndraw
import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])
model.build(input_shape=(None, 100))
ndraw.server(model)
# 打开浏览器访问9999端口即可
```

### 4、生成html文件

```python
import ndraw
html = ndraw.render("pb/h5/mode均可",out_file="model.html")
# 生成一个model.html文件
```

### 5、其他参数

```
:param host: 服务地址 可自定义
:param port: 服务端口可自定义
:param flow: 布局方式：vertical and horizontal
```

## 参考图

![输入图片说明](image.png)

![输入图片说明](1image.png)
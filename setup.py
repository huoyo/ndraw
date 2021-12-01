#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   zhangchang
@Date  :   2021/12/1 21:11
'''
from setuptools import find_packages,setup
setup(
    name = 'ndraw',
    version = '1.0.0',
    packages = find_packages(),
    author = 'Chang Zhang',
    author_email = '1729913829@qq.com',
    url = 'www.langpy.cn',
    description = 'a tool to show neural networks',
    data_files = [
        ('core',['core/MetricFlow.js','core/template.html']),]
)
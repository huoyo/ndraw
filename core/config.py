#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :     
@Author:   Chang Zhang
@Date  :   2021/12/1 21:47
'''

def load_file(file_name):
    with open(file_name,'r',encoding='utf-8') as file:
        return file.read()
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   Chang Zhang
@Date  :   2022/4/09 22:31
'''
import uuid

class Graph(object):

    def __init__(self):
        self.nodes = []
        self.id = None
        self.from_id = None
        self.name = ''
        self.data = []


    def create(self,name,data=[]):
        node = Graph()
        node.id = str(uuid.uuid1()).replace('-','')
        node.name = name
        node.data = data
        node.nodes.append(node)
        return node

    def to(self,name,data=[]):
        node = Graph()
        node.id = str(uuid.uuid1()).replace('-','')
        node.from_id = self.id
        node.name = name
        node.data = data
        self.nodes.append(node)
        node.nodes = self.nodes
        return node

    def __repr__(self):
        return f'Graph(id={0},name={1},data={2})'.format(self.id,self.name,self.data)


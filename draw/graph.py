# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   Chang Zhang
@Date  :   2022/4/09 22:31
'''
import uuid
from draw.node import Node


class AutoGraph(object):

    def __init__(self):
        self.nodes = []
        self.id = None
        self.ids = None
        self.from_id = None
        self.name = ''
        self.data = []
        self.theme = None
        self.x = 0
        self.y = 0

    def create(self, node_data, data=[]):
        node = AutoGraph()
        node.id = str(uuid.uuid1()).replace('-', '')
        node = self.__parse_node_data(node, node_data, data=data)
        node.nodes.append(node)
        return node

    def creates(self, node_datas):
        node_ids = []
        nodes = []
        for node_data in node_datas:
            node = self.create(node_data)
            node_ids.append(node.id)
            nodes.append(node)
        return_node = nodes[-1]
        return_node.ids = node_ids
        return_node.nodes = nodes
        return return_node

    def tos(self, node_datas):
        node_ids = []
        nodes = self.nodes
        for node_data in node_datas:
            node = self.create(node_data)
            if self.ids is not None:
                node.from_id = self.ids
            else:
                node.from_id = self.id
            node_ids.append(node.id)
            nodes.append(node)
        return_node = nodes[-1]
        return_node.ids = node_ids
        return_node.nodes = nodes
        return return_node

    def to(self, node_data, data=[]):
        node = AutoGraph()
        node.id = str(uuid.uuid1()).replace('-', '')
        if self.ids is not None:
            node.from_id = self.ids
        else:
            node.from_id = self.id
        node = self.__parse_node_data(node, node_data, data=data)
        self.nodes.append(node)
        node.nodes = self.nodes
        return node

    def __parse_node_data(self, node, node_data, data=[]):
        if isinstance(node_data, str):
            node.name = node_data
            node.data = data
        elif isinstance(node_data, Node):
            node.name = node_data.name
            node.data = node_data.data
            node.theme = node_data.theme
            node.x = node_data.x
            node.y = node_data.y
        elif isinstance(node_data, dict):
            node.name = node_data['name']
            node.data = node_data['data']
            node.theme = node_data['theme']
            node.x = node_data['x']
            node.y = node_data['y']

        return node

    def __repr__(self):
        return 'AuthGraph(id={0},name={1},data={2})'.format(self.id, self.name, self.data)

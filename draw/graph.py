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
        self.border_color = None
        self.title_color = None
        self.data_color = None

    def add_node(self,node_data, data=[]):
        node = AutoGraph()
        node.id = str(uuid.uuid1()).replace('-', '')
        node = self.__parse_node_data(node, node_data, data=data)
        self.nodes.append(node)
        return node
    def add_nodes(self,node_datas):
        nodes = []
        for node_data in node_datas:
            node = self.add_node(node_data)
            nodes.append(node)
        return nodes

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
            node.border_color = node_data.border_color
            node.title_color = node_data.title_color
            node.data_color = node_data.data_color
        elif isinstance(node_data, dict):
            node.name = node_data['name']
            if 'data' in node_data.keys():
                node.data = node_data['data']

            if 'theme' in node_data.keys():
                node.theme = node_data['theme']

            if 'x' in node_data.keys():
                node.x = node_data['x']
            if 'y' in node_data.keys():
                node.y = node_data['y']

            if 'border_color' in node_data.keys():
                node.border_color = node_data['border_color']

            if 'title_color' in node_data.keys():
                node.title_color = node_data['title_color']

            if 'data_color' in node_data.keys():
                node.data_color = node_data['data_color']

        return node

    def __repr__(self):
        return 'AuthGraph(id={0},name={1},data={2})'.format(self.id, self.name, self.data)


class StableGraph(object):

    def __init__(self):
        self.nodes = []
        self.links = []
        self.id = None
        self.ids = None
        self.from_id = None
        self.name = ''
        self.data = []
        self.theme = None
        self.x = 0
        self.y = 0
        self.border_color = None
        self.title_color = None
        self.data_color = None

    def add_node(self,node_data, data=[]):
        node = StableGraph()
        node.id = str(uuid.uuid1()).replace('-', '')
        node = self.__parse_node_data(node, node_data, data=data)
        self.nodes.append(node)
        return node

    def add_nodes(self,node_datas):
        nodes = []
        for node_data in node_datas:
            node = self.add_node(node_data)
            nodes.append(node)
        return nodes

    def add_link(self,link_nodes):
        self.links.append(link_nodes)

    def add_links(self,link_nodes):
        self.links=self.links+link_nodes


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
            node.border_color = node_data.border_color
            node.title_color = node_data.title_color
            node.data_color = node_data.data_color

        elif isinstance(node_data, dict):
            node.name = node_data['name']
            if 'data' in node_data.keys():
                node.data = node_data['data']

            if 'theme' in node_data.keys():
                node.theme = node_data['theme']

            if 'x' in node_data.keys():
                node.x = node_data['x']
            if 'y' in node_data.keys():
                node.y = node_data['y']

            if 'border_color' in node_data.keys():
                node.border_color = node_data['border_color']

            if 'title_color' in node_data.keys():
                node.title_color = node_data['title_color']

            if 'data_color' in node_data.keys():
                node.data_color = node_data['data_color']

        return node

    def __repr__(self):
        return 'StableGraph(id={0},name={1},data={2})'.format(self.id, self.name, self.data)

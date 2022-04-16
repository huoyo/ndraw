# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   Chang Zhang
@Date  :   2022/4/09 22:31
'''
import uuid
from draw.node import Node
from core import server
from core.theme import *

class Graph(object):

    def __init__(self,name_unique=False):
        '''
        :param name_unique: Graph.id equals Graph.name if name_unique is True
        '''
        self.name_unique = name_unique
        self.links = []
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

    def exists(self,node):
        '''
        :param node: created node
        :return: return the node whose name is node.name if self.nodes contains it,if not,return the created node
        '''
        if self.name_unique == False:
            return False,None
        exist = False
        re = None
        for n in self.nodes:
            if n.name==node.name:
                exist = True
                re = n
                if node.from_id is not None:
                    if re.from_id is None:
                        re.from_id = node.from_id
                    else:
                        if isinstance(re.from_id,list) and isinstance(node.from_id,list):
                            re.from_id = re.from_id+node.from_id
                        elif isinstance(re.from_id,list) and isinstance(node.from_id,str):
                            re.from_id.append(node.from_id)
                        elif isinstance(re.from_id,str) and isinstance(node.from_id,list):
                            re.from_id = [re.from_id] + node.from_id
                        elif isinstance(re.from_id, str) and isinstance(node.from_id, str):
                            re.from_id = [re.from_id, node.from_id]
                break

        return exist,re

    def parse_node_data(self, node, node_data, data=[]):
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

    def server(self, host='localhost', port=9999, flow="horizontal", theme=Defualt()):
        server.server(self,host=host,port=port,flow=flow,theme=theme)

    def render(self,out_file='model.html', flow="horizontal", theme=Defualt()):
        return server.render(self,out_file=out_file,flow=flow,theme=theme)




class AutoGraph(Graph):

    def create(self, node_data, data=[]):
        node = AutoGraph(self.name_unique)
        node = self.parse_node_data(node, node_data, data=data)
        exists,n = self.exists(node)
        if exists:
            return n

        if self.name_unique:
            node.id = node.name
        else:
            node.id = str(uuid.uuid1()).replace('-', '')
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
        node = AutoGraph(self.name_unique)
        if self.ids is not None:
            node.from_id = self.ids
        else:
            node.from_id = self.id
        node = self.parse_node_data(node, node_data, data=data)
        exists, n = self.exists(node)
        if exists:
            return n
        if self.name_unique:
            node.id = node.name
        else:
            node.id = str(uuid.uuid1()).replace('-', '')
        self.nodes.append(node)
        node.nodes = self.nodes
        return node

    def __repr__(self):
        return 'AuthGraph(id={0},name={1},data={2})'.format(self.id, self.name, self.data)


class StableGraph(Graph):

    def add_node(self,node_data, data=[]):
        node = StableGraph(self.name_unique)
        node = self.parse_node_data(node, node_data, data=data)
        exists, n = self.exists(node)
        if exists:
            return n
        if self.name_unique:
            node.id = node.name
        else:
            node.id = str(uuid.uuid1()).replace('-', '')
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


    def __repr__(self):
        return 'StableGraph(id={0},name={1},data={2})'.format(self.id, self.name, self.data)

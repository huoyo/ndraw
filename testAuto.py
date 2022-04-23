# -*- encoding: utf-8 -*-
import ndraw
from ndraw import Node

graph = ndraw.AutoGraph()
graphs = graph.create(Node("开始",theme=ndraw.GREEN_WHITE))\
    .to(Node("过程1",data=["1.xxx","2.xxx"],theme=ndraw.DEEPGRAY_WHITE))\
    .to(Node("过程2",data=["1.xxx","2.xxx"],theme=ndraw.BLUE_WHITE))\
    .to(Node("结束",theme=ndraw.GREEN_WHITE))
ndraw.server(graphs)
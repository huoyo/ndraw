# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   Chang Zhang
@Date  :   2021/12/1 20:31
'''
import logging
from core import auto_template_html
from core import stable_template_html
from core import template_js
from core.constant import Flow
from core.theme import *
from draw.graph import AutoGraph
from draw.graph import StableGraph
from draw.graph import Graph

logging.basicConfig(level=logging.INFO)
try:
    import tensorflow as tf
except Exception as e:
    logging.warning(
        "failed to import tensorflow,please install tensorflow>=2.0 if you want to show model constructure of tensorflow! Of course,maybe you need ignore it when you want to show other model constructure.")


def _parse_layer(layer):
    input = map(lambda x: x.name.split("/")[0].split(":")[0],
                layer.input if isinstance(layer.input, list) else [layer.input])
    input = list(input)
    if len(input) == 1 and input[0] == layer.name:
        input = []
    res = {
        'name': layer.name,
        'class': layer.__class__.__name__,
        "input_shape": str(layer.input_shape),
        "output_shape": str(layer.output_shape),
        "activation": str(layer.activation.__name__) if hasattr(layer, 'activation') else 'None',
        "input": list(input),
        "filters": layer.filters if hasattr(layer, 'filters') else None,
        "kernel_size": layer.kernel_size if hasattr(layer, 'kernel_size') else None,
        "strides": layer.strides if hasattr(layer, 'strides') else None,
        "units": layer.units if hasattr(layer, 'units') else None,
        "rate": layer.rate if hasattr(layer, 'rate') else None,
    }
    if 'input' in  res['name'].lower():
        res['border_color'] = 'green'
        res['title_color'] = 'green'
        res['data_color'] = 'white'

    elif 'concatenate' in res['name'].lower():
        res['border_color'] = 'blue'
        res['title_color'] = 'blue'
        res['data_color'] = 'white'

    elif 'conv' in res['name'].lower():
        res['border_color'] = '#327355'
        res['title_color'] = '#327355'
        res['data_color'] = 'white'
    else:
        res['border_color'] = None
        res['title_color'] = None
        res['data_color'] = None

    return res


def _get_style(theme):
    theme = theme if isinstance(theme, Theme) else Theme()
    res = {}
    res['node'] = f"border:2px solid {theme.border_color};background-color:{theme.data_color};"
    res['title'] = f"font-size:{theme.title_font_size};background-color:{theme.title_color};color:{theme.title_font_color};"
    res['element'] = f"font-size:{theme.data_font_size};background-color:{theme.data_color};color:{theme.data_font_color};"

    return res

def _update_style(node_data,style):
    res ={}
    res['node'] = "border:2px solid border_color;background-color:data_color;"
    res['title'] = "font-size:15px;background-color:title_color;color:white;"
    res['element'] = "font-size:13px;background-color:data_color;color:black;"
    n  = 0
    if isinstance(node_data,Graph):
        if  node_data.border_color is not None:
            n+=1
            res['node'] = res['node'].replace('border_color',node_data.border_color)

        if node_data.title_color is not None:
            n += 1
            res['title'] = res['title'].replace('title_color', node_data.title_color)

        if node_data.data_color is not None:
            n += 1
            res['node'] = res['node'].replace('data_color', node_data.data_color)
            res['element'] = res['element'].replace('data_color', node_data.data_color)
    elif isinstance(node_data,dict):
        if node_data['border_color'] is not None:
            n += 1
            res['node'] = res['node'].replace('border_color', node_data['border_color'])

        if node_data['title_color'] is not None:
            n += 1
            res['title'] = res['title'].replace('title_color', node_data['title_color'] )

        if node_data['data_color'] is not None:
            n += 1
            res['node'] = res['node'].replace('data_color', node_data['data_color'])
            res['element'] = res['element'].replace('data_color', node_data['data_color'])

    if n==0:
        return style

    res['node'] = res['node'].replace('border_color', '#4a555e').replace('data_color', 'white')
    res['title'] = res['title'].replace('title_color', '#4a555e')
    res['element'] = res['element'].replace('data_color', 'white')
    return res


def _generate_nodes_data(node_name, res, theme=Defualt):
    style = _get_style(theme)
    style = _update_style(res, style)
    if len(res['input']) == 0:
        node_text_from = ''
    elif len(res['input']) == 1:
        node_text_from = '"from":"' + res['input'][0] + '",'
    else:
        node_text_from = '"from":' + str(res['input']) + ','

    node_text_start = ' let ' + node_name + '= {"style":"' + style['node'] + '", ' + node_text_from + ' "id":"' + res[
        'name'] + '","title":{"name":"' + res['class'] + '","style":"' + style['title'] + '"},"data":['
    node_text_end = ']}\n'
    node_text_mid = []
    for i,key in enumerate(res.keys()):
        value = res[key]
        if key not in ['name', 'class', 'input'] and value is not None:

            text = '{"name":"' + key + '：' + (value if isinstance(value, str) else str(value)) + '","style":"' + \
                       style['element'] + '"},'
            node_text_mid.append(text)
    return node_text_start + ''.join(node_text_mid) + node_text_end

def _generate_graph_nodes_data(node_name, res, theme=Defualt,is_auto=True):
    style = _get_style(theme)
    style = _update_style(res,style)
    if res.from_id is None:
        node_text_from = ''
    elif isinstance(res.from_id, str):
        node_text_from = '"from":"' + res.from_id+ '",'
    elif isinstance(res.from_id,list):
        node_text_from = '"from":' + str(res.from_id)+ ','

    xy = ''
    if hasattr(res,'x') and is_auto==False:
        node_text_from = '"x":' + str(res.x) + ','

    if hasattr(res, 'y') and is_auto==False:
        node_text_from = node_text_from+'"y":' + str(res.y) + ','

    node_text_start = ' let ' + node_name + '= {'+xy+'"style":"' + style['node'] + '", ' + node_text_from + ' "id":"' + res.id + '","title":{"name":"' + res.name + '","style":"' + style['title'] + '"}'
    data_pre = ''
    data_suf = ''
    node_text_end = '}\n'
    node_text_mid = []
    if res.data is not None and len(res.data)>0:
        data_pre = ',"data":['
        data_suf = ']'
        keys_len = len(res.data)
        for j,value in enumerate(res.data):
            if j==keys_len-1:
                text = '{"name":"' + value + '","style":"' + style['element'] + ';border-bottom:none"},'
            else:
                text = '{"name":"' + value + '","style":"' + style[
                    'element'] + '"},'
            node_text_mid.append(text)
    return node_text_start + data_pre+''.join(node_text_mid) +data_suf+ node_text_end


def server(model, host='localhost', port=9999, flow="horizontal", theme=Defualt):
    '''
    start a webserver to show model structure
    :param model: a model object such as tf.keras.Sequential/tf.keras.Model,
                  or h5 model path such as mnist.h5 and pb model path
    :param host: webserver host,default value is localhost
    :param port: webserver port,default value is 9999
    :param flow: layout style：vertical/ndraw.VERTICAL and horizontal/ndraw.HORIZONTAL
    :param theme:
                    ndraw.DEFAULT
                    ndraw.BLACK_WHITE
                    ndraw.GREEN_WHITE
                    ndraw.LIGHTBLACK_WHITE
    :return:
    '''
    from http.server import HTTPServer, BaseHTTPRequestHandler
    logging.info("see http://{}:{}".format(host, port))
    html = render(model, out_file=None, flow=flow, theme=theme)

    class Resquest(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

    server = HTTPServer((host, port), Resquest)
    server.serve_forever()


def render_graph(model, out_file='model.html', flow="horizontal", theme=Defualt,template_type='auto'):
    nodes_text = []
    nodes = []
    link_ids = []

    for i,node in enumerate(model.nodes):
        node_name = f'graphnode{i}'
        nodes_text.append(_generate_graph_nodes_data(node_name, node, theme=(theme if node.theme is None else node.theme),is_auto= True if template_type=='auto' else False))
        nodes.append(node_name)
    if template_type=='auto':
        html = auto_template_html \
            .replace("flowValue", flow.value if isinstance(flow, Flow) else flow) \
            .replace("templateJs", template_js) \
            .replace("nodesText", ';'.join(nodes_text)) \
            .replace("nodesList", str(nodes).replace('\'', ''))
    else:
        for j, link in enumerate(model.links):
            link_ids.append([link[0].id, link[1].id])
        html = stable_template_html \
            .replace("flowValue", flow.value if isinstance(flow, Flow) else flow) \
            .replace("templateJs", template_js) \
            .replace("nodesText", ';'.join(nodes_text)) \
            .replace("nodesList", str(nodes).replace('\'', ''))\
            .replace("linksList", str(link_ids))

    if out_file is not None and out_file.endswith(".html"):
        with open(out_file, 'w', encoding='utf-8') as file_w:
            file_w.write(html)
    return html


def render(model, out_file='model.html', flow="horizontal", theme=Defualt):
    '''
    start a webserver to show model structure
    :param model: a model object such as tf.keras.Sequential/tf.keras.Model,
                  or h5 model path such as mnist.h5 and pb model path
    :param host: webserver host,default value is localhost
    :param port: webserver port,default value is 9999
    :param flow: layout style：vertical/ndraw.VERTICAL and horizontal/ndraw.HORIZONTAL
    :param out_file: html file path that model will generate
    :param theme:
                    ndraw.DEFAULT
                    ndraw.BLACK_WHITE
                    ndraw.GREEN_WHITE
                    ndraw.LIGHTBLACK_WHITE
    :return: html
    '''
    if tf:
        if isinstance(model, tf.keras.Sequential) or isinstance(model, tf.keras.Model):
            nodes_text = []
            nodes = []
            for i, layer in enumerate(model.layers):
                res = _parse_layer(layer)
                node_name = f'node{i}'
                nodes_text.append(_generate_nodes_data(node_name, res, theme=theme))
                nodes.append(node_name)

            html = auto_template_html \
                .replace("flowValue", flow.value if isinstance(flow, Flow) else flow) \
                .replace("templateJs", template_js) \
                .replace("nodesText", ';'.join(nodes_text)) \
                .replace("nodesList", str(nodes).replace('\'', ''))
            if out_file is not None and out_file.endswith(".html"):
                with open(out_file, 'w', encoding='utf-8') as file_w:
                    file_w.write(html)
            return html
        elif isinstance(model, str):
            try:
                h5model = tf.keras.models.load_model(model)
                return render(h5model)
            except Exception as e:
                logging.error("invalid model path")
                raise e
        elif isinstance(model, AutoGraph):
            return render_graph(model,flow=flow,theme=theme,out_file=out_file)
        elif isinstance(model, StableGraph):
            return render_graph(model, flow=flow, theme=theme, out_file=out_file, template_type='stable')
        else:
            logging.error("invalid Graph!")
    else:
        if isinstance(model, AutoGraph):
          return render_graph(model,flow=flow,theme=theme,out_file=out_file)
        elif isinstance(model, StableGraph):
          return render_graph(model,flow=flow,theme=theme,out_file=out_file,template_type='stable')
        else:
            logging.error("invalid Graph!")
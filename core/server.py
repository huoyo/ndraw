# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   zhangchang
@Date  :   2021/12/1 20:31
'''
import logging
from core import template_html
from core import template_js

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
    }
    return res


def _generate_nodes_data(node_name, res):
    if len(res['input']) == 0:
        node_text = ' let ' + node_name + '= {' \
                                          '"style":"background-color:whitesmoke",\
                                 "id":"' + res['name'] + '",\
                                "title":{"name":"' + res['class'] + '","style":"font-size:14px;background-color:#4b804b;"},\
                                "data":[\
                                    {"name":"input_shape：' + res['input_shape'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"},\
                                    {"name":"output_shape：' + res['output_shape'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"},\
                                    {"name":"activation：' + res['activation'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"}\
                                ]\
                            }\n'
    elif len(res['input']) == 1:
        node_text = ' let ' + node_name + '= {    ' \
                                          '"style":"background-color:whitesmoke",\
                                          "id":"' + res['name'] + '","from":"' + res['input'][0] + '",\
                             "title":{"name":"' + res['class'] + '","style":"font-size:14px;background-color:#4b804b;"},\
                             "data":[\
                                 {"name":"input_shape：' + res['input_shape'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"},\
                                 {"name":"output_shape：' + res['output_shape'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"},\
                                 {"name":"activation：' + res['activation'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"}\
                             ],\
                         }\n'
    else:
        node_text = ' let ' + node_name + '= {' \
                                          '"style":"background-color:whitesmoke",\
                                                               "id":"' + res['name'] + '",\
                              "from":' + str(res['input']) + ',\
                             "title":{"name":"' + res['class'] + '","style":"font-size:14px;background-color:#4b804b;"},\
                             "data":[\
                                 {"name":"input_shape：' + res['input_shape'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"},\
                                   {"name":"output_shape：' + res['output_shape'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"},\
                                 {"name":"activation：' + res['activation'] + '","style":"font-size:13px;background-color:whitesmoke;color:black"}\
                             ]\
                         }\n'

    return node_text


def server(model, host='localhost', port=9999, flow="horizontal"):
    from http.server import HTTPServer, BaseHTTPRequestHandler
    logging.info("see http://{}:{}".format(host, port))
    html = render(model, out_file=None, flow=flow)

    class Resquest(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

    server = HTTPServer((host, port), Resquest)
    server.serve_forever()


def render(model, out_file='model.html', flow="horizontal"):
    if tf:
        if isinstance(model, tf.keras.Sequential) or isinstance(model, tf.keras.Model):
            nodes_text = []
            nodes = []
            for i, layer in enumerate(model.layers):
                res = _parse_layer(layer)
                node_name = f'node{i}'
                nodes_text.append(_generate_nodes_data(node_name, res))
                nodes.append(node_name)

            html = template_html \
                .replace("flowValue", flow) \
                .replace("templateJs", template_js) \
                .replace("nodesText", ';'.join(nodes_text)) \
                .replace("nodesList", str(nodes).replace('\'', ''))
            if out_file is not None and out_file.endswith(".html"):
                with open(out_file, 'w', encoding='utf-8') as file_w:
                    file_w.write(html)
            return html

        else:
            logging.error("invalid model!")

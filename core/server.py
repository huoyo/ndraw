# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   Chang Zhang
@Date  :   2021/12/1 20:31
'''
import logging
from core.constant import Flow
from core.theme import *
from draw.graph import AutoGraph
from draw.graph import StableGraph
from draw.graph import Graph
from core.parse import *

logging.basicConfig(level=logging.INFO)
try:
    import tensorflow as tf
except Exception as e:
    logging.warning(
        "failed to import tensorflow,please install tensorflow>=2.0 if you want to show model constructure of tensorflow! Of course,maybe you need ignore it when you want to show other model constructure.")

graph_parser = GraphParser()
tfmodel_parser = TFmodelParser()


def server(model, host='localhost', port=9999, flow="horizontal", theme=Defualt()):
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
    logging.info("@see http://{}:{}".format(host, port))
    html = render(model, out_file=None, flow=flow, theme=theme)

    class Resquest(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

    server = HTTPServer((host, port), Resquest)
    server.serve_forever()


def render(model, out_file='model.html', flow="horizontal", theme=Defualt()):
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
    if isinstance(model, AutoGraph):
        return graph_parser(model, flow=flow, theme=theme, out_file=out_file)
    elif isinstance(model, StableGraph):
        return graph_parser(model, flow=flow, theme=theme, out_file=out_file, template_type='stable')
    elif tf:
        if isinstance(model, tf.keras.Sequential) or isinstance(model, tf.keras.Model):
            return tfmodel_parser(model,out_file=out_file,flow=flow,theme=theme)
        elif isinstance(model, str):
            try:
                h5model = tf.keras.models.load_model(model)
                return render(h5model)
            except Exception as e:
                logging.error("invalid model path!")
                raise e
        else:
            logging.error("invalid model path!")
    else:
        logging.error("invalid Graph!")


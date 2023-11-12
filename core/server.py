# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Desc  :
@Author:   Chang Zhang
@Date  :   2021/12/1 20:31
'''
import math
import json
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

auto_graph_parser = AutoGraphParser()
stable_graph_parser = StableGraphParser()
tfmodel_parser = TFmodelParser()


def server(model, host='localhost', port=9999, init_x=0, init_y=0, flow="horizontal", theme=Defualt()):
    '''
    start a webserver to show model structure
    :param model: a model object such as tf.keras.Sequential/tf.keras.Model,
                  or h5 model path such as mnist.h5 and pb model path
    :param init_x: initial x of node[0]
    :param init_y: initial y of node[0]
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
    html = render(model, out_file=None, init_x=init_x, init_y=init_y, flow=flow, theme=theme)

    class NRequest(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

    server = HTTPServer((host, port), NRequest)
    server.serve_forever()


def render(model, out_file='model.html', init_x=0, init_y=0, flow="horizontal", theme=Defualt()):
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
        return auto_graph_parser(model, init_x=init_x, init_y=init_y, flow=flow, theme=theme, out_file=out_file)
    elif isinstance(model, StableGraph):
        return stable_graph_parser(model, init_x=init_x, init_y=init_y, flow=flow, theme=theme, out_file=out_file)
    elif tf:
        if isinstance(model, tf.keras.Sequential) or isinstance(model, tf.keras.Model):
            return tfmodel_parser(model, init_x=init_x, init_y=init_y, out_file=out_file, flow=flow, theme=theme)
        elif isinstance(model, str):
            try:
                h5model = tf.keras.models.load_model(model)
                return render(h5model, init_x=init_x, init_y=init_y)
            except Exception as e:
                logging.error("invalid model path!")
                raise e
        else:
            logging.error("invalid model path!")
    else:
        logging.error("invalid Graph!")


def get_cos_d(seqs):
    start = seqs[0]
    start1 = seqs[2]
    vec_start = [start1[0] - start[0], start1[1] - start[1]]
    coss = []
    for i in range(2, len(seqs), 2):
        seq = seqs[i]
        vec = [seq[0] - start[0], seq[1] - start[1]]
        cos = (vec_start[0] * vec[0] + vec_start[1] * vec[1]) / (
                    math.sqrt(vec_start[0] ** 2 + vec_start[1] ** 2) * math.sqrt(vec[0] ** 2 + vec[1] ** 2))

        coss.append(cos)
        vec_start = vec
        start = seq
    coss = [round(cos) for cos in coss]
    d = math.sqrt((seqs[0][0] - seqs[-1][0]) ** 2 + (seqs[0][1] - seqs[-1][1]) ** 2)
    return coss, d


def get_draw_intent(coses, d):
    n0 = 0
    distinct_coss = []
    for cos in coses:
        if cos not in distinct_coss:
            distinct_coss.append(cos)
        if cos == 0:
            n0 += 1

    intent = 'other'
    if len(distinct_coss) <= 2 and d > 30:
        intent = 'line'
    elif len(distinct_coss) < 2 and n0 < 2 and d <= 30:
        intent = 'circle'
    elif len(distinct_coss) >= 2 and n0 >= 2 and d <= 30:
        intent = 'rectangle'

    return {'intent': intent}


def draw_server(host='localhost', port=9999,db_dir='',db_reset = False):
    from http.server import HTTPServer, BaseHTTPRequestHandler
    logging.info("@see http://{}:{}".format(host, port))
    from core import draw_free_template_html
    from core import dream_msg_js
    from core import color_picker_js
    from core import template_js
    from core import draw_operate_js
    import dbm
    import atexit
    #     r：只读，要求文件必须存在，默认就是这个模式
    #     w：可读可写，要求文件必须存在
    #     c：可读可写，文件不存在会创建，存在则追加
    #     n：可读可写，文件不存在会创建，存在则清空
    import os
    if db_dir != '':
        if not db_dir.endswith("/"):
            db_dir = f'{db_dir}/'
    else:
        user_home = os.path.expanduser("~")
        db_dir = f'{user_home}/.ndraw'
        if not os.path.exists(db_dir):
            os.mkdir(f'{user_home}/.ndraw')

        db_dir = f'{db_dir}/'

    ndrawdb = dbm.open(f"{db_dir}ndrawdb", "n" if db_reset else 'c')

    def close_db():
        ndrawdb.close()
        logging.info("closing db")

    atexit.register(close_db)

    def save_drawed(name, content):
        res_bytes = json.dumps(content).encode('utf-8')
        ndrawdb[name] = res_bytes

    def get_drawed_keys():
        keys = ndrawdb.keys()
        key_names = [key.decode('utf-8') for key in keys]
        return key_names

    def get_drawed_by_key(key):
        res_dict = json.loads(ndrawdb.get(key).decode('utf-8'))
        return res_dict

    def delete_drawed_by_key(key):
        ndrawdb.pop(key)

    class NRequest(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = draw_free_template_html \
                    .replace("templateJs", f"{dream_msg_js};{color_picker_js};{template_js};{draw_operate_js}") \
                    .replace('filesList', str(get_drawed_keys()))
                self.wfile.write(html.encode())

        def do_POST(self):
            if self.path == '/drawIntent':
                request_data = self.rfile.read(int(self.headers['content-length']))
                request_data = request_data.decode()
                request_data = json.loads(request_data)
                request_data = request_data['seq']

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                if request_data == None or len(request_data) < 3:
                    self.wfile.write(json.dumps({"intent": "other"}).encode())
                else:
                    coses, d = get_cos_d(request_data)
                    intent_info = get_draw_intent(coses, d)
                    self.wfile.write(json.dumps(intent_info).encode())
            elif self.path == '/getHtml':
                request_data = self.rfile.read(int(self.headers['content-length']))
                request_data = request_data.decode()
                request_data = json.loads(request_data)
                file_name = request_data['name']
                html = get_drawed_by_key(file_name)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"content": html}).encode())
            elif self.path == '/saveHtml':
                request_data = self.rfile.read(int(self.headers['content-length']))
                request_data = request_data.decode()
                request_data = json.loads(request_data)
                name = request_data['name']
                content = request_data['content']
                nodes = request_data['nodes']
                links = request_data['links']
                linkColors = request_data['linkColors']
                info = {
                    'content': content,
                    'nodes': nodes,
                    'links': links,
                    'linkColors': linkColors,
                }
                save_drawed(name, info)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                self.wfile.write(json.dumps({"names": get_drawed_keys()}).encode())

            elif self.path == '/deleteHtml':
                request_data = self.rfile.read(int(self.headers['content-length']))
                request_data = request_data.decode()
                request_data = json.loads(request_data)
                name = request_data['name']

                delete_drawed_by_key(name)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                self.wfile.write(json.dumps({"names": get_drawed_keys()}).encode())

    server = HTTPServer((host, port), NRequest)
    server.serve_forever()

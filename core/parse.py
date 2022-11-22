import logging
from core import auto_template_html
from core import stable_template_html
from core import template_js
from core.constant import Flow
from core.theme import *
from draw.graph import AutoGraph
from draw.graph import StableGraph
from draw.graph import Graph


class CommParser(object):

    def __call__(self, model, init_x = 0,init_y = 0, out_file='model.html', flow="horizontal", theme=Defualt()):
        return self.render(model,init_x = init_x,init_y = init_y,  out_file=out_file, theme=theme, flow=flow)

    def render(self, model,init_x = 0,init_y = 0,  out_file='model.html', flow="horizontal", theme=Defualt()):
        pass

    def parse_layer(self, layer):
        pass

    def generate_node_data(self, node_name, res, theme=Defualt()):
        pass

    def update_style(self, node_data, style):
        if isinstance(node_data, Graph):
            if node_data.border_color is not None:
                style.border_color= node_data.border_color
            if node_data.title_color is not None:
                style.title_color= node_data.title_color

            if node_data.data_color is not None:
                style.data_color= node_data.data_color

            if node_data.theme is not None:
                style = node_data.theme

        elif isinstance(node_data, dict):
            if 'border_color' in node_data.keys() and node_data['border_color'] is not None:
                style.border_color=  node_data['border_color']

            if 'title_color' in node_data.keys() and node_data['title_color'] is not None:
                style.title_color=  node_data['title_color']

            if 'data_color' in node_data.keys() and node_data['data_color'] is not None:
                style.data_color = node_data['data_color']

            if 'theme' in node_data.keys() and node_data['theme'] is not None:
                style = node_data['theme']
        return style


class TFmodelParser(CommParser):

    def __init__(self):
        CommParser.__init__(self)
        self.trans = ['Dropout','Flatten','Lambda','Masking','Permute','RepeatVector','Reshape','Concatenate','concatenate',
                      'LayerNormalization',
                      'BatchNormalization',
                      ]
        self.pools = [
                      'AveragePooling1D',
                      'AveragePooling2D',
                      'AveragePooling3D',
                      'GlobalAveragePooling1D',
                      'GlobalAveragePooling2D',
                      'GlobalAveragePooling3D',
                      'MaxPooling1D',
                      'MaxPooling2D',
                      'MaxPooling3D',
                      ]
        self.activates = ['ELU','LeakyReLU','PReLU','ReLU','Softmax','ThresholdedReLU']
        self.models = ['Conv1D',
                       'Convolution1D',
                       'Conv1DTranspose',
                       'Conv1DTranspose',
                       'Conv2D','Conv2DTranspose',
                       'Conv3D',
                       'Conv3DTranspose',
                       'AbstractRNNCell',
                       'RNN',
                       'SimpleRNN',
                       'SimpleRNNCell',
                       'StackedRNNCells',
                       'GRU',
                       'GRUCell',
                       'LSTM',
                       'LSTMCell'
                       ]
        self.inputs = ['Input','InputLayer']


    def render(self, model,init_x = 0,init_y = 0, out_file='model.html', flow="horizontal", theme=Defualt):
        nodes_text = []
        nodes = []
        for i, layer in enumerate(model.layers):
            res = self.parse_layer(layer)
            node_name = f'node{i}'
            nodes_text.append(self.generate_node_data(node_name, res, theme=(theme if res['theme'] is None else res['theme'])))
            nodes.append(node_name)

        html = auto_template_html \
            .replace("flowValue", flow.value if isinstance(flow, Flow) else flow) \
            .replace("templateJs", template_js) \
            .replace("nodeDistanceX", "-30") \
            .replace("initXValue", str(init_x)) \
            .replace("initYValue", str(init_y)) \
            .replace("nodeDistanceY", "-55") \
            .replace("nodesText", ';'.join(nodes_text)) \
            .replace("nodesList", str(nodes).replace('\'', ''))
        if out_file is not None and out_file.endswith(".html"):
            with open(out_file, 'w', encoding='utf-8') as file_w:
                file_w.write(html)
        return html

    def parse_layer(self, layer):
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
        if res['class'] in self.inputs:
            class InputTheme(Theme):
                border_color = 'green'
                title_color = 'green'
                data_color = 'white'

            res['theme'] = InputTheme()

        elif res['class'] in self.trans:
            class ConcatenateTheme(Theme):
                border_color = '#1940ad'
                title_color = '#1940ad'
                data_color = 'white'

            res['theme'] = ConcatenateTheme()

        elif res['class'] in self.models:
            class ConvTheme(Theme):
                border_color = '#327355'
                title_color = '#327355'
                data_color = 'white'

            res['theme'] = ConvTheme()

        elif res['class'] in self.activates:
            class ActivateTheme(Theme):
                border_color = '#585777'
                title_color = '#585777'
                data_color = 'white'

            res['theme'] = ActivateTheme()
        elif res['class'] in self.activates:
            class PoolTheme(Theme):
                border_color = '#625fc1'
                title_color = '#625fc1'
                data_color = 'white'

            res['theme'] = PoolTheme()
        else:
            res['theme'] = None

        return res

    def generate_node_data(self, node_name, res, theme=Defualt()):
        style = self.update_style(res, theme)
        if len(res['input']) == 0:
            node_text_from = ''
        elif len(res['input']) == 1:
            node_text_from = '"from":"' + res['input'][0] + '",'
        else:
            node_text_from = '"from":' + str(res['input']) + ','

        node_text_start = ' let ' + node_name + '= {"style":'+str(style).replace('_','-')+', ' + node_text_from + ' "id":"' + \
                          res['name'] + '","title":{"name":"' + res['class'] + '"},"data":['
        node_text_end = ']}\n'
        node_text_mid = []
        filters = ['name', 'class', 'input','border_color','title_color','data_color','title_font_size','title_font_color','data_font_size','data_font_color','theme']
        for i, key in enumerate(res.keys()):
            value = res[key]
            if key not in filters and value is not None:
                text = '{"name":"' + key + '：' + (value if isinstance(value, str) else str(value)) + '"},'
                node_text_mid.append(text)
        return node_text_start + ''.join(node_text_mid) + node_text_end


class AutoGraphParser(CommParser):

    def render(self, model,init_x = 0,init_y = 0, out_file='model.html', flow="horizontal", theme=Defualt()):
        nodes_text = []
        nodes = []
        for i, node in enumerate(model.nodes):
            node_name = f'graphnode{i}'
            nodes_text.append(
                self.generate_node_data(node_name, node, theme=(theme if node.theme is None else node.theme)))
            nodes.append(node_name)
        html = auto_template_html \
            .replace("flowValue", flow.value if isinstance(flow, Flow) else flow) \
            .replace("templateJs", template_js) \
            .replace("nodeDistanceX", "-40") \
            .replace("nodeDistanceY", "55") \
            .replace("initXValue", str(init_x)) \
            .replace("initYValue", str(init_y)) \
            .replace("nodesText", ';'.join(nodes_text)) \
            .replace("nodesList", str(nodes).replace('\'', ''))

        if out_file is not None and out_file.endswith(".html"):
            with open(out_file, 'w', encoding='utf-8') as file_w:
                file_w.write(html)
        return html

    def generate_node_data(self, node_name, res, theme=Defualt):
        style = self.update_style(res, theme)
        if res.from_id is None:
            node_text_from = ''
        elif isinstance(res.from_id, str):
            node_text_from = '"from":"' + res.from_id + '",'
        elif isinstance(res.from_id, list):
            node_text_from = '"from":' + str(res.from_id) + ','

        node_text_start = ' let ' + node_name + '= {' + '"style":' + str(style).replace('_','-') + ', ' + node_text_from + ' "id":"' + res.id + '","title":{"name":"' + res.name + '"}'
        data_pre = ''
        data_suf = ''
        node_text_end = '}\n'
        node_text_mid = []
        if res.data is not None and len(res.data) > 0:
            data_pre = ',"data":['
            data_suf = ']'
            keys_len = len(res.data)
            for j, value in enumerate(res.data):
                if j == keys_len - 1:
                    text = '{"name":"' + value + '"},'
                else:
                    text = '{"name":"' + value + '"},'
                node_text_mid.append(text)
        return node_text_start + data_pre + ''.join(node_text_mid) + data_suf + node_text_end

class StableGraphParser(AutoGraphParser):

    def render(self, model,init_x = 0,init_y = 0, out_file='model.html', flow="horizontal", theme=Defualt()):
        nodes_text = []
        nodes = []
        link_ids = []

        for i, node in enumerate(model.nodes):
            node_name = f'graphnode{i}'
            nodes_text.append(
                self.generate_node_data(node_name, node, theme=(theme if node.theme is None else node.theme)))
            nodes.append(node_name)

        for j, link in enumerate(model.links):
            link_ids.append([link[0].id, link[1].id])
        html = stable_template_html \
            .replace("flowValue", flow.value if isinstance(flow, Flow) else flow) \
            .replace("templateJs", template_js) \
            .replace("nodesText", ';'.join(nodes_text)) \
            .replace("nodesList", str(nodes).replace('\'', '')) \
            .replace("linksList", str(link_ids))

        if out_file is not None and out_file.endswith(".html"):
            with open(out_file, 'w', encoding='utf-8') as file_w:
                file_w.write(html)
        return html

    def generate_node_data(self, node_name, res, theme=Defualt):
        style = self.update_style(res, theme)
        if res.from_id is None:
            node_text_from = ''
        elif isinstance(res.from_id, str):
            node_text_from = '"from":"' + res.from_id + '",'
        elif isinstance(res.from_id, list):
            node_text_from = '"from":' + str(res.from_id) + ','

        if hasattr(res, 'x') :
            node_text_from = '"x":' + str(res.x) + ','

        if hasattr(res, 'y') :
            node_text_from = node_text_from + '"y":' + str(res.y) + ','

        node_text_start = ' let ' + node_name + '= {' + '"style":' +str(style).replace('_','-') + ', ' + node_text_from + ' "id":"' + res.id + '","title":{"name":"' + res.name + '"}'
        data_pre = ''
        data_suf = ''
        node_text_end = '}\n'
        node_text_mid = []
        if res.data is not None and len(res.data) > 0:
            data_pre = ',"data":['
            data_suf = ']'
            keys_len = len(res.data)
            for j, value in enumerate(res.data):
                if j == keys_len - 1:
                    text = '{"name":"' + value + '"},'
                else:
                    text = '{"name":"' + value + '"},'
                node_text_mid.append(text)
        return node_text_start + data_pre + ''.join(node_text_mid) + data_suf + node_text_end

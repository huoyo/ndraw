from core import config
import os
root_path = os.path.abspath(os.path.dirname(__file__))
template_html = config.load_file(os.path.join(root_path,"template.html"))
template_js = config.load_file(os.path.join(root_path,"MetricFlow.js"))
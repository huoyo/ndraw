from core import config
import os
root_path = os.path.abspath(os.path.dirname(__file__))
auto_template_html = config.load_file(os.path.join(root_path,"AutoTemplate.html"))
stable_template_html = config.load_file(os.path.join(root_path,"StableTemplate.html"))
template_js = config.load_file(os.path.join(root_path,"MetricFlow.js"))
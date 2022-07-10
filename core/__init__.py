from core import config
import os
root_path = os.path.abspath(os.path.dirname(__file__))
auto_template_html = config.load_file(os.path.join(root_path,"AutoTemplate.html"))
stable_template_html = config.load_file(os.path.join(root_path,"StableTemplate.html"))
draw_free_template_html = config.load_file(os.path.join(root_path,"DrawFree.html"))
template_js = config.load_file(os.path.join(root_path,"MetricFlow.js"))
dream_msg_js = config.load_file(os.path.join(root_path,"dream-msg.min.js"))
color_picker_js = config.load_file(os.path.join(root_path,"colorpicker.min.js"))
draw_operate_js = config.load_file(os.path.join(root_path,"DrawOperate.js"))
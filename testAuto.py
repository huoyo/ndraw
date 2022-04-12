
import ndraw
g = ndraw.AutoGraph(name_unique=True)
# nodes = g\
#     .creates([ndraw.Node(name='黑白1',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE),ndraw.Node(name='黑白1',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE)])\
#     .tos([ndraw.Node(name='黑白11',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE),ndraw.Node(name='黑白22',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE)])\
#     .to("第三")\
# .tos([ndraw.Node("第二",data=["name:测试","color:hggg"]),ndraw.Node("第二",data=["name:测试","color:hggg"]),ndraw.Node("第二",data=["name:测试","color:hggg"])])\
start1= g.create("开始")
start2= start1.to("开始2")
start3= start1.to("开始3")
nodes4= start2.to("中间")
nodes4= start3.to("中间")

# 多类型创建  任意关系创建

ndraw.server(nodes4,theme=ndraw.GREEN_WHITE,flow=ndraw.HORIZONTAL)
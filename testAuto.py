
import ndraw
g = ndraw.AutoGraph()
nodes = g\
    .creates([ndraw.Node(name='黑白1',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE),ndraw.Node(name='黑白1',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE)])\
    .tos([ndraw.Node(name='黑白11',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE),ndraw.Node(name='黑白22',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE)])\
    .to("第三")\
.tos([ndraw.Node("第二",data=["name:测试","color:hggg"]),ndraw.Node("第二",data=["name:测试","color:hggg"]),ndraw.Node("第二",data=["name:测试","color:hggg"])])\
# start1= g.create("开始")
# start2= g.create("开始2")
# nodes= start1.to("中间")

# 多类型创建  任意关系创建
# print(nodes.nodes)
ndraw.server(nodes,theme=ndraw.GREEN_WHITE,flow=ndraw.HORIZONTAL)
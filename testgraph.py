from draw.graph import Graph
import ndraw
g = Graph()
nodes = g\
    .create("开始")\
    .to("中间",data=["hjhkhjj","hjhkhjj","hjhkhjj","hjhkhjj"])\
    .to("中间",data=["hjhkhjj"])\
    .to("中间",data=["hjhkhjj"])\
    .to("中间")
# start1= g.create("开始")
# start2= g.create("开始2")
# nodes= start1.to("中间")

# 多类型创建  任意关系创建
print(nodes)
ndraw.server(nodes,theme=ndraw.BLACK_WHITE,flow=ndraw.HORIZONTAL)
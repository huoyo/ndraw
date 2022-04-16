
import ndraw
g = ndraw.AutoGraph(name_unique=False)
# nodes = g\
#     .creates([ndraw.Node(name='黑白1',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE),ndraw.Node(name='黑白1',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE)])\
#     .tos([ndraw.Node(name='黑白11',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE),ndraw.Node(name='黑白22',data =['哈哈哈','kjkjkkjkj'],theme=ndraw.BLACK_WHITE)])\
#     .to("第三")\
# .tos([ndraw.Node("第二5",data=["name:测试","color:hggg","color:hggg"]),
#       ndraw.Node("第二4",data=["name:测试","color:hggg","color:hggg"]),
#       ndraw.Node("第二2",data=["name:测试","color:hggg","color:hggg"]),
#       ndraw.Node("第二1",data=["name:测试","color:hggg","color:hggg"])
#       ])\
start1= g.create("开始").to("开始2").to("开始3").to("开始4")
# start2= start1.to("开始2")
# start3= start1.to("开始3")
# start3_= start1.to("开始31")
# nodes4= start2.to("中间")
# nodes4= start3.to("中间")
# # nodes4_= start3_.to("中间")
# nodes4.server(theme=ndraw.BlueWhite)


# 多类型创建  任意关系创建
ndraw.server(start1,flow=ndraw.HORIZONTAL)
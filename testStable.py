
import ndraw
g = ndraw.StableGraph(name_unique=True)

node1 = g.add_node(ndraw.Node(name='节点1',x=10,y=10))
node2 = g.add_node(ndraw.Node(name='节点1',data =['111111111','22222222'],x=200,y=10))
node3 = g.add_node(ndraw.Node(name='节点3',data =['111111111','22222222'],x=10,y=200))
g.add_link((node1,node2))
g.add_link((node1,node3))
ndraw.server(g,theme=ndraw.DEFAULT)
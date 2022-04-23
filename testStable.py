
import ndraw
g = ndraw.StableGraph(name_unique=False)

node1 = g.add_node(ndraw.Node(name='节点1',x=100,y=10,theme=ndraw.BlueWhite))
node2 = g.add_node(ndraw.Node(name='节点1',data =['111111111','22222222'],x=200,y=10,theme=ndraw.GreenWhite))
node3 = g.add_node(ndraw.Node(name='节点3',data =['111111111','22222222'],x=10,y=200))
g.add_link((node1,node2))
g.add_link((node1,node3))
g.server(theme=ndraw.RED_WHITE)
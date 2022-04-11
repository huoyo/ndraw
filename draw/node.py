

class Node(object):

    def __init__(self,name,data=[],x=0,y=0,theme=None,border_color=None,title_color=None,data_color=None):
        self.name= name
        self.data= data
        self.theme= theme
        self.border_color= border_color
        self.title_color= title_color
        self.data_color= data_color
        self.x= x
        self.y=y